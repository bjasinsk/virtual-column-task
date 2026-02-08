import pandas
from typing import List
import re

OPERATIONS = {
    "+": lambda c1, c2: c1 + c2,
    "-": lambda c1, c2: c1 - c2,
    "*": lambda c1, c2: c1 * c2,
}


def check_column_name(name: str) -> bool:
    if not all(char.isalpha() or char == "_" for char in name):
        return False
    return True


def parse_role(role: str) -> List:
    elements = re.split(r'(\+|\-|\*)', role)
    if len(elements) != 3:
        return None
    
    elements = [e.strip() for e in elements]

    first_column, operator, second_column = elements

    for column_name in [first_column, second_column]:
        if not check_column_name(column_name):
            return None

    if operator not in OPERATIONS:
        return None
    
    return elements


def add_virtual_column(df: pandas.DataFrame, role: str, new_column: str) -> pandas.DataFrame:
    if not check_column_name(new_column):
        return pandas.DataFrame([])
    
    new_df = df.copy()
    elements = parse_role(role)

    if not elements:
        return pandas.DataFrame([])
        
    first_column, operator, second_column = elements

    if first_column in df and second_column in df:
        new_df[new_column] = OPERATIONS[operator](new_df[first_column], new_df[second_column])
    else:
        return pandas.DataFrame([])

    return new_df