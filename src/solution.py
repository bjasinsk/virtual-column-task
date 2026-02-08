import pandas
from typing import Optional, List
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


def parse_role(role: str) -> Optional[List[str]]:
    elements = re.split(r'(\+|\-|\*)', role)
    if len(elements) != 3:
        return None
    
    elements = [e.strip() for e in elements]
    
    first_column, operator, second_column = elements
    if not check_column_name(first_column) or not check_column_name(second_column):
        return None

    if operator not in OPERATIONS:
        return None
    
    return first_column, operator, second_column


def add_virtual_column(df: pandas.DataFrame, role: str, new_column: str) -> pandas.DataFrame:
    if not check_column_name(new_column):
        return pandas.DataFrame([])
    
    elements = parse_role(role)
    if not elements:
        return pandas.DataFrame([])
    
    first_column, operator, second_column = elements

    if first_column not in df.columns or second_column not in df.columns:
        return pandas.DataFrame([])
        
    new_df = df.copy()
    new_df[new_column] = OPERATIONS[operator](new_df[first_column], new_df[second_column])

    return new_df