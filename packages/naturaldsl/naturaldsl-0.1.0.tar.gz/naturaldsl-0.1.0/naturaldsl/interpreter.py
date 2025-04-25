import dask.dataframe as dd
import pandas as pd
import numpy as np
from datetime import datetime
from lark import Transformer

class NaturalDSLInterpreter(Transformer):
    def __init__(self):
        self.df = None

    def load(self, args):
        filename = args[0].strip('"')
        if filename.endswith('.parquet'):
            self.df = dd.read_parquet(filename)
        else:
            self.df = dd.read_csv(filename)
        print(f"Loaded {filename}")

    def merge(self, args):
        filename = args[0].strip('"')
        on_column = args[1].strip('"')
        if filename.endswith('.parquet'):
            new_df = dd.read_parquet(filename)
        else:
            new_df = dd.read_csv(filename)
        self.df = dd.merge(self.df, new_df, on=on_column, how='inner')
        print(f"Merged {filename} on {on_column}")

    def drop_missing(self, args):
        column_name = args[0].strip('"')
        self.df = self.df.dropna(subset=[column_name])
        print(f"Dropped rows where {column_name} is missing")

    def drop_col(self, args):
        column_name = args[0].strip('"')
        self.df = self.df.drop(columns=[column_name])
        print(f"Dropped column {column_name}")

    def fillna(self, args):
        column_name = args[0].strip('"')
        value = args[1]
        self.df[column_name] = self.df[column_name].fillna(value)
        print(f"Filled missing values in {column_name} with {value}")

    def rename(self, args):
        old_name = args[0].strip('"')
        new_name = args[1].strip('"')
        self.df = self.df.rename(columns={old_name: new_name})
        print(f"Renamed column {old_name} to {new_name}")

    def sort(self, args):
        column_name = args[0].strip('"')
        order = True if len(args) < 2 or args[1] == 'ascending' else False
        self.df = self.df.sort_values(by=column_name, ascending=order)
        print(f"Sorted by {column_name} in {'ascending' if order else 'descending'} order")

    def groupby(self, args):
        column_name = args[0].strip('"')
        agg_func = args[1].strip('"')
        if agg_func == 'sum':
            self.df = self.df.groupby(column_name).sum()
        elif agg_func == 'mean':
            self.df = self.df.groupby(column_name).mean()
        elif agg_func == 'count':
            self.df = self.df.groupby(column_name).count()
        print(f"Grouped by {column_name} and calculated {agg_func}")

    def filter(self, args):
        column_name = args[0].strip('"')
        operator = args[1]
        value = args[2]
        if operator == '>':
            self.df = self.df[self.df[column_name] > value]
        elif operator == '<':
            self.df = self.df[self.df[column_name] < value]
        elif operator == '==':
            self.df = self.df[self.df[column_name] == value]
        elif operator == '!=':
            self.df = self.df[self.df[column_name] != value]
        elif operator == '>=':
            self.df = self.df[self.df[column_name] >= value]
        elif operator == '<=':
            self.df = self.df[self.df[column_name] <= value]
        print(f"Filtered rows where {column_name} {operator} {value}")

    def convert(self, args):
        column_name = args[0].strip('"')
        to_type = args[1].strip('"')
        if to_type == 'datetime':
            self.df[column_name] = dd.to_datetime(self.df[column_name])
        elif to_type == 'number':
            self.df[column_name] = dd.to_numeric(self.df[column_name], errors='coerce')
        elif to_type == 'string':
            self.df[column_name] = self.df[column_name].astype(str)
        print(f"Converted column {column_name} to {to_type}")

    def create(self, args):
        new_column_name = args[0].strip('"')
        column1 = args[1]
        operator = args[2]
        column2 = args[3]
        if operator == '+':
            self.df[new_column_name] = self.df[column1] + self.df[column2]
        elif operator == '-':
            self.df[new_column_name] = self.df[column1] - self.df[column2]
        elif operator == '*':
            self.df[new_column_name] = self.df[column1] * self.df[column2]
        elif operator == '/':
            self.df[new_column_name] = self.df[column1] / self.df[column2]
        print(f"Created new column {new_column_name} as {column1} {operator} {column2}")

    def save(self, args):
        filename = args[0].strip('"')
        if filename.endswith('.parquet'):
            self.df.to_parquet(filename, write_options={'compression': 'snappy'})
        else:
            self.df.to_csv(filename, index=False)
        print(f"Saved dataset as {filename}")
