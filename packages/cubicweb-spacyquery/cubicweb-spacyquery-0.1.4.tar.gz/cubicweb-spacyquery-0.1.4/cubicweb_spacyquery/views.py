# -*- coding: utf-8 -*-
# copyright 2025 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""cubicweb-spacyquery views/forms/actions/components for web ui"""
import urllib.parse

from cubicweb_web.views.startup import StartupView

from cubicweb_web import httpcache
from cubicweb_web.views.urlrewrite import SimpleReqRewriter

from cubicweb_spacyquery.query_extractor import llm_rewrite_queries
from cubicweb_spacyquery.spacyquery import (
    get_entity_extractor,
    get_query_extractor,
    ask,
)

from spacy import displacy


class SpacyQueryRewriter(SimpleReqRewriter):
    priority = 100

    rules = [
        ("/spacyquery", dict(vid="spacyquery_startup")),
        ("/query", dict(vid="query_startup")),
    ]


SPACY_QUERY_TEMPLATE = """
<h1 style="text-align: center; margin-bottom: 5px;">Pose-moi une question</h1>
<hr style="width: 60%; margin: 0 auto; border: 1px solid #ccc;">
<div class="container" style="height: 100vh; width: 100%; position: relative;">
    <div class="row" style="height: 100%;">
        <div class="col-xs-12 col-md-6 col-md-offset-3" style="position: absolute; top: 20.33%; left: 25%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; width: 100%;">
            <form id="search-form" class="input-group" style="width: 100%; display: flex; flex-direction: row; align-items: center;">
                <input type="search" id="search-input" name="q"
                    class="form-control" placeholder="Rechercher..." value="{q}"
                    required>
                <button type="submit" class="btn btn-primary">Rechercher</button>
            </form>
            <!-- Zone pour afficher les résultats -->
            <div id="search-results" style="width: 100%; margin-top: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 4px; min-height: 50px;">
                <!-- Les résultats de la recherche s'afficheront ici -->
                {output}
            </div>
        </div>
    </div>
</div>
"""  # noqa: E501


def get_question(url):
    return urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("q", [""])[0]


RQL_BUTTON = """
  <a href="http://localhost:8080/view?{}" class="btn btn-primary" role="button">
    Tester la requête
  </a>
"""


def create_colors_options(docs):
    colors = {"VALUE": "#7aecec"}
    for ent in docs.ents:
        if ":" not in ent.label_:
            if ent.label_ in colors:
                pass
            elif ent.label_[0].isupper():
                colors[ent.label_] = "#aa9cfc"
            else:
                colors[ent.label_] = "#bfe1d9"
        else:
            colors[ent.label_] = "#e4e7d2"
    return colors


def generate_query_result_table(queries):
    table = "<table style='table-layout: auto ; width: 100%'><thead>"
    table += "<tr><th>Requêtes</th><th>Explications</th><th></th></tr></thead>\n"
    table += "<tbody>"
    try:
        nl_queries = [q.to_nl() for q in queries]
        try:
            nl_queries = llm_rewrite_queries(queries)
        except Exception:
            import traceback

            traceback.print_exc()

        for query, nl_query in zip(queries, nl_queries):
            button_query = {
                "rql": query.to_rql(),
                "vtitle": nl_query,
            }
            button = RQL_BUTTON.format(urllib.parse.urlencode(button_query))

            table += (
                f"<tr>"
                f"<td>{query.to_rql()}</td>"
                f"<td>{nl_query}</td>"
                f"<td>{button}</td>"
                f"</tr>"
            )
    except Exception:
        import traceback

        traceback.print_exc()
        table += "<tr><td colspan='3'>Aucune requête trouvée<td></li>"
    table += "</tbody></table>"

    return table


class SpacyQueryView(StartupView):
    __select__ = StartupView.__select__
    __regid__ = "spacyquery_startup"
    http_cache_manager = httpcache.NoHTTPCacheManager

    def call(self):
        cnx = self._cw.cnx
        ee = get_entity_extractor(cnx)
        question = get_question(self._cw.url())
        spacy_ent_html, spacy_dep_html = "", ""
        if question:
            docs = ee.get_nlp_analyze(question)
            colors = create_colors_options(docs)
            spacy_ent_html = displacy.render(
                docs, style="ent", options={"colors": colors}
            )
            spacy_dep_html = displacy.render(
                docs, style="dep", options={"compact": True, "distance": 50}
            )
            table = generate_query_result_table(ask(cnx, question))
            output = """
            <h2> Recherche dans la question des mots clés du modèle et des données : </h2>
            {}
            <h2> Recherche dans la question des liens entre les termes : </h2>
            {}
            <h2> Proposition de requête RQL :</h2>
            {}
            """.format(
                spacy_ent_html, spacy_dep_html, table
            )
            self.w(SPACY_QUERY_TEMPLATE.format(output=output, q=question))
        else:
            self.w(
                SPACY_QUERY_TEMPLATE.format(
                    output="Aucun résultat pour le moment", q=question
                )
            )


class QueryView(StartupView):
    __regid__ = "query_startup"
    http_cache_manager = httpcache.NoHTTPCacheManager

    def call(self):
        cnx = self._cw.cnx
        question = get_question(self._cw.url())
        query_extractor = get_query_extractor(cnx)
        if question:
            target_entities = [i for i in question.split() if "#" not in i]
            target_attributes = [i for i in question.split() if "#" in i]

            table = generate_query_result_table(
                query_extractor.get_queries(target_entities, target_attributes)
            )

            output = f"<h2> Proposition de requête RQL :</h2> {table}"
            self.w(SPACY_QUERY_TEMPLATE.format(output=output, q=question))
        else:
            self.w(
                SPACY_QUERY_TEMPLATE.format(
                    output="Aucun résultat pour le moment", q=question
                )
            )


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__)
