import pickle
from datetime import datetime, date
import sklearn
import pandas as pd
import base64
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
st.set_page_config(layout="wide", initial_sidebar_state="auto")

data = pd.read_csv("Data/sales_data.csv")

Model_list = data['Model'].unique().tolist()

Age_list = data["Age"].unique().tolist()

def price_prediction(Model, Age):
    pickle_file_path = "Data/DecisionTreeModel.pkl"
    
    # Load the pickle file
    with open(pickle_file_path, 'rb') as file:
        saved_models = pickle.load(file)
    ML_Model = saved_models['ML_Model']
    Encoder = saved_models['Label_encoder']

    # Define a new data point to predict on
    new_data = pd.DataFrame({'Model': [Model],
                            'Age': [Age],
                            'Sale Price': 0})

    # Encoding Model
    new_data['Model']= Encoder.transform(new_data['Model'])
    new_data.drop('Sale Price', axis=1, inplace=True)
    sale_price = ML_Model.predict(new_data)
    return sale_price[0]
def price_prediction_RF(Model, Age):
    pickle_file_path = "Data/RandomForestModel.pkl"
    
    # Load the pickle file
    with open(pickle_file_path, 'rb') as file:
        saved_models = pickle.load(file)
    ML_Model = saved_models['ML_Model']
    Encoder = saved_models['Label_encoder']

    # Define a new data point to predict on
    new_data = pd.DataFrame({'Model': [Model],
                            'Age': [Age],
                            'Sale Price': 0})

    # Encoding Model
    new_data['Model']= Encoder.transform(new_data['Model'])
    new_data.drop('Sale Price', axis=1, inplace=True)
    sale_price = ML_Model.predict(new_data)
    return sale_price[0]


def add_background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    uniq001 = "unique_key_for_selectbox"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_background( 'Data/fullScreen.png' )

def Login():
    st.markdown("<h1 style='text-align: center; color: #64469b;'font-size:30px; font-family:Helvetica;'>DriveX Vehicle Price Prediction</h1>", unsafe_allow_html=True)
    uniq001 = "key001"
    uniq002 = "key002"
    col1,col2,col3,col4= st.columns([1,2,2,1])
    with col2:
        Model = st.selectbox("Model", Model_list,key=uniq001)
    with col3:
        Age = st.selectbox("Age", Age_list, key=uniq002)
    button_style = """
        <style>
            .stButton button {
                background-color: #64469b;
                color: white;
            }
            .stButton button.clicked {
                background-color: white;
                color: white;
            }
            header[data-testid="stHeader"] {
                display: none;
            }
        </style>
        """
    col1, col2, col3 = st.columns([3,2,2])
    with col1:
        st.write('')
    # Displaying the button
    with col2:
        st.markdown(button_style, unsafe_allow_html=True)
        if st.button("Predict Price"):
            try:
                Sale_price = price_prediction( Model, Age)
                Sale_price = round(Sale_price )
                Sale_price = f"{Sale_price:,}"
                
                RF_Sale_price = price_prediction_RF( Model, Age)
                RF_Sale_price = round(RF_Sale_price )
                RF_Sale_price = f"{RF_Sale_price:,}"
            
                
                custom_css1 = """
                    <style>
                    .rounded-box {
                        background-color: #f47624;
                        padding: 0px;
                        margin: 0 auto;
                        text-align: center;
                        width: 240px;
                        height: 130px;
                        transform: translateX(-50%);
                        border-radius: 15px; /* Adjust the value to change the roundness */
                    }
                    .rounded-box h1, .rounded-box h2 {
                        color: white;
                        font-size: 20px;
                    }
                    .rounded-box h2 {
                        font-size: 40px;
                        color:white;
                    }
                    </style>
                    """

                # Apply the custom CSS style
                st.markdown(custom_css1, unsafe_allow_html=True)

                # Display the rounded corner box with dynamic sale price
                col1, col2,col3 = st.columns([2,2,2])
                with col1:
                    st.markdown(
                        f"<div class='rounded-box'>"
                        f"<h1>Predicted Price</h1>"
                        f"<h2>\u20B9 {Sale_price}</h2>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                with col3:
                    st.markdown(
                        f"<div class='rounded-box'>"
                        f"<h1>Predicted Price</h1>"
                        f"<h2>\u20B9 {RF_Sale_price}</h2>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            except Exception as e:
                st.write("Invalid Data")
    with col3:
        st.write("")
if __name__ == "__main__":
    Login()