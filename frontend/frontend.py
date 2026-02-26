import requests
import streamlit as st
import os
st.title('Insurance Premium Category Predictor')
st.markdown('Enter your details below:')

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')

age = st.number_input('Age', min_value=1, max_value=119, value=30)
weight = st.number_input('Weight (kg)', min_value=1.0, max_value=199.0, value=65.0)
height = st.number_input('Height (m)', min_value=0.5, max_value=2.49, value=1.7)
income_lpa = st.number_input('Annual Income (LPA)', min_value=0.1, value=10.0)
smoker = st.selectbox('Are you a smoker?', options=[False, True])
city = st.text_input('City', value='Mumbai')
occupation = st.selectbox(
    'Occupation',
    [
        'student', 'private_job', 'government_job',
        'business_owner', 'unemployed', 'freelancer', 'retired',
    ],
)

if st.button('Predict Premium Category'):
    input_data = {
        'age': age,
        'weight': weight,
        'height': height,
        'income_lpa': income_lpa,
        'smoker': smoker,
        'city': city.strip().title(),
        'occupation': occupation,
    }

    try:
        response = requests.post(API_URL, json=input_data, timeout=15)
        response.raise_for_status()
        result = response.json()

        st.success(
            f'Predicted Insurance Premium Category: '
            f'**{result["predicted_category"]}**'
        )
        st.metric('Confidence', f'{result["confidence"]:.1%}')
        st.write('Class Probabilities:')
        st.json(result['class_probabilities'])

    except requests.exceptions.ConnectionError:
        st.error(
            'Could not connect to the API server. '
            'Make sure the backend is running.'
        )
    except requests.exceptions.Timeout:
        st.error('Request timed out. The server may be overloaded.')
    except requests.exceptions.HTTPError as exc:
        st.error(f'API returned an error: {exc.response.status_code}')
        try:
            st.json(exc.response.json())
        except ValueError:
            st.text(exc.response.text)
    except Exception as exc:
        st.error(f'Unexpected error: {exc}')
