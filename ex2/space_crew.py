from enum import Enum
from pydantic import Field, BaseModel

class Rank(Enum):
    Cadet = "cadet"
    Officer = "officer" 
    Lieutenant = "lieutenant" 
    Captain  = "captain" 
    Commander = "commander"

class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank 
    age:  int = Field(ge=18, le=80)
    specialization: str=Field(ge=3, le=30)
    years_experience: int=Field(ge=0, le=50)
    is_active: bool =True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length = 5, max_length = 15)
• mission_name: String, 3-100 characters
• destination: String, 3-50 characters
• launch_date: DateTime
• duration_days: Integer, 1-3650 days (max 10 years)
• crew: List of CrewMember, 1-12 members
• mission_status: String, defaults to "planned"
• budget_millions: Float, 1.0-10000.0 million dollars