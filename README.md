# 🌱 Master's Degree Project: Kinship Rules and Agrobiodiversity of Manioc
## 📖 Introduction
Welcome to the repository for my Master's Degree Project! This project explores the effect of kinship rules and the inheritance of plants on the agrobiodiversity of manioc. It includes several components to simulate the reproduction of Unidades Domésticas (UD) or Households (HD) and the inheritance of manioc varieties, along with validations to ensure model accuracy.

Before running the project, install the required dependencies listed in the requirements.txt file. You can do this by running the following command:


pip install -r requirements.txt

📂 The literature folder contains valuable data and references about manioc diversity in traditional communities. This resource provides crucial context for understanding the project.

## 🚀 Running the Model or Validations
To run the model or perform validation checks, execute the main.py file. Instructions for running the model and validations are included directly in the main.py file.

🛠️ Main Components:
Experiments:

1. Effect of kinship rules and inheritance of plants in agrobiodiversity
2. Effect of different parameters on agrobiodiversity 

Validation:

1. Populational behavior
2. Kinship systems


Simply go to the Main folder and run the main.py file as follows:

py main.py

## 📂 Folder Structure
Here's a quick overview of the repository's organization:


├── Literature -------> Literature folder. There we have a revision on diversity of manioc. As you may see, there is no data available! We may publish the systematic revision version of that topic soon.

├── Main/ ----------------------------> Core simulation scripts and outputs.

│------├── Outputs/ ---------------------> Directory storing the results produced by the experiments (e.g., figures, data exports).

│------├── Experiment_1.py --------------> Script defining the configuration and execution of the first experimental setup.

│------├── Experiment_2.py --------------> Script for the second experimental configuration, exploring different parameters or scenarios.

│------├── Main.py ----------------------> Central entry point for running the model and coordinating different components.

│------└── Validation kinship systems.py -> Script focused on the validation of the model.

├── model_class ------> Classes of the model.

├── to_get_data ------> Methods used to get data in some points of the model. Some were not used.

└── README.md --------> Project documentation (this file)
