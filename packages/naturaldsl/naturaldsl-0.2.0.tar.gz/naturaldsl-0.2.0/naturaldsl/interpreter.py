import dask.dataframe as dd
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from lark import Transformer


# DataLoader class for loading and saving data
class DataLoader:
    def __init__(self):
        self.df = None

    def load(self, filename):
        """Load a CSV or Parquet file into a dataframe."""
        if filename.endswith('.parquet'):
            self.df = dd.read_parquet(filename)
        else:
            self.df = dd.read_csv(filename)
        print(f"Loaded {filename}")

    def save(self, filename):
        """Save dataframe to CSV or Parquet."""
        if filename.endswith('.parquet'):
            self.df.to_parquet(filename, write_options={'compression': 'snappy'})
        else:
            self.df.to_csv(filename, index=False)
        print(f"Saved dataset as {filename}")


# DataPreprocessing class for cleaning and manipulating data
class DataPreprocessing:
    def __init__(self, df):
        self.df = df

    def drop_missing(self, column):
        """Drop rows with missing values in a specific column."""
        self.df = self.df.dropna(subset=[column])
        print(f"Dropped rows where {column} is missing")

    def fill_missing(self, column, value):
        """Fill missing values in a specific column."""
        self.df[column] = self.df[column].fillna(value)
        print(f"Filled missing values in {column} with {value}")

    def rename(self, old_name, new_name):
        """Rename a column."""
        self.df = self.df.rename(columns={old_name: new_name})
        print(f"Renamed column {old_name} to {new_name}")

    def sort(self, column, order='ascending'):
        """Sort data by a column."""
        order_bool = True if order == 'ascending' else False
        self.df = self.df.sort_values(by=column, ascending=order_bool)
        print(f"Sorted by {column} in {order} order")

    def filter(self, column, operator, value):
        """Filter rows based on conditions."""
        if operator == '>':
            self.df = self.df[self.df[column] > value]
        elif operator == '<':
            self.df = self.df[self.df[column] < value]
        elif operator == '==':
            self.df = self.df[self.df[column] == value]
        elif operator == '!=':
            self.df = self.df[self.df[column] != value]
        elif operator == '>=':
            self.df = self.df[self.df[column] >= value]
        elif operator == '<=':
            self.df = self.df[self.df[column] <= value]
        print(f"Filtered rows where {column} {operator} {value}")


# DataTransformation class for reshaping and type conversion
class DataTransformation:
    def __init__(self, df):
        self.df = df

    def convert(self, column, to_type):
        """Convert a column to a specific data type."""
        if to_type == 'datetime':
            self.df[column] = dd.to_datetime(self.df[column])
        elif to_type == 'number':
            self.df[column] = dd.to_numeric(self.df[column], errors='coerce')
        elif to_type == 'string':
            self.df[column] = self.df[column].astype(str)
        elif to_type == 'int':
            self.df[column] = self.df[column].astype(int, errors='ignore')
        elif to_type == 'float':
            self.df[column] = self.df[column].astype(float, errors='ignore')
        print(f"Converted column {column} to {to_type}")

    def reshape_long_to_wide(self, id_vars, value_vars):
        """Reshape data from long format to wide format."""
        self.df = self.df.pivot_table(index=id_vars, columns=value_vars[0], values=value_vars[1])
        print(f"Reshaped data from long to wide using {id_vars} and {', '.join(value_vars)}")

    def reshape_wide_to_long(self, id_vars, value_vars):
        """Reshape data from wide format to long format."""
        self.df = self.df.melt(id_vars=id_vars, value_vars=value_vars)
        print(f"Reshaped data from wide to long using {id_vars} and {', '.join(value_vars)}")


# DataAggregation class for performing group-by and aggregation operations
class DataAggregation:
    def __init__(self, df):
        self.df = df

    def group_by(self, column, agg_func):
        """Group data by a column and aggregate."""
        if agg_func == 'sum':
            self.df = self.df.groupby(column).sum()
        elif agg_func == 'mean':
            self.df = self.df.groupby(column).mean()
        elif agg_func == 'count':
            self.df = self.df.groupby(column).count()
        print(f"Grouped by {column} and calculated {agg_func}")


