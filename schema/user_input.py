from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal
from config.city_tier import TIER_1_CITIES, TIER_2_CITIES
from config.occupations import OCCUPATIONS

class InsuranceRequestUserInput(BaseModel):
    age: Annotated[int, Field(gt=0, lt=120, description='Age of the user', examples=[25])]
    weight: Annotated[float, Field(gt=0, lt=200, description='Weight in kg', examples=[70.0])]
    height: Annotated[float, Field(gt=0, lt=2.5, description='Height in meters', examples=[1.75])]
    smoker: Annotated[bool, Field(description='Whether the user is a smoker', examples=[False])]
    city: Annotated[str, Field(description='City of the user', examples=['Delhi'])]
    income_lpa: Annotated[float, Field(gt=0, description='Annual income in Lakhs', examples=[10.0])]
    occupation: Annotated[Literal[*OCCUPATIONS],Field(description='Occupation of the user', examples=['student'])]

    @field_validator('city')
    @classmethod
    def validate_city(cls, v: str) -> str:
        v = v.strip().title()
        return v
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in TIER_1_CITIES:
            return 1
        elif self.city in TIER_2_CITIES:
            return 2
        else:
            return 3