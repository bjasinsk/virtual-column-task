import pandas as pd
from src.solution import add_virtual_column


def test_sum_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 2]] * 2, columns = ["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one+label_two", "label_three")
    assert df_result.equals(df_expected), f"The function should sum the columns: label_one and label_two.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_multiplication_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 1]] * 2, columns = ["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one * label_two", "label_three")
    assert df_result.equals(df_expected), f"The function should multiply the columns: label_one and label_two.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_subtraction_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 0]] * 2, columns = ["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one - label_two", "label_three")
    assert df_result.equals(df_expected), f"The function should subtract the columns: label_one and label_two.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_empty_result_when_invalid_labels():
    df = pd.DataFrame([[1, 2]] * 3, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one + label_two", "label3")
    assert df_result.empty, f"Should return an empty df when the \"new_column\" is invalid.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"


def test_empty_result_when_invalid_rules():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, "label&one + label_two", "label_three")
    assert df_result.empty, f"Should return an empty df when the role have invalid character: '&'.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"
    df_result = add_virtual_column(df, "label_five + label_two", "label_three")
    assert df_result.empty, f"Should return an empty df when the role have a column which isn't in the df: 'label_five'.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"


def test_when_extra_spaces_in_rules():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 2]] * 2, columns = ["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one + label_two ", "label_three")
    assert df_result.equals(df_expected), f"Should work when the role have spaces between the operation and the column.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"
    df_result = add_virtual_column(df, "  label_one + label_two ", "label_three")
    assert df_result.equals(df_expected), f"Should work when the role have extra spaces in the start/end.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_incomplete_expression_in_role():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one + label_two -", "label_three")
    assert df_result.empty, f"If the expression in role is invalid, the function returns an empty df"


def test_empty_expression_in_role():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, " ", "label_three")
    assert df_result.empty, f"If the expression in role is empty, the function returns an empty df"


def test_wrong_order_of_expression_in_role():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one label_two +", "label_three")
    assert df_result.empty, f"If the order of expression is wrong, the function returns an empty df"


def test_expression_with_multiple_operators():
    df = pd.DataFrame([[1, 2, 3]] * 2, columns = ["label_one", "label_two", "label_three"])
    df_expected = pd.DataFrame([[1, 2, 3, 0]] * 2, columns = ["label_one", "label_two", "label_three", "label_four"])
    df_result = add_virtual_column(df, "label_one+label_two-label_three", "label_four")
    assert df_result.equals(df_expected), f"The function should sum the columns: label_one and label_two and then subtract column: label_three \n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_order_of_operations_add_multiply():
    df = pd.DataFrame([[1, 2, 3, 2]] * 2, columns = ["label_one", "label_two", "label_three", "label_four"])
    df_expected = pd.DataFrame([[1, 2, 3, 2, 7]] * 2, columns = ["label_one", "label_two", "label_three", "label_four", "label_five"])
    df_result = add_virtual_column(df, "label_one+label_three * label_four", "label_five")
    assert df_result.equals(df_expected), f"The function should first multiply label_three and label_fice and after this add label_one \n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_order_of_operations_subtract_multiply():
    df = pd.DataFrame([[1, 2, 3, 2]] * 2, columns = ["label_one", "label_two", "label_three", "label_four"])
    df_expected = pd.DataFrame([[1, 2, 3, 2, -5]] * 2, columns = ["label_one", "label_two", "label_three", "label_four", "label_five"])
    df_result = add_virtual_column(df, "label_one - label_three*label_four", "label_five")
    assert df_result.equals(df_expected), f"The function should first multiply label_three and label_fice and after this subtract label_one \n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"


def test_empty_new_column():
    df = pd.DataFrame([[1, 1]] * 2, columns = ["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one - label_two", " ")
    assert df_result.empty, f"If the name of new column is empty, the function returns an empty df"