# ClaxonHack
End-to-end datascience app

# Machine Learning Model Development

This project involves the development of a machine learning model to predict loan default based on various features. The process includes data cleaning, exploratory data analysis (EDA), feature selection, model training, and evaluation.

## Data Cleaning

- Checked for missing values and dropped rows with any missing data.
- Removed duplicate entries to ensure the uniqueness of the dataset.
- Validated and cleaned inconsistent categorical data.

## Exploratory Data Analysis (EDA)

- Visualized the distribution of gender and loan status using bar charts to understand the dataset's composition.
- Analyzed the correlation between numeric features to identify potential relationships.

## Feature Selection

- Utilized a RandomForestClassifier to determine the importance of features.
- Selected the top features based on their importance scores for model training.

## Model Training

- Trained multiple models including Logistic Regression, SVC, Gradient Boosting Classifier, KNN, and RandomForestClassifier.
- Evaluated each model's accuracy to identify the best performer.

## Model Evaluation

- Further evaluated the selected model using a separate validation set.
- Generated a classification report and confusion matrix to assess the model's performance.

## Conclusion

The project successfully demonstrates the process of developing a machine learning model from data cleaning to model evaluation. The RandomForestClassifier emerged as a robust model for predicting loan defaults, balancing accuracy with computational efficiency.

## Future Work

- Experiment with more advanced feature engineering techniques.
- Explore model tuning and hyperparameter optimization for improved performance.
- Investigate the deployment of the model for real-time predictions.