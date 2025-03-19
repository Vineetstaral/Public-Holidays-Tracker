import streamlit as st
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
import os
import requests

# Load the environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq model
llm = Groq(model="llama3-70b-8192", api_key=api_key)

# Calendarific API endpoint
CALENDARIFIC_API_URL = "https://calendarific.com/api/v2/holidays"

# List of country codes (ISO 3166-1 alpha-2)
COUNTRY_CODES = {
    "US": "United States",
    "IN": "India",
    "GB": "United Kingdom",
    "CA": "Canada",
    "AU": "Australia",
    "DE": "Germany",
    "FR": "France",
    "JP": "Japan",
    "CN": "China",
    "BR": "Brazil",
    # Add more country codes as needed
}

def get_public_holidays(country, year):
    """
    Fetch government holidays for a specific country and year using Calendarific API.
    """
    try:
        params = {
            "api_key": "bq5iJun7DoFEait3ZQ0Trki7i3eDGngA",  # Replace with your Calendarific API key
            "country": country,
            "year": year
        }
        response = requests.get(CALENDARIFIC_API_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        holidays_data = response.json()
        holidays = []
        for holiday in holidays_data["response"]["holidays"]:
            holidays.append({
                "name": holiday["name"],
                "date": holiday["date"]["iso"]
            })
        return holidays
    except requests.exceptions.RequestException as e:
        return {"error": f"Calendarific API error: {e}"}
    except KeyError:
        return {"error": "Invalid response from Calendarific API"}

# Streamlit app
st.title("🎉 Public Holidays Tracker 🌍")

# Dropdown for country code
country_code = st.selectbox(
    "Select a country",
    options=list(COUNTRY_CODES.keys()),
    format_func=lambda x: f"{x} - {COUNTRY_CODES[x]}"  # Display country name alongside code
)

# Input field for year
year = st.text_input("Enter a year (e.g., 2023)")

if st.button("Get Public Holidays"):
    if country_code and year:
        holidays = get_public_holidays(country_code, year)
        if "error" in holidays:
            st.error(holidays["error"])
        else:
            st.write(f"### Public Holidays in {COUNTRY_CODES[country_code]} ({country_code}) for {year}")
            for holiday in holidays:
                st.write(f"**{holiday['name']}:** {holiday['date']}")
    else:
        st.write("Please select a country and enter a year.")

# Add a footer
st.markdown("---")
st.markdown("AI can make mistakes(HAHAHAHA)")
