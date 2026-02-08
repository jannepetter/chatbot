from unittest.mock import patch
from src.ask_ai import ask, get_query_dict, OPENAI_CLIENT, EmployeeQuery, TOOL_MAPPING
from tests import AIBaseTCase

FAKE_DATA = {
    "country": "finland",
    "corporation": "Joo Tech",
    "employees": [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 33}],
}


class AIModelTestCase(AIBaseTCase):

    @patch("src.ask_ai.get_query_dict")
    @patch.dict(
        "src.ask_ai.TOOL_MAPPING",
        {
            "employee_query": AIBaseTCase.patch_tool_fetch(
                TOOL_MAPPING, "employee_query", FAKE_DATA
            )
        },
    )
    def test_employee_answer_flow(self, mock_get_query_dict):
        """
        Test that model will answer in correct format
        """

        mock_get_query_dict.return_value = {
            "country": "Finland",
            "corporation": "Joo Tech",
            "filters": {"age_1": 30, "age_2": None},
        }
        result = ask(
            "Who works in Finland department of Joo Tech and is over 30 years old"
            "employee_query"
        )

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        # assert contract, not content
        self.assertIn("response", result)
        self.assertIsInstance(result["response"], str)
        self.assertGreater(len(result["response"]), 5)

        # Peek at the response
        print("Test - Employee answer flow answer: ", result["response"])

    def test_get_query_dict(self):
        """
        Test that the model is able to construct correct dictionary for data fetch
        """
        question = (
            "Who works in Finland department of Joo Tech and is over 30 years old"
        )
        result = get_query_dict(OPENAI_CLIENT, question, EmployeeQuery)
        self.assertDictEqual(
            {
                "country": "Finland",
                "corporation": "Joo Tech",
                "filters": {"age_1": 30, "age_2": None},
            },
            result,
        )
