import streamlit as st
import joblib
import numpy as np
import pandas as pd
import pickle as pkl

gender_encode = joblib.load('OneHot_Gender.pkl')
one_hot = joblib.load('OneHot_Geo.pkl')
Model = joblib.load('XGBOOST.pkl')

def main():
    st.title('Churn Model Deployment')

    creditscore = st.number_input('CreditScore',0,900)
    geography = st.radio('Geography', ['France', 'Germany', 'Spain'])
    age = st.number_input('Age',18,100)
    gender = st.radio("Gender", ["Male", "Female"])
    tenure = st.number_input('Tenure',0,10)
    Balance = st.number_input('Balance',0.0,250000.0)
    NumOfProducts = st.number_input('Number of Products',0,5)
    HasCrCard = st.checkbox('Has Credit Card')
    IsActiveMember = st.checkbox('Is Active Member')
    EstimatedSalary = st.number_input('Estimated Salary', 0.0,220000.0)

    data = {'CreditScore': creditscore,'Geography': geography,'Age': int(age),'Gender': gender,'Tenure': int(tenure),'Balance': int(Balance),
            'NumOfProducts': int(NumOfProducts),'HasCrCard': int(HasCrCard),'IsActiveMember': int(IsActiveMember),'EstimatedSalary': EstimatedSalary}

    df=pd.DataFrame([list(data.values())],columns=['CreditScore','Geography','Age','Gender','Tenure','Balance',
            'NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary'])

    Gen = df[['Gender']]
    Geo = df[['Geography']]

    GENDER = pd.DataFrame(gender_encode.transform(Gen).toarray(),columns=gender_encode.get_feature_names_out())
    GEO = pd.DataFrame(one_hot.transform(Geo).toarray(),columns=one_hot.get_feature_names_out())

    df = pd.concat([df,GENDER,GEO], axis=1)
    df = df.drop(['Gender','Geography'], axis=1)

    if st.button('Make Prediction'):
      features=df
      result=make_prediction(features)
      st.success(f'The Prediction is: {result}')
        
def make_prediction(features):
    input_arr = np.array(features).reshape(1, -1)
    prediction = Model.predict(input_arr)
    if prediction == 1:
        return "Churn"
    else:
        return "Not Churn"
if __name__ == '__main__':
    main()
