import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--file_name', default=None, type=str)

    parser_argumentss = parser.parse_args()
    
    return parser_argumentss