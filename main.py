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
key = "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"
key = os.getenv("OPENAI_KEY")

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

    # Password input for authentication
    password = st.text_input("Enter password to unlock:", type="password")
    
    if password == "stz":
        st.session_state["authenticated"] = True

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

