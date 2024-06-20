import pytest
from integrations.api.views import FormResponseAPI

from src.tests.test_data_for_form_response import input_correct_data, input_data_without_question_name, \
    input_data_without_answer_values, input_empty_data, output_correct_data, output_empty_data, \
    output_data_without_question_name, output_data_without_answer_values


@pytest.mark.parametrize("input_data, expected_output", [
    (input_correct_data, output_correct_data),
    (input_data_without_question_name, output_data_without_question_name),
    (input_data_without_answer_values, output_data_without_answer_values),
    (input_empty_data, output_empty_data),
])
def test_my_function(input_data, expected_output):
    result = FormResponseAPI.get_str_form_response(input_data)
    assert result == expected_output