# DataVisualization class for Seaborn plotting
class DataVisualization:
    @staticmethod
    def plot_bar(df, x_col, y_col):
        """Plot a barplot."""
        sns.barplot(x=x_col, y=y_col, data=df.compute())
        plt.show()
        print(f"Plotted barplot between {x_col} and {y_col}")

    @staticmethod
    def plot_scatter(df, x_col, y_col):
        """Plot a scatterplot."""
        sns.scatterplot(x=x_col, y=y_col, data=df.compute())
        plt.show()
        print(f"Plotted scatterplot between {x_col} and {y_col}")

    @staticmethod
    def plot_line(df, x_col, y_col):
        """Plot a lineplot."""
        sns.lineplot(x=x_col, y=y_col, data=df.compute())
        plt.show()
        print(f"Plotted lineplot between {x_col} and {y_col}")

    @staticmethod
    def plot_pairplot(df):
        """Generate pairplot."""
        sns.pairplot(df.compute())
        plt.show()
        print("Generated pairplot")

    @staticmethod
    def plot_heatmap(df):
        """Plot heatmap for correlation matrix."""
        corr = df.corr().compute()  # Ensure it's a pandas DataFrame
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.show()
        print(f"Plotted heatmap for correlation matrix")

    @staticmethod
    def plot_facetgrid(df, x_col, y_col):
        """Generate a FacetGrid plot."""
        sns.FacetGrid(df.compute(), col=x_col, row=y_col).map(sns.scatterplot)
        plt.show()
        print(f"Generated facet grid for {x_col} and {y_col}")


# Main interpreter class that integrates all components
class NaturalDSLInterpreter:
    def __init__(self):
        self.data_loader = DataLoader()
        self.data_preprocessing = None
        self.data_transformation = None
        self.data_aggregation = None
        self.data_visualization = DataVisualization()

    def load(self, filename):
        self.data_loader.load(filename)
        self.data_preprocessing = DataPreprocessing(self.data_loader.df)
        self.data_transformation = DataTransformation(self.data_loader.df)
        self.data_aggregation = DataAggregation(self.data_loader.df)

    def save(self, filename):
        self.data_loader.save(filename)

    def drop_missing(self, column):
        self.data_preprocessing.drop_missing(column)

    def fill_missing(self, column, value):
        self.data_preprocessing.fill_missing(column, value)

    def rename(self, old_name, new_name):
        self.data_preprocessing.rename(old_name, new_name)

    def sort(self, column, order='ascending'):
        self.data_preprocessing.sort(column, order)

    def filter(self, column, operator, value):
        self.data_preprocessing.filter(column, operator, value)

    def convert(self, column, to_type):
        self.data_transformation.convert(column, to_type)

    def reshape_long_to_wide(self, id_vars, value_vars):
        self.data_transformation.reshape_long_to_wide(id_vars, value_vars)

    def reshape_wide_to_long(self, id_vars, value_vars):
        self.data_transformation.reshape_wide_to_long(id_vars, value_vars)

    def group_by(self, column, agg_func):
        self.data_aggregation.group_by(column, agg_func)

    def plot_bar(self, x_col, y_col):
        self.data_visualization.plot_bar(self.data_loader.df, x_col, y_col)

    def plot_scatter(self, x_col, y_col):
        self.data_visualization.plot_scatter(self.data_loader.df, x_col, y_col)

    def plot_line(self, x_col, y_col):
        self.data_visualization.plot_line(self.data_loader.df, x_col, y_col)

    def plot_pairplot(self):
        self.data_visualization.plot_pairplot(self.data_loader.df)

    def plot_heatmap(self):
        self.data_visualization.plot_heatmap(self.data_loader.df)

    def plot_facetgrid(self, x_col, y_col):
        self.data_visualization.plot_facetgrid(self.data_loader.df, x_col, y_col)


# Example usage
interpreter = NaturalDSLInterpreter()
interpreter.load("data.csv")  # Load your data
interpreter.plot_bar("column1", "column2")
interpreter.fill_missing("column1", 0)  # Fill missing values in column1 with 0
