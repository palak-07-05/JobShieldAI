# JobShield AI

AI-powered fake job detection platform using Machine Learning and NLP.

---

## Overview
This project uses Machine Learning and Natural Language Processing (NLP) to detect fake and fraudulent job postings.

The model analyzes job descriptions and predicts whether a job posting is real or fake.

---

## Real-World Problem
Fake job postings and internship scams are increasing on online job platforms. This project helps identify suspicious job listings using AI techniques.

---

## Features
- Fake vs Real job prediction
- Text preprocessing using NLP
- TF-IDF vectorization
- Machine Learning classification
- Accuracy evaluation
- Custom job posting prediction
- Netflix-style UI
- Login & Signup system
- AI confidence gauge
- Dashboard analytics
- Cybersecurity-inspired design

---

## Technologies Used
- Python
- Streamlit
- Machine Learning
- NLP
- Scikit-learn
- Plotly
- SQLite
- Pandas
- NumPy
- Matplotlib
- TF-IDF

---

## Machine Learning Model
- Logistic Regression

---

## Dataset
Fake Job Postings Dataset from Kaggle

Dataset Link:
https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction

---

## Project Workflow
1. Load dataset
2. Data cleaning
3. Combine text columns
4. Text vectorization using TF-IDF
5. Train-test split
6. Train Logistic Regression model
7. Predict fake job postings
8. Evaluate model accuracy

---

## Sample Prediction

Input:
"Earn money quickly from home without experience"

Output:
Fake Job Posting

---

## Future Improvements
- Deep learning integration
- Resume-job matching
- Real-time API deployment

---

## Run Project

```
pip install -r requirements.txt
streamlit run app.py
```