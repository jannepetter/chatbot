import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.instructions import (
    EmployeeQuery,
    QuarterlyQuery,
    EMPLOYEE_AI_INSTRUCTIONS,
    QUARTERLY_AI_INSTRUCTIONS,
    BasicResponse,
)
from src.tools import get_query_dict, get_employees, get_quarterlies, get_topic

load_dotenv()

ENV = os.getenv("ENV")

OPENAI_CLIENT = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


TOOL_MAPPING = {
    "employee_query": (
        EmployeeQuery,
        get_employees,
        EMPLOYEE_AI_INSTRUCTIONS,
        BasicResponse,
    ),
    "quarterly_query": (
        QuarterlyQuery,
        get_quarterlies,
        QUARTERLY_AI_INSTRUCTIONS,
        BasicResponse,
    ),
}


def ask(question, topic=None):

    if not topic:
        topic = get_topic(OPENAI_CLIENT, question)

    tool_items = TOOL_MAPPING.get(topic, None)
    if not tool_items:
        print("I am sorry, I did not catch the topic of discussion")
        return
    schema, tool_function, assistant_instructions, response_format = tool_items

    question_data = get_query_dict(OPENAI_CLIENT, question, schema)

    data = tool_function(question_data)
    content = [
        {
            "role": "developer",
            "content": f"Answer user questions based on following data: {json.dumps(data,ensure_ascii=False)}",
        }
    ]
    content.append({"role": "user", "content": question})

    # dont care intelligence on tests, but the response format
    use_model = "gpt-4.1-nano" if ENV == "test" else "gpt-4.1-mini"

    response = OPENAI_CLIENT.responses.parse(
        model=use_model,
        instructions=assistant_instructions,
        input=content,
        text_format=response_format,
        prompt_cache_key="assistant_instructions",
    )
    ai_reply = response.output_parsed.model_dump()

    return ai_reply
