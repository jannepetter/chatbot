from openai import OpenAI
from src.data import EMPLOYEE_DATA, QUARTERLY_RESULTS
from src.instructions import INSTRUCTIONS_ABOUT_TOPICS


def get_query_dict(
    client: OpenAI,
    question: str,
    data_format,
    special_instructions="",
):

    # not necessarily even needed to provide the dict.
    instructions = f"""
    Convert the user question into JSON with fields in the provided response format
    Special instructions: {special_instructions}
    Respond with JSON only.
    """
    retries = 3
    for i in range(retries):
        try:
            response = client.responses.parse(
                model="gpt-4.1-nano",  # fast and sufficient. Faster than 5-nano
                instructions=instructions,
                input=question,
                text_format=data_format,
                prompt_cache_key="query_dict_instructions",
            )
            data = response.output_parsed.model_dump()
            return data
        except Exception:  # pylint:disable=broad-except
            if i == retries - 1:
                raise


def get_topic(client, question):
    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions=INSTRUCTIONS_ABOUT_TOPICS,
        input=question,
        prompt_cache_key="topic_instructions",
    )
    return response.output_text


def get_employees(question_data):

    country = question_data["country"]
    corporation = question_data["corporation"]
    filters = question_data["filters"]
    age_1 = filters.get("age_1", None)
    age_2 = filters.get("age_2", None)

    country_data = EMPLOYEE_DATA.get(country.lower(), None)

    if not country_data:
        return []

    corp_data = country_data.get(corporation.lower(), None)

    if not corp_data:
        return []

    if age_1 and age_2:
        employees = [e for e in corp_data["employees"] if age_1 <= e["age"] <= age_2]
    elif age_1:
        employees = [e for e in corp_data["employees"] if age_1 == e["age"]]
    else:
        employees = corp_data["employees"]

    return {"country": country, "corporation": corporation, "employees": employees}


def get_quarterlies(question_data):

    country = question_data["country"].lower()
    corporation = question_data["corporation"].lower()
    filters = question_data["filters"]
    year_1 = filters.get("year_1", None)
    year_2 = filters.get("year_2", None)

    quarter_1 = filters.get("quarter_1", None)
    quarter_2 = filters.get("quarter_2", None)

    country_data = QUARTERLY_RESULTS.get(country, None)
    if not country_data:
        return []

    corp_data = country_data.get(corporation, None)

    if not corp_data:
        return []

    comp_list_1 = []
    comp_list_2 = []

    quarters_list = corp_data["quarters"]
    for item in quarters_list:
        if item["year"] == year_1 and item["quarter"] == quarter_1:
            comp_list_1.append(item)
        if item["year"] == year_2 and item["quarter"] == quarter_2:
            comp_list_2.append(item)

    return {"list_1": comp_list_1, "list_2": comp_list_2}
