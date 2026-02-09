import pandas
from typing import Optional, List
import re

OPERATIONS = {"+", "-", "*"}
_OPERATIONS_TO_PARSE = re.compile(
    "(" + "|".join(re.escape(operator) for operator in OPERATIONS) + ")"
)

def check_column_name(name: str) -> bool: 
    if not name or not all(char.isalpha() or char == "_" for char in name):
        return False
    
    return True


def parse_role(role: str) -> Optional[List[str]]:
    elements = re.split(_OPERATIONS_TO_PARSE, role)
    elements = [e.strip() for e in elements]

    if not elements or len(elements) % 2 == 0 or any(e == "" for e in elements):
        return None
    
    for i in range(0, len(elements), 2):
        if not check_column_name(elements[i]):
            return None

    for i in range(1, len(elements), 2):
        if elements[i] not in OPERATIONS:
            return None
    
    return elements


def add_virtual_column(df: pandas.DataFrame, role: str, new_column: str) -> pandas.DataFrame:
    new_column = new_column.strip()
    if not check_column_name(new_column):
        return pandas.DataFrame([])
    
    elements = parse_role(role)
    if not elements:
        return pandas.DataFrame([])
    
    for i in range(0, len(elements), 2):
        if elements[i] not in df.columns:
            return pandas.DataFrame([])

    expression = " ".join(elements)
        
    new_df = df.copy()
    try:
        new_df[new_column] = new_df.eval(expression, engine="python")
    except Exception:
        return pandas.DataFrame([])

    return new_df