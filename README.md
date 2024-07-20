# Loan Status Prediction App

## Overview

This project aims to develop a machine learning model to predict loan approval status based on various financial indicators. The project encompasses the entire workflow from data preprocessing, model selection, training, evaluation, to deployment, and building a user interface with Streamlit for real-time predictions.

## Approach

### Data Preprocessing

- **Data Cleaning**: Handling missing values, removing duplicates, and correcting data types.
- **Feature Engineering**: Creating new features that could improve model performance, such as ratios between loan amount and salary.
- **Normalization/Standardization**: Scaling the features to ensure that no variable dominates due to its scale.

### Model Selection

- **Algorithm Choice**: Gradient Boosting Classifier was chosen due to its effectiveness in handling imbalanced datasets and its ability to model complex non-linear relationships.
- **Evaluation Metrics**: Accuracy, Precision, Recall, and F1 Score were considered to evaluate model performance, with a focus on F1 Score due to the imbalanced nature of the dataset.

### Model Training and Evaluation

- **Cross-Validation**: Used to estimate the performance of the model on unseen data and to mitigate overfitting.
- **Hyperparameter Tuning**: Performed using grid search to find the optimal settings for the model.

### Deployment

- **Model Serialization**: The trained model was serialized with joblib for easy loading in the application.
- **Streamlit App**: A user-friendly web app was built using Streamlit, allowing users to input their data and receive predictions in real-time.

### User Interface

- **Input Fields**: Users can input their financial indicators such as interest rate, loan amount, and outstanding balance.
- **Prediction Output**: The app displays the model's prediction on the loan status (Approved/Not Approved) based on the input data.

## Assumptions

- **Data Representativeness**: It is assumed that the dataset accurately represents the population of loan applicants.
- **Feature Relevance**: The selected features are assumed to have a significant impact on the loan approval decision.
- **Static Model**: The model does not adapt to new data over time; retraining is required for model updates.

## Reasoning

- **Gradient Boosting Classifier**: Chosen for its robustness and ability to handle various types of data. Its performance on similar tasks suggested it would be a good fit.
- **Streamlit for UI**: Streamlit was selected for its simplicity and effectiveness in creating data applications, allowing for rapid development and deployment.

## Future Directions

- **Model Improvement**: Continuous monitoring of model performance and retraining with new data to adapt to changes over time.
- **Feature Expansion**: Incorporating more features, such as employment history or credit score, could improve model accuracy.
- **User Feedback Loop**: Implementing a mechanism to collect user feedback on predictions to further refine and improve the model.

## Conclusion

This project demonstrates the end-to-end development of a machine learning application, from data preprocessing and model training to deployment and user interface creation. The choice of technologies and methodologies was driven by the need for accuracy, efficiency, and user accessibility.