
# **NaturalDSL: Documentation**

## **Overview**

**NaturalDSL** is a human-first, natural programming language designed for data science. It abstracts away the complexity of traditional programming languages while providing powerful tools for data manipulation, visualization, and analysis. With seamless integration of **Pandas**, **Numpy**, **Seaborn**, **Matplotlib**, and **Dask**, **NaturalDSL** offers intuitive commands for handling common data analysis tasks.

## **Core Features**
- **Human-Readable Syntax**: Use natural language constructs for common data science tasks.
- **Data Manipulation**: Load, clean, transform, and aggregate data.
- **Data Visualization**: Simple, intuitive plotting commands using Seaborn and Matplotlib.
- **Parallel Computing**: Handle large datasets with Dask.
- **Extensibility**: Easily extendable through plugins.
- **AI Integration**: Code autocompletion for frequent data science tasks.

---

## **Getting Started**

### **System Requirements**
- Python 3.7 or higher
- Pip for managing packages

### **Installation**

To install **NaturalDSL**, use the following steps:

1. Clone the repository (if you haven't done so yet):

```bash
git clone https://github.com/pradumana/naturaldsl.git
cd naturaldsl
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Install globally from PyPI:

```bash
pip install naturaldsl
```

---

## **CLI Usage**

### **Basic Command Syntax**

```bash
[COMMAND] [OPTIONS]
```

Here’s a summary of the most common commands for data analysis using **NaturalDSL**:

### **1. Loading Data**

Load your data from CSV or Parquet files:

```bash
load data.csv
```

This command loads the data into **NaturalDSL** for further processing.

### **2. Data Cleaning**

- **Drop rows with missing values in a specific column**:

```bash
drop_missing age
```

- **Fill missing values in a specific column with a constant value**:

```bash
fill_missing age 0
```

### **3. Data Transformation**

- **Rename a column**:

```bash
rename old_name new_name
```

- **Sort data by a column**:

```bash
sort age descending
```

- **Convert a column to a specific data type (e.g., datetime)**:

```bash
convert date_column datetime
```

### **4. Grouping and Aggregation**

Group data by a specific column and apply an aggregation (e.g., sum, average):

```bash
group_by age sum
```

### **5. Data Visualization**

- **Generate a bar plot** between two columns:

```bash
plot_bar age salary
```

- **Generate a scatter plot** between two columns:

```bash
plot_scatter age salary
```

### **6. Save Data**

Save the processed data to a new file:

```bash
save cleaned_data.csv
```

---

## **Example CLI Session**

Here’s an example session showing common data analysis steps:

```bash
load data.csv
drop_missing age
rename old_column new_column
sort age descending
group_by age mean
plot_scatter age salary
save cleaned_data.csv
```

This series of commands loads a dataset, cleans it, performs some transformations, generates a plot, and saves the cleaned data to a new file.

---

## **Advanced Features**

### **Multiple Command Chaining**

You can chain multiple commands in a single line to improve your workflow:

```bash
load data.csv && drop_missing age && plot_scatter age salary
```

### **Plot Customization**

Customize the appearance of your plots, such as colors, labels, and titles, directly from the CLI. You could, for example, modify the color of a scatter plot:

```bash
plot_scatter age salary --color blue
```

---

## **Python API Usage**

You can also use **NaturalDSL** in Python scripts for more control and flexibility.

### **Basic API Workflow**

```python
from natural_dsl_interpreter import NaturalDSLInterpreter

# Initialize the interpreter
interpreter = NaturalDSLInterpreter()

# Load data
interpreter.load("data.csv")

# Clean data
interpreter.drop_missing("age")
interpreter.fill_missing("age", 0)

# Transform data
interpreter.rename("old_column", "new_column")
interpreter.sort("age", ascending=False)

# Group and aggregate
interpreter.group_by("age", "sum")

# Visualize data
interpreter.plot_bar("age", "salary")

# Save data
interpreter.save("cleaned_data.csv")
```

---

## **Extending NaturalDSL**

### **Creating Custom Functions**

You can extend **NaturalDSL** by adding custom functions for specific use cases. Here’s an example:

1. Define a custom function:

```python
def custom_mean(dataframe, column):
    return dataframe[column].mean()
```

2. Register the custom function with the interpreter:

```python
interpreter.register_function("custom_mean", custom_mean)
```

### **Using Plugins**

You can extend **NaturalDSL** by creating plugins for additional features like new plotting methods, data sources, or algorithms. Once a plugin is created, you can load it using the CLI or Python API.

---

## **Contributing**

We encourage contributions from the community! To contribute:

1. Fork the repository on GitHub.
2. Clone your fork and create a new branch:

```bash
git checkout -b feature-branch
```

3. Make your changes, commit, and push them:

```bash
git commit -m "Added new feature"
git push origin feature-branch
```

4. Open a pull request to merge your changes into the main repository.

---

## **License**

**NaturalDSL** is licensed under the MIT License. See the LICENSE file for more details.

---

## **Contact**

For more information or questions, please contact me at:

**Email**: prdmn.shrm@gmail.com



