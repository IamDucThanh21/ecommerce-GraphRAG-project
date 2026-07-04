from fluvius.domain.aggregate import Aggregate, action
 
from .service import ask_graph
 
 
class EcomAiAggregate(Aggregate):
 
    @action("graph-query-answered", resources="ai-query")
    async def ask(self, *, query: str):
        """Run the full pipeline: user query -> Cypher -> Neo4j -> Gemini answer.
 
        Uses the Neo4j driver + Gemini client singletons initialized at
        app startup via ecom_ai.startup.setup().
        """
        result = ask_graph(query)
        return result
 