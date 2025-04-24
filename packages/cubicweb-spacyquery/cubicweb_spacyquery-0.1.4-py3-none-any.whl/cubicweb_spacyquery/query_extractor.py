import networkx as nx
import pandas as pd

CW_INTERNAL_ENTITIES = {"TrInfo", "Workflow"}


class GraphQuery(nx.Graph):
    def __init__(
        self,
        *args,
        target_entities=None,
        target_attributes=None,
        translator=lambda x: x,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.target_entities = target_entities
        self.target_attributes = target_attributes
        self.translator = translator
        self.type_to_var = {}
        self._definitions = []

    @staticmethod
    def to_variable(txt):
        return txt.upper()

    def get_node_var_name(self, node):
        if node not in self.type_to_var:
            var_name = self.to_variable(node)
            self._definitions.append(f"{var_name} is {node}")
            self.type_to_var[node] = var_name
        else:
            var_name = self.type_to_var[node]
        return var_name

    def convert_attr_into_rql(self, attr_type):
        descr = attr_type.split("#")
        instance_type, attr_name, expected_value = [None] * 3
        if len(descr) == 2:
            instance_type, attr_name = descr
            attr_code = GraphQuery.to_variable(instance_type) + "_" + attr_name.upper()
            self.type_to_var[attr_type] = attr_code
            self._definitions.append(f"%({instance_type})s {attr_name} {attr_code}")
        elif len(descr) == 3:
            instance_type, attr_name, expected_value = descr
            self.get_node_var_name(instance_type)
            self._definitions.append(
                f"%({instance_type})s {attr_name} '{expected_value}'"
            )
        elif len(descr) == 4:
            instance_type, attr_name, expected_value, qtype = descr
            self.get_node_var_name(instance_type)
            if qtype == "I":
                self._definitions.append(
                    f"%({instance_type})s {attr_name} ILIKE '%%{expected_value}%%'"
                )

    @property
    def definitions(self):
        return [dd % self.type_to_var for dd in sorted(self._definitions)]

    @property
    def var_to_type(self):
        return {v: t for t, v in self.type_to_var.items()}

    def __repr__(self):
        return f"<{self.__class__.__name__}: `{self.to_rql()}`>"

    def to_rql(self):
        query_part = []

        # We have nodes attributes, looking like etype#attr
        # but sometime, we look for a specific value, and in target_attributes
        # we have etype#attr#value
        # here, we create a map from nodes to the target attribute values
        # This map will be used when we encounter node attr
        nodes_to_target_attributes = {
            "#".join(ta.split("#")[:2]): ta for ta in self.target_attributes
        }

        if len(self.nodes) == 1:
            var_type = list(self.nodes)[0]
            var_name = self.to_variable(var_type)
            return f"Any {var_name} WHERE {var_name} is {var_type}"

        for node in filter(lambda node: "|" in node, self.nodes):
            sub, rel, obj = node.split("|")
            if rel == "attribute":
                sub_varname = self.get_node_var_name(sub)
                self.convert_attr_into_rql(nodes_to_target_attributes.get(obj, obj))
            else:
                sub_varname = self.get_node_var_name(sub)
                obj_varname = self.get_node_var_name(obj)
                query_part.append(f"{sub_varname} {rel} {obj_varname}")

        beg_query = f"Any {', '.join(sorted(self.type_to_var.values()))} WHERE "
        query_txt = f"{beg_query}{', '.join(self.definitions)}"
        if query_part:
            query_txt += f", {','.join(sorted(query_part))}"

        return query_txt

    def to_nl(self):
        _ = self.translator
        query_part = []

        # We have nodes attributes, looking like etype#attr
        # but sometime, we look for a specific value, and in target_attributes
        # we have etype#attr#value
        # here, we create a map from nodes to the target attribute values
        # This map will be used when we encounter node attr
        nodes_to_target_attributes = {
            "#".join(ta.split("#")[:2]): ta for ta in self.target_attributes
        }

        if len(self.nodes) == 1:
            var_type = list(self.nodes)[0]
            return f"Je veux tous les {_(var_type + '_plural')}"

        for node in filter(lambda node: "|" in node, self.nodes):
            sub, rel, obj = node.split("|")
            if rel == "attribute":
                self.get_node_var_name(sub)  # called to populated type_to_var
                self.convert_attr_into_rql(nodes_to_target_attributes.get(obj, obj))

                match nodes_to_target_attributes[obj].split("#"):
                    case _, attr:
                        # nothing to do, the part is added before the `WHERE`
                        # in the final sentence
                        pass
                    case _, attr, value:
                        query_part.append(
                            f"{_(sub + '_plural')} ont un {_(attr)} qui vaut {value!r}"
                        )
                    case _, attr, value, _:
                        query_part.append(
                            f"{_(sub + '_plural')} ont un {_(attr)} qui contient {value!r}"
                        )
            else:
                query_part.append(f"{_(sub + '_plural')} {_(rel)} {_(obj + '_plural')}")
                self.get_node_var_name(sub)  # called to populated type_to_var
                self.get_node_var_name(obj)

        beg_query = "Je veux tous les "
        items = []
        for type_ in sorted(self.type_to_var, key=lambda x: self.type_to_var[x]):
            if "#" in type_:
                type_, attr = type_.split("#")[:2]
                items.append(f"{_(attr)} des {_(type_ + '_plural')}")
            else:
                items.append(_(f"{type_}_plural"))
        beg_query += ", ".join(items)
        beg_query += " pour lesquels"
        query_txt = beg_query
        if query_part:
            query_txt += f" {', '.join(sorted(query_part))}"

        return query_txt


class QueryExtractor:
    def __init__(self, df, weight_file=None, translator=lambda x: x):
        self.df = df
        self.weight_df = None
        self.translator = translator
        if weight_file and weight_file.is_file():
            self.weight_df = pd.read_csv(weight_file, delimiter=";")
        self.graph = nx.Graph()
        for node1, rel, node2 in self.df.values:
            weight = self.compute_weight(node1, rel, node2)

            rel_label = f"{node1}|{rel}|{node2}"
            self.graph.add_edge(node1, rel_label, weight=weight)
            self.graph.add_edge(rel_label, node2, weight=weight)

    def _get_weight(self, subj, pred, obj):
        selection = self.weight_df[["subj", "pred", "obj"]]
        row = self.weight_df[
            selection.isin({"subj": [subj], "pred": [pred], "obj": [obj]}).all(axis=1)
        ]
        if row.shape and row.shape[0] == 1:
            return row["weight"].iloc[0]

    def compute_weight(self, subj, pred, obj):
        if self.weight_df is None:
            if subj.startswith("CW") or obj.startswith("CW"):
                return 3
            if subj in CW_INTERNAL_ENTITIES or obj in CW_INTERNAL_ENTITIES:
                return 3
            return 1
        weight = self._get_weight(subj, pred, obj)
        if weight is not None:
            return weight
        weight = self._get_weight(subj, pred, "*")
        if weight is not None:
            return weight
        weight = self._get_weight(subj, "*", obj)
        if weight is not None:
            return weight
        weight = self._get_weight("*", pred, obj)
        if weight is not None:
            return weight
        weight = self._get_weight("*", pred, "*")
        if weight is not None:
            return weight
        weight = self._get_weight("*", "*", obj)
        if weight is not None:
            return weight
        return 1

    def _get_subgraphs(self, subgraph, max_radius=6):
        def get_not_connected_nodes(g):
            if len(subgraph) == 1:
                return
            for node in g.nodes:
                if not g.edges(node):
                    yield node

        target_nodes = {n for n in subgraph.nodes if "|" not in n}
        not_connected_nodes = list(get_not_connected_nodes(subgraph))
        if not not_connected_nodes:
            yield subgraph

        for current_node in not_connected_nodes:
            found_nodes_with_current_radius = False
            for radius in range(3, max_radius + 3, 3):
                ego_graph = nx.ego_graph(
                    self.graph, current_node, radius=radius, distance="weight"
                )
                for node in target_nodes:
                    if node == current_node:
                        continue
                    if node in ego_graph.nodes:
                        found_nodes_with_current_radius = True
                        paths = nx.all_shortest_paths(
                            self.graph, current_node, node, weight="weight"
                        )
                        for path in paths:
                            new_subgraph = subgraph.copy()
                            for n1, n2 in zip(path[:-1], path[1:]):
                                edges_properties = self.graph.edges[n1, n2]
                                new_subgraph.add_edge(n1, n2, **edges_properties)

                            yield from self._get_subgraphs(new_subgraph)
                if found_nodes_with_current_radius:
                    # we have found a path between the current_node and a node.
                    # let's stop the search in the neighborhoods.
                    break

    def get_queries(self, target_entities, target_attributes) -> list[GraphQuery]:
        """Return all the subgraphs visiting the target_nodes

        Returns:
            list of (subgraph, weight)
        """
        target_nodes = list(target_entities)

        for ta in target_attributes:
            entity, attr, *_ = ta.split("#")

            target_nodes.append(entity)
            target_nodes.append(f"{entity}#{attr}")

        subgraph = nx.Graph()
        subgraph.add_nodes_from(target_nodes)

        all_subgraphs_and_weight = []

        for a_subgraph in self._get_subgraphs(subgraph):
            for existing_subgraph, _ in all_subgraphs_and_weight:
                if nx.utils.graphs_equal(existing_subgraph, a_subgraph):
                    break
            else:
                weight = sum(w for _, _, w in a_subgraph.edges.data("weight"))
                all_subgraphs_and_weight.append((a_subgraph, weight))

        return [
            GraphQuery(
                sg,
                target_entities=target_entities,
                target_attributes=target_attributes,
                translator=self.translator,
            )
            for sg, _ in sorted(all_subgraphs_and_weight, key=lambda x: x[1])
        ]


def llm_rewrite_queries(queries: list[GraphQuery], max_queries=10):
    import os
    import json
    from openai import OpenAI

    if not (os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_BASE_URL")):
        raise ValueError(
            "You must provide OPENAI_BASE_URL and OPENAI_API_KEY "
            "to use the LLM feature."
        )

    if not queries:
        return []

    queries = queries[:max_queries]

    def llm(system_prompt: str, user_prompt: str) -> str:
        client = OpenAI(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        print(system_prompt)
        print(user_prompt)
        response = client.chat.completions.create(
            model="llama-3.3-70b-instruct",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "Queries",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "rewritting": {
                                    "type": "string",
                                    "description": (
                                        "The rewritting of the query into french"
                                    ),
                                },
                            },
                            "additionalProperties": False,
                            "required": ["rewritting"],
                        },
                    },
                },
            },
        )
        return json.loads(response.choices[0].message.content)

    results = []

    for i in range(0, len(queries) + 1, max_queries):
        some_queries = queries[i * max_queries : (i + 1) * max_queries]
        queries_and_explanation = llm(
            system_prompt=(
                "You are a fluent french speaker. Given a list of sentences "
                "in basic french, rewrite them into simple french. "
                "Simplify the sentence if you can."
            ),
            user_prompt=(
                "QUERIES:\n"
                + "- "
                + "- ".join(f"`{q.to_nl()}`\n" for q in some_queries)
                + "\n"
            ),
        )

        # add a safe guard to return only queries generated by the graph analysis
        # and not by the LLM hallucinations
        results.extend(queries_and_explanation)
        # (record for record in queries_and_explanation if record["query"] in queries)
        # )

    return [r["rewritting"] for r in results]
