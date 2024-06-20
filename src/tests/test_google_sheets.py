import pytest

from integrations.service.google_sheet_integration import insert_data_by_stage

from src.tests.test_data_for_google_sheets import test_base_model, \
    expected_output_for_P5, \
    expected_output_for_P15, expected_output_for_P17, expected_output_for_other, \
    test_base_model_invalid, test_base_model_for_P5, test_base_model_for_P15, test_base_model_for_P17, \
    expected_output_invalid_lead, test_base_model_empty, test_base_model_empty_output, test_base_model_empty_invalid, \
    test_base_model_empty_invalid_output


@pytest.mark.parametrize("deal_info, expected_output", [
    (test_base_model_invalid, expected_output_invalid_lead),
    (test_base_model_for_P5, expected_output_for_P5),
    (test_base_model_for_P15, expected_output_for_P15),
    (test_base_model_for_P17, expected_output_for_P17),
    (test_base_model, expected_output_for_other),
    (test_base_model_empty, test_base_model_empty_output),
    (test_base_model_empty_invalid, test_base_model_empty_invalid_output),
])
def test_insert_data_by_stage(deal_info, expected_output):
    print(f"INVALID MODEL ----->>>  {test_base_model_invalid}")
    assert insert_data_by_stage(deal_info) == expected_output
