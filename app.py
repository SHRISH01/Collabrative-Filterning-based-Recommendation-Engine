import streamlit as st
import pickle
import pandas as pd
import random
import sys
import os


with open('joke_recommendation_model.pkl', 'rb') as file:
    model = pickle.load(file)


jokes = pd.read_csv('Data/JokeText.csv')


# Streamlit App
st.set_page_config(page_title="Joke Recommendation Engine", page_icon="😂", layout="wide")

st.title("😂 Joke Recommendation Engine")
st.write("Discover jokes tailored to your sense of humor!")

current_joke_id = st.session_state['current_joke_id']
joke_text = jokes.loc[jokes['JokeId'] == current_joke_id, 'JokeText']
st.subheader("Here's a joke for you : ")
st.write(joke_text)

rating = st.slider(f"Rate this joke (-10-10):", -10, -5, 0, 10, 5)

# Recommend a new joke
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
            st.session_state['current_joke_id'] = joke_id
            break
    
    st.success("Thanks for rating! Here's another joke for you:")
    st.experimental_rerun()