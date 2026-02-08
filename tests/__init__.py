from unittest import TestCase


class AIBaseTCase(TestCase):
    @staticmethod
    def patch_tool_fetch(tool_map, tool_name, fake_data):
        original = tool_map[tool_name]
        return (
            original[0],
            lambda _: fake_data,
            original[2],
            original[3],
        )
