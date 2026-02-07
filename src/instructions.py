from typing import Optional
from pydantic import BaseModel


class EmployeeFilters(BaseModel):
    age_1: Optional[int]
    age_2: Optional[int]


class EmployeeQuery(BaseModel):
    country: str
    corporation: str
    filters: EmployeeFilters


class BasicResponse(BaseModel):
    response: str


class QuarterlyFilters(BaseModel):
    year_1: Optional[int]
    quarter_1: Optional[int]
    year_2: Optional[int]
    quarter_2: Optional[int]


class QuarterlyQuery(BaseModel):
    country: str
    corporation: str
    filters: QuarterlyFilters


EMPLOYEE_AI_INSTRUCTIONS = """
You are an expert of statistics. Answer user questions based on the data you receive.
You will detect what language user speaks, and answer with the same language as user is using.
"""

QUARTERLY_AI_INSTRUCTIONS = """
You are an expert of finances. Answer user questions based on the data you receive.
You will detect what language user speaks, and answer with the same language as user is using.
"""

INSTRUCTIONS_ABOUT_TOPICS = """
Detect the topic from user question. Possible topics are:
employee_query, when user wants to know something employee related.
quarterly_query, when user wants to know something about corporations quarterly data.
Return just one of the topics, without additional explanations.
"""


# EMPLOYEE_FORMAT = {
#     "format": {
#         "type": "json_schema",
#         "name": "response_schema",
#         "schema": {
#             "type": "object",
#             "properties": {
#                 "country": {
#                     "type": "string",
#                 },
#                 "corporation": {"type": "string"},
#                 "filters": {
#                     "type": "object",
#                     "properties": {
#                         "age_1": {"type": ["integer", "null"]},
#                         "age_2": {"type": ["integer", "null"]},
#                     },
#                     "required": ["age_1", "age_2"],
#                     "additionalProperties": False,
#                 },
#             },
#             "required": ["country", "corporation", "filters"],
#             "additionalProperties": False,
#         },
#     }
# }
