from fluvius.data import DataModel
from pydantic import Field
 
 
class AskGraphData(DataModel):
    """Data model for sending a natural-language query to the AI graph pipeline."""
 
    query: str = Field(..., description="User's natural language question.", min_length=1)
 