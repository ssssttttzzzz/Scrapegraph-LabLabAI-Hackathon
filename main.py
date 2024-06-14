import os
import base64
import streamlit as st
import json
import pandas as pd
from dotenv import load_dotenv
from helper import (
    playwright_install,
    add_download_options
)
from task import task
from text_to_speech import text_to_speech

# Load environment variables
load_dotenv()
st.set_page_config(page_title="search")

# Install playwright browsers
playwright_install()

def save_email(email):
    with open("mails.txt", "a") as file:
        file.write(email + "\n")
        
with st.sidebar:
    st.markdown("""---""")
    st.write("# Usage Examples")
    st.write("## Prompt 1")
    st.write("- Give me all the news with their abstracts")
    st.write("## Prompt 2")
    st.write("- Create a voice summary of the webpage")
    st.write("## Prompt 3")
    st.write("- List me all the images with their visual description")
    st.write("## Prompt 4")
    st.write("- Read me the summary of the news")
    st.markdown("""---""")
    if st.session_state['code']:
        st.markdown(st.session_state['code'])

    # Password input for authentication
    password = st.text_input("Enter password to unlock:", type="password")
    
    if password == "stz":
        st.session_state["authenticated"] = True
        st.session_state["code"] = "k7Bv9xF4Z0mT2aQ3pJ1oL8wR6uY5N0gX9dW\
        3yH7nV2sA4bC6tP8zE1jK5fM3rQ\
        6oY9vL0wZ2uX4nT5mP1aR7yF9pH6dW3kJ8sV0gQ2oC4tN7zY1bA6jE5fM3rL9xW\
        4uT0pJ2aQ5mT8yR1oX6nV3sW9dH7bC4gK0zE2uY5fM8kP6tL1jQ3oR7vN9wF0J2\
        aT4yP5mX8nV1sW6dH3bC9gK7zE0uY2fM5kR8oL6tJ1aQ3pT7yP9mN0wF4xJ2u2X\
        wyVL6nnQcP7WwV6VLccUa4T3BlbkFJ1i5OPuxGEnWxFVQ5gn9fyw5nV3sT8oLaQ\
        6mR9yP2dH5bW7kC0gE4fM3jN8tR5oL6uY1aQ7pT9mV2nW4dH3bC8kJ0gE5fM2r9\
        yP6oL1tJ3aQ8mT7uX4wV0nW3dH5bC9kR6zE2fM1jY8pT4oL7aQW0dH39mT1uX5w\
        3mR5yP9nV0wF2xJ6uX3sT8dH5bC4gK9zE0fM7kR1jQ3oL6tY2aP9mT5wV8nW4dH\
        3bC7kJ0gE6fM1rN9yP3oL8tT5uX2aQ7pR6mV4nW9dH0bC2kJ5gE3fM7kR1jY8tP\
        4oL6aQ9mTkR1jQ3oL9tY5nV4dH9bC0kJ2gE5fM3kR1jY7tP4oL6aQ9mT1uX5wV2\
        nW3dH8bC0gK4zE7fM6kR1jQ3oL9tY5aP2mT9uX4wV7nW0dH3bC8kJ5gE6fM1rN9\
        yP3oL7tT5uX2aQ8mR6nV4dH9bC0kJ2gE5fM3kR1jY7tP4oL6aQ9mT1uX5wV2nW3\
        dH8bC0gK4zE7fM6kR1jQ3oL9tY5aP2mT9uX4wV7nW0dH3bC8kJ5gE6fM1rN9yP3\
        oL7tT5uX2aQ8mR6nV4dH9bC0kJ2gE5fM3kR1jY7tP4oL6aQ9mT1uX5wV2nW3dH8\
        bC0gK4zE7fM6kR1jQ3oL9tY5aP2mT9uX4wV7nW0dH3bC8kJ5gE6fM1rN9yP3oL7\
        tT5uX2aQ8mR6nV4dH9bC0kJ2gE5fM3kR1jY7tP4oL6aQ9mT1uX5wV2nW3dH8bC0\
        gK4zE7fM6kRkJ5gE6fM1rN9yP3oL7tT5uX2aQ8mR6nV4dH9bC0kJ2gE5fM3kR1j\
        Y7tP4oL6aQ9mT1uX5wV2nW3dH8bC0gK4zE7fM6kR1jQ3oL9tY5aP2mT9uX4wV7n\
        W0dH3"

st.title("Search")
left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image("assets/scrapegraphai_logo.png")

if "authenticated" in st.session_state and st.session_state["authenticated"]:
    model = st.radio(
        "Select the model",
        ["gpt-3.5-turbo", "gpt-4turbo", "text-to-speech", "gpt-4o"],
        index=3,
    )
    key = st.text_input("api_key",type="password")
    url = st.text_input("base url (optional)")
    link_to_scrape = st.text_input("Link to scrape")
    prompt = st.text_input("Write the prompt")

    if st.button("Run the program", type="primary"):
        if not key or not model or not link_to_scrape or not prompt:
            st.error("Please fill in all fields except the base URL, which is optional.")
        else:
            st.write("Scraping phase started ...")

            if model == "text-to-speech":
                res = text_to_speech(key, prompt, link_to_scrape)
                st.write(res["answer"])
                st.audio(res["audio"])
            else:
                # Pass url only if it's provided
                if url:
                    graph_result = task(key, link_to_scrape, prompt, model, base_url=url)
                else:
                    graph_result = task(key, link_to_scrape, prompt, model)

                print(graph_result)
                st.write("# Answer")
                st.write(graph_result)
else:
    st.warning("Please enter the correct password to unlock the application.")

