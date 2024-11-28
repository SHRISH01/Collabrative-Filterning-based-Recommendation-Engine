import streamlit as st
import pickle
import pandas as pd
import random
import sys
import os

# Load model and data
with open('joke_recommendation_model.pkl', 'rb') as file:
    model = pickle.load(file)

jokes = pd.read_csv('Data/JokeText.csv')

# Streamlit App Configuration
st.set_page_config(page_title="Joke Recommendation Engine", page_icon="😂", layout="wide")
st.title("😂 Joke Recommendation Engine")
st.write("Discover jokes tailored to your sense of humor!")

# Initialize session_state if not already initialized
if 'current_joke_id' not in st.session_state:
    st.session_state['current_joke_id'] = 0  # Initialize the joke id to 0 (or your starting point)

# Get the current joke
current_joke_id = st.session_state['current_joke_id']
joke_text = jokes.loc[jokes['JokeId'] == current_joke_id, 'JokeText'].values[0]
st.subheader("Here's a joke for you : ")
st.write(joke_text)

# Rating input from the user
rating = st.slider(f"Rate this joke (-10 to 10):", -10, 10, 0)

# Recommend a new joke based on the rating
if st.button("Submit Rating"):
    user_id = "streamlit_user"
    
    # Predict ratings for all jokes
    predicted_ratings = {}
    for joke_id in jokes['JokeId']:
        predicted_ratings[joke_id] = model.predict(user_id, joke_id).est
    
    # Sort jokes by predicted ratings
    sorted_jokes = sorted(predicted_ratings.items(), key=lambda x: x[1], reverse=True)
    
    # Find the next recommended joke
    for joke_id, pred_rating in sorted_jokes:
        if joke_id != current_joke_id:  # Exclude the current joke
            st.session_state['current_joke_id'] = joke_id  # Update to the next joke
            break
    
    st.success("Thanks for rating! Here's another joke for you:")
