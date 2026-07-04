from fluvius.domain.command import Command
from fluvius.helper import serialize_mapping
 
from . import datadef
 
 
class AskGraphCommand(Command):
    """Send a natural-language question through the Cypher/Neo4j/Gemini pipeline."""
 
    Data = datadef.AskGraphData
 
    class Meta:
        key = "ask-graph"
        description = "Ask the AI a question; it queries the product graph and replies."
        resource_init = True
        resources = ("ai-query",)
        tags = ["ai", "graph"]
        auth_required = True
        policy_required = False
 
    async def _process(self, agg, stm, payload):
        data = serialize_mapping(payload)
 
        result = await agg.ask(query=data["query"])
 
        yield agg.create_response(
            serialize_mapping(result),
            _type="ask-graph-response",
        )
 