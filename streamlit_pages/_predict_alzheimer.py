import time
import joblib
import pandas as pd
from config import *
import streamlit as st

def prediction_page():
    def convert_to_one_hot(selected_category, all_categories):
        one_hot = [True if category == selected_category else False for category in all_categories]
        for value in one_hot:
            user_input.append(value)

    def predict_alzheimer(input_data):
        loaded_model = joblib.load('model/alzheimer_model.pkl')
        predictions = loaded_model.predict(input_data)
        return predictions

    st.markdown('<h1 style="color: orange;">Patient Information</h1>', unsafe_allow_html=True)


    age = st.number_input("Age", min_value=0, max_value=122, step=1, value=65)
    gender = st.selectbox("Gender", ("Male", "Female"))
    education = st.number_input("Years of Education", min_value=0, value=12)

    st.write("<br>", unsafe_allow_html=True)

    # Orange heading for Demographics
    st.markdown('<h2 style="color: orange;">Demographics</h2>', unsafe_allow_html=True)
    ethnicity = st.radio("Ethnicity", ("Hisp/Latino", "Not Hisp/Latino", "Unknown"))
    race_cat = st.radio("Race Category", ("White", "Black", "Asian"))

    st.write("<br>", unsafe_allow_html=True)

    # Orange heading for Genetic Info
    st.markdown('<h2 style="color: orange;">Genetic Information</h2>', unsafe_allow_html=True)
    apoe_allele_type = st.selectbox("APOE Allele Type", ["APOE4_0", "APOE4_1", "APOE4_2"])
    apoe_genotype = st.selectbox("APOE4 Genotype", ("2,2", "2,3", "2,4", "3,3", "3,4", "4,4"))
    imputed_genotype = st.radio("Imputed Genotype", ("True", "False"))

    # Orange heading for Cognitive Assessment
    st.markdown('<h2 style="color: orange;">Cognitive Assessment</h2>', unsafe_allow_html=True)
    mmse = st.number_input("MMSE Score", min_value=0, max_value=30, step=1)

    st.write("<br>", unsafe_allow_html=True)

    # Custom CSS to style the Predict button
    with st.container():
        st.markdown("""
            <style>
                div.stButton > button:first-child {
                    background-color: red;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)
        predict_button = st.button("Predict")

    st.write("")

    loading_bar = st.empty()
    if age and education and mmse and apoe_genotype and race_cat and gender and apoe_allele_type and imputed_genotype and ethnicity and predict_button:
        loading_bar.write("Thank you for entering the patient's information.")
        progress_text = "Please wait, we're predicting your clinical condition..."
        my_bar = loading_bar.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1, text=progress_text)

        user_input = [age, education, mmse]

        convert_to_one_hot("PTRACCAT_" + race_cat, PTRACCAT_CATEGORIES)
        convert_to_one_hot("APOE Genotype_" + apoe_genotype, APOE_CATEGORIES)
        convert_to_one_hot("PTETHCAT_" + ethnicity, PTHETHCAT_CATEGORIES)
        convert_to_one_hot(apoe_allele_type, APOE4_CATEGORIES)
        convert_to_one_hot("PTGENDER_" + gender, PTGENDER_CATEGORIES)
        convert_to_one_hot("imputed_genotype_" + imputed_genotype, IMPUTED_CATEGORIES)

        data = pd.DataFrame([user_input])
        predicted_condition = predict_alzheimer(data)
        
        loading_bar.empty()

        st.write("")
        st.write("")
        st.markdown('<h3 style="color: orange;">Predicted Clinical Condition:</h3>', unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: orange;'><b>{ABBREVIATION[predicted_condition[0]]}</b> ({predicted_condition[0]})</h2>", unsafe_allow_html=True)
        st.markdown(f"<p>{CONDITION_DESCRIPTION[predicted_condition[0]]}</p>", unsafe_allow_html=True)

