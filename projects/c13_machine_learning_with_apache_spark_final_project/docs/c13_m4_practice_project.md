# Practice Project: Create a Machine Learning Pipeline for a Regression Project

![IBM](../assets/ibm_logo.png)

**Estimated Study Time:** 225 mins (Deep Comprehension @ 2.5x) | Hands-on Lab Base: 90 mins

> **Source Notebook:** [`Practice_Project.ipynb`](Practice_Project.ipynb)  
> **Target Environment:** Python 3.x with `pyspark==3.1.2`, `findspark`  
> **Course / Module:** [Course 13](../../index.md) / [Module 4: Final Project and Assessment](../index.md)

---

## Scenario & Role Description

You are a **Data Engineer** at a data analytics consulting company. Your company prides itself on being able to efficiently handle huge datasets. Data scientists in your office need to work with different algorithms and data in different formats. While they are proficient at Machine Learning, they count on you to perform distributed ETL jobs and construct robust, automated ML pipelines.

---

## Lab Objectives

In this 4-part assignment, you will:

1. **Part 1: ETL Pipeline**
   - Ingest raw CSV data into a Spark DataFrame.
   - Profile record cardinality and handle duplicate rows.
   - Cleanse missing and null values.
   - Execute column renaming and schema standardization.
   - Persist the cleaned dataset in compressed columnar Parquet format.
2. **Part 2: Machine Learning Pipeline Creation**
   - Ingest cleaned Parquet data.
   - Stage 1: Categorical encoding with `StringIndexer`.
   - Stage 2: Feature vectorization with `VectorAssembler`.
   - Stage 3: Feature standardization with `StandardScaler`.
   - Stage 4: Supervised regression estimator with `LinearRegression`.
   - Pipeline DAG assembly and 70:30 train/test data splitting.
   - Fit pipeline to generate a production `PipelineModel`.
3. **Part 3: Model Evaluation**
   - Generate holdout test predictions.
   - Compute regression metrics using `RegressionEvaluator`: Mean Squared Error ($\text{MSE}$), Mean Absolute Error ($\text{MAE}$), and Coefficient of Determination ($R^2$).
   - Extract model parameters (intercept and feature coefficients).
4. **Part 4: Model Persistence & Deserialization**
   - Persist the fitted `PipelineModel` to disk for production serving.
   - Deserialize and reload the stored pipeline model via `PipelineModel.load()`.
   - Verify zero-drift out-of-sample inference on testing data.

---

## Datasets Overview

