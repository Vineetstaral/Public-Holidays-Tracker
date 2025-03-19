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

def get_public_holidays(country, year):
    """
    Fetch public holidays for a specific country and year using Calendarific API.
    """
    try:
        params = {
            "api_key": "YOUR_CALENDARIFIC_API_KEY",  # Replace with your Calendarific API key
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

# Input fields
country = st.text_input("Enter a country code (e.g., US, IN)")
year = st.text_input("Enter a year (e.g., 2023)")

if st.button("Get Public Holidays"):
    if country and year:
        holidays = get_public_holidays(country, year)
        if "error" in holidays:
            st.error(holidays["error"])
        else:
            st.write(f"### Public Holidays in {country.upper()} for {year}")
            for holiday in holidays:
                st.write(f"**{holiday['name']}:** {holiday['date']}")
    else:
        st.write("Please enter a country code and year.")

# Add a footer
st.markdown("---")
st.markdown("AI can make mistakes verify info hahaha")
