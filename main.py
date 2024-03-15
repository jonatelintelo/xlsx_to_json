from argument_parser import parse_arguments

import pandas as pd
import json
import os

def is_list(df, row, column):
    return pd.isna(df.iloc[row, column+1]) \
            and pd.isna(df.iloc[row+1, column])

def get_list_items(df, column, old_row):
    result = dict()
    column_values = dict(df[column].dropna()) # {1: 'number', 2: 'source_system_code', 3: 'start_DateTime'}
    rows_with_values = list(column_values) # [1, 2, 3, 4, 5]
    for row in rows_with_values:
        if row > old_row and column + 1 != len(df.columns) and row + 1 != len(df[0]):
            if is_list(df, row, column):
                result[column_values[row]] = get_list_items(df, column+1, row)
            else:
                if not pd.isna(df.iloc[row, column+1]):
                    result[column_values[row]] = df.iloc[row, column+1]
    return [result]

def fill_dict(_dict, df):
    column = 0
    column_values = dict(df[column].dropna()) # {1: 'number', 2: 'source_system_code', 3: 'start_DateTime'}
    rows_with_values = list(column_values) # [1, 2, 3, 4, 5]
    for row in rows_with_values:
        if is_list(df, row, column):
            _dict[column_values[row]] = get_list_items(df, column+1, row)
        else:
            _dict[column_values[row]] = df.iloc[row, column+1]

    return _dict

if __name__ == "__main__":
    parser_arguments = parse_arguments()
    
    assert parser_arguments is not None, "Please provide a file path with script call."
    
    DATA_FILE_PATH = os.path.join('data', parser_arguments.file_name+'.xlsx')

    # print(FILE_PATH)

    df = pd.read_excel(DATA_FILE_PATH,header=None)

    result = dict()

    fill_dict(result, df)

    # print(result)
    # print(len(list(result.keys())))

    RESULT_FILE_PATH = os.path.join('result_json_files','result.json')

    with open(RESULT_FILE_PATH, 'w',encoding='utf8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("========== Job finished ==========")