- **Dataset:** Modified Auto Miles Per Gallon (Auto MPG) dataset.
- **Original Source:** [UCI Machine Learning Repository - Auto MPG](https://archive.ics.uci.edu/ml/datasets/auto+mpg)
- **Direct Download URL:** `https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-BD0231EN-Coursera/datasets/mpg-raw.csv`
- **Features:** `MPG` (target continuous label), `Cylinders`, `Engine Disp`, `Horsepower`, `Weight`, `Accelerate`, `Year`, `Origin`.

---

## Environment Setup & Initialization

```bash
!pip install pyspark==3.1.2 -q
!pip install findspark -q
```

```python
# Warning suppression
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')

# Initialize findspark
import findspark
findspark.init()
```

---

## Part 1: Distributed ETL Pipeline

### Task 1: Import Required Libraries

```python
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.pipeline import PipelineModel
from pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
```

### Task 2: Create SparkSession

```python
spark = SparkSession.builder.appName("Practice Project").getOrCreate()
```

### Task 3: Ingest Raw CSV Dataset

```python
# Download dataset
!wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-BD0231EN-Coursera/datasets/mpg-raw.csv

# Ingest into Spark DataFrame
df = spark.read.csv("mpg-raw.csv", header=True, inferSchema=True)
```

### Task 4: Inspect Top 5 Records

```python
df.show(5)
```

### Task 5: Profile Origin Distribution

```python
# Group by Origin and count occurrences ordered by frequency
df.groupBy('Origin').count().orderBy('count').show()
```

### Task 6: Audit Initial Row Count

```python
rowcount1 = df.count()
print("Initial row count:", rowcount1)
```

### Task 7: Deduplicate Records

```python
# Drop duplicate rows
df = df.dropDuplicates()
```

### Task 8: Audit Row Count After Deduplication

```python
rowcount2 = df.count()
print("Row count after deduplication:", rowcount2)
```

### Task 9: Drop Rows with Null / Missing Values

```python
# Purge missing values
df = df.dropna()
```

### Task 10: Audit Row Count After Null Removal

```python
rowcount3 = df.count()
print("Row count after dropping nulls:", rowcount3)
```

### Task 11: Rename Feature Columns

```python
# Rename "Engine Disp" to standardized column name "Engine_Disp"
df = df.withColumnRenamed("Engine Disp", "Engine_Disp")
```

### Task 12: Persist Cleaned Dataset to Parquet

```python
# Save DataFrame to Parquet format in overwrite mode
df.write.mode("overwrite").parquet("mpg-cleaned.parquet")
```

### Part 1: Automated Verification Block

```python
print("Part 1 - Evaluation")
print("Total rows =", rowcount1)
print("Total rows after dropping duplicate rows =", rowcount2)
print("Total rows after dropping duplicate rows and rows with null values =", rowcount3)
print("Renamed column name =", df.columns[2])

import os
print("mpg-cleaned.parquet exists :", os.path.isdir("mpg-cleaned.parquet"))
```

---

## Part 2: Machine Learning Pipeline Creation

### Task 1: Load Cleaned Parquet Dataset

```python
df = spark.read.parquet("mpg-cleaned.parquet")
rowcount4 = df.count()
df.show(5)
df.printSchema()
```

### Task 2: Define Stage 1 — Categorical `StringIndexer`

```python
# Stage 1: Convert categorical string column "Origin" to numerical "OriginIndex"
indexer = StringIndexer(inputCol="Origin", outputCol="OriginIndex")
```

### Task 3: Define Stage 2 — Feature `VectorAssembler`

```python
# Stage 2: Assemble numerical predictors and indexed origin into a single feature vector
assembler = VectorAssembler(
    inputCols=['Cylinders', 'Engine_Disp', 'Horsepower', 'Weight', 'Accelerate', 'Year', 'OriginIndex'],
    outputCol="features"
)
```

### Task 4: Define Stage 3 — Feature `StandardScaler`

```python
# Stage 3: Standardize feature distributions (zero mean, unit variance)
scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures")
```

### Task 5: Define Stage 4 — Linear Regression Estimator

```python
# Stage 4: Linear regression estimator predicting continuous target "MPG"
lr = LinearRegression(featuresCol="scaledFeatures", labelCol="MPG")
```

### Task 6: Assemble Pipeline DAG

```python
# Build multi-stage pipeline
pipeline = Pipeline(stages=[indexer, assembler, scaler, lr])
```

### Task 7: Train / Test Split (70:30)

```python
# Split dataset with reproducible seed
(trainingData, testingData) = df.randomSplit([0.7, 0.3], seed=42)
```

### Task 8: Fit Pipeline on Training Data

```python
# Execute fit on training split to generate PipelineModel
pipelineModel = pipeline.fit(trainingData)
```

### Part 2: Automated Verification Block

```python
print("Part 2 - Evaluation")
print("Total rows =", rowcount4)
ps = [str(x).split("_")[0] for x in pipeline.getStages()]

print("Pipeline Stage 1 =", ps[0])
print("Pipeline Stage 2 =", ps[1])
print("Pipeline Stage 3 =", ps[2])
print("Pipeline Stage 4 =", ps[3])

print("Label column =", lr.getLabelCol())
```

---

## Part 3: Model Evaluation

### Task 1: Generate Predictions on Holdout Test Data

```python
# Apply fitted pipeline model to transform testing data
predictions = pipelineModel.transform(testingData)
```

### Task 2: Calculate Mean Squared Error ($\text{MSE}$)

$$\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

```python
evaluator_mse = RegressionEvaluator(predictionCol="prediction", labelCol="MPG", metricName="mse")
mse = evaluator_mse.evaluate(predictions)
print("Mean Squared Error (MSE):", mse)
```

### Task 3: Calculate Mean Absolute Error ($\text{MAE}$)

$$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i|$$

```python
evaluator_mae = RegressionEvaluator(predictionCol="prediction", labelCol="MPG", metricName="mae")
mae = evaluator_mae.evaluate(predictions)
print("Mean Absolute Error (MAE):", mae)
```

### Task 4: Calculate Coefficient of Determination ($R^2$)

$$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$

```python
evaluator_r2 = RegressionEvaluator(predictionCol="prediction", labelCol="MPG", metricName="r2")
r2 = evaluator_r2.evaluate(predictions)
print("R-Squared (R2):", r2)
```

### Part 3: Automated Verification Block

```python
print("Part 3 - Evaluation")
print("Mean Squared Error =", round(mse, 2))
print("Mean Absolute Error =", round(mae, 2))
print("R Squared =", round(r2, 2))

lrModel = pipelineModel.stages[-1]
print("Intercept =", round(lrModel.intercept, 2))
```

---

## Part 4: Model Persistence & Deserialization

### Task 1: Persist Fitted PipelineModel to Disk

```python
# Save pipeline model artifact to local storage
pipelineModel.write().overwrite().save("Practice_Project")
```

### Task 2: Deserialize and Load Stored Model

```python
# Load persisted pipeline model from storage
loadedPipelineModel = PipelineModel.load("Practice_Project")
```

### Task 3: Generate Predictions Using Loaded Model

```python
# Score holdout testing data with loaded model
predictions_loaded = loadedPipelineModel.transform(testingData)
```

### Task 4: Display Predicted vs Actual Values

```python
# Show sample predictions
predictions_loaded.select("MPG", "prediction").show(10)
```

### Part 4: Automated Verification Block

```python
print("Part 4 - Evaluation")

loadedmodel = loadedPipelineModel.stages[-1]
totalstages = len(loadedPipelineModel.stages)
inputcolumns = loadedPipelineModel.stages[1].getInputCols()

print("Number of stages in the pipeline =", totalstages)
for col_name, coef in zip(inputcolumns, loadedmodel.coefficients):
    print(f"Coefficient for {col_name} is {round(coef, 4)}")
```

### Task 5: Terminate SparkSession

```python
# Stop active SparkSession
spark.stop()
```

---

## Practice Project Summary & Architectural Highlights

```mermaid
flowchart LR
    A["mpg-raw.csv"] -->|ETL Cleansing| B["mpg-cleaned.parquet"]
    B --> C["randomSplit(0.7, 0.3)"]
    C --> D["Training Data"]
    C --> E["Testing Data"]
    D --> F["Pipeline.fit()"]
    subgraph SparkML_Pipeline["SparkML Pipeline DAG"]
        S1["StringIndexer ('Origin')"] --> S2["VectorAssembler (7 Features)"]
        S2 --> S3["StandardScaler"]
        S3 --> S4["LinearRegression ('MPG')"]
    end
    F --> G["PipelineModel"]
    G -->|Persistence| H["write().save('Practice_Project')"]
    H -->|Deserialization| I["PipelineModel.load()"]
    I -->|transform()| J["Regression Metrics<br/>(MSE, MAE, R²)"]
```

1. **Integrated Data Engineering & Machine Learning:** Demonstrated seamless data flow from raw, uncurated CSVs through Spark SQL transformations, columnar Parquet persistence, and multi-stage MLlib pipeline training.
2. **Deterministic Preprocessing:** Encapsulated `StringIndexer`, `VectorAssembler`, and `StandardScaler` inside a single `Pipeline` object to ensure test datasets undergo identical mathematical transformations without data leakage.
3. **Model Persistence Compliance:** Verified that serialized `PipelineModel` objects preserve both preprocessing transformer parameters and fitted regression weights for zero-downtime serving.

---

## Authors & Acknowledgments

- **Author:** [Ramesh Sannareddy](https://www.linkedin.com/in/rsannareddy/) (IBM Corporation)
- **Copyright:** © IBM Corporation. All rights reserved.
