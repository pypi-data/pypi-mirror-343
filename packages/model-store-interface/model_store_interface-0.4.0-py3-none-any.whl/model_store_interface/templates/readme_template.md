# model-store-interface

Repository: [GitHub](https://github.com/synthema-project/app-model_store-interface)

# **Upload a Federated Learning Model to the Federated Platform**

This library provides utilities for creating, managing, and registering federated learning models to the Federated Platform. It encapsulates a local learner and an aggregator into a single FederatedModel object and provides a function to register the model in a Federated Platform Model Catalogue with appropriate credentials and metadata.

The package uses the following libraries internally:
- `MLflow`: For model tracking and registry. More information can be found [here](https://mlflow.org/).
- `Flower`: For federated learning framework. More information can be found [here](https://flower.dev/).
The user needs do work with objects originating from these libraries to upload a Federated Model.

---

## **Features provided by the package**

- **Create a custom FederatedModel**:
  - Create a local learner, a ML model that will be executed on edge nodes with custom training, evaluation, and parameter management methods.
  - Define and integrate your custom aggregation strategy, with a default implementation of plain averaging (DefaultAggregator) for both parameters and metrics.

- **Upload it to the Model Catalogue of the Federated Platform**:
  - Log the FL Model and its metadata to the Federated Platform using the `submit_fl_model` method.


---

# **Walkthrough: How to Implement a Federated Model**

### **Step 1: Define Your Local Learner**

To create a custom local learner, implement your model according to the `LLProtocol`. Your model class should have the following structure:

#### **Methods**
- **`prepare_data(data: pd.DataFrame) -> None`**:  
  - **Purpose**: Prepares the input data for training or evaluation.
  - **Arguments**:
    - `data`: A pandas DataFrame containing the input data.
  - **Returns**: None.

- **`train_round() -> flwr.common.MetricsRecord`**:  
  - **Purpose**: Performs the training process for the local learner.
  - **Arguments**: None.
  - **Returns**: A `flwr.common.MetricsRecord` containing metrics collected during training.

- **`get_parameters() -> flwr.common.ParametersRecord`**:  
  - **Purpose**: Retrieves the model's current parameters for aggregation.
  - **Arguments**: None.
  - **Returns**: A `flwr.common.ParametersRecord` representing the current model parameters.

- **`set_parameters(parameters: flwr.common.ParametersRecord) -> None`**:  
  - **Purpose**: Updates the model's parameters with the provided values.
  - **Arguments**:
    - `parameters`: A `flwr.common.ParametersRecord` containing the parameters to be set.
  - **Returns**: None.

- **`evaluate() -> flwr.common.MetricsRecord`**:  
  - **Purpose**: Evaluates the model's performance on validation or test data.
  - **Arguments**: None.
  - **Returns**: A `flwr.common.MetricsR"https://github.com/synthema-project/app-model_store-interface"ecord` containing metrics from the evaluation.

**NB:** Any dependency needed alongside the model must be stored inside the `src/` directory and referenced from there.

---

### **Step 2: Incapsulate local learner into a function**

A function must be created according to the `LLFactoryProtocol`. The function must contain the definition of the model class and it must return an instance of the model itself. Also the function must import all the packages necessary to the local learner with the  `Lazy Imports` strategy. Here is an example:
```python
# Incapsulating function
def create_aggregator():
    import torch # import all the packages necessary to the local learner

    # Definition of the local learner as in step 1
    class CustomLocalLearner(nn.Module):
      '''Local learner according LLProtocol'''
      ...
  
    return CustomLocalLearner()
```


### **Step 3: Define Your Aggregation Strategy**

To implement a custom aggregation strategy, follow the `AggProtocol`. The strategy class should have the following structure: 


#### **Methods**
- **`aggregate_parameters(results: list[flwr.common.ParametersRecord], config: Optional[flwr.common.ConfigsRecord]=None) -> flwr.common.ParametersRecord`**:  
  - **Purpose**: Aggregates a list of parameter records from multiple clients into a single set of parameters.
  - **Arguments**:
    - `results`: A list of `flwr.common.ParametersRecord` objects, each representing the parameters from a client.
  - **Returns**: A `flwr.common.ParametersRecord` containing the aggregated parameters.

- **`aggregate_metrics(results: list[flwr.common.MetricsRecord], config: Optional[flwr.common.ConfigsRecord]=None) -> flwr.common.MetricsRecord`**:  
  - **Purpose**: Aggregates a list of metrics records from multiple clients into a single set of metrics.
  - **Arguments**:
    - `results`: A list of `flwr.common.MetricsRecord` objects, each representing the metrics from a client.
  - **Returns**: A `flwr.common.MetricsRecord` containing the aggregated metrics.

---

### **Step 4: Incapsulate local learner into function**

As for the local learner,a function must be created according to the `AggFactoryProtocol`. The function must contain the definition of the aggregator class and it must return an instance of the aggregator itself. Also the function must import all the packages necessary to the class with the  `Lazy Imports` strategy. Here is an example:
```python
# Incapsulating function
def create_aggregator():
    import numpy as np # import all the packages necessary to the aggregator

    # Definition of the aggregator as in step 3
    class CustomAggregator():
      '''Aggregator according AggProtocol'''
      ...
  
    return CustomAggregator()
```

## **Step 5: Create the FederatedModel to include both local learner and aggregator**
The local learner and the aggregator must be included in the same FederatedModel class. The model-store-interface package provides the FederatedModelclass which recieves as arguments the function creating the local learner and the function creating the aggregator with their respective names. If no aggregation strategy is provided, the model will by default use a plain averaging strategy for both parameters and metrics, and if also the local learner is not provided the model will get a default local learner which is shown in `example.py`. Here is an example of how to set up the FederatedModel:
```python
from model_store_interface import FederatedModel

# Define your local learner and aggregator
def create_local_learner():
    '''Create local learner according to LLProtocol'''
    return CustomLocalLearner()
    

def create_aggregator():
    '''Create aggregator according to AggProtocol'''
    return CustomAggregator()

# Create the FederatedModel
federated_model = FederatedModel(create_local_learner=create_local_learner,
                           model_name="your_model_name",
                           create_saggregator=create_aggregator,
                           aggregator_name="your_aggregator_name")
```

**NB:** Make sure your model and aggregation strategy are compatible with static type checking tools like MyPy. This will help catch any issues related to the implementation of the protocols.


### **Step 6: Submit the model to the Platform Model Catalogue**
Upload the model created with the submit_fl_model function provided by the package. To successfully upload the model the user must provide to the function the platform url to which upload the model, a valid set of username and password, the name of the experiment (if it doesn't exist already a new experiment is created with that name) and some tags related to the model the user is uploading. Here is an example:

```python
from model_store_interface import submit_fl_model

# Submit the FederatedModel to the Platform
submit_fl_model(federated_model, 
                platform_url="platform_model_registry_url"
                username="your_username", 
                password="your_password",
                experiment_name="your_experiment_name",
                disease="your_disease", # The use case the model is used for ("AML" or "SCD")
                trained=False) # Whether the local learner is trained or not
```
---

### **Example Included**

An example is included in the `example.py` script, demonstrating how to compile and use the provided methods to implement and log an FL model. The example provides clear documentation on how to define the local learner and aggregation strategy, and how to log the model to the Platform model catalogue. Local learner and aggregation strategy defined in this example script are the same default elements the class FederatedModel gets if the user is not providing any.
To run the example code you need to install pytorch library, you can find it at this link: https://pytorch.org/get-started/locally/
