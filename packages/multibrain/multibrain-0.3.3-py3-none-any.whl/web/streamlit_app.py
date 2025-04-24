# app/web/streamlit_app.py

import streamlit as st
import httpx
import markdown2
import asyncio

# Set page configuration
st.set_page_config(
    page_title="MultiBrain",
    page_icon="favicon.ico",
    layout="centered",
)

# Read custom CSS from file
with open("app/web/styles.css") as f:
    custom_css = f.read()

# Inject custom CSS with Markdown
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

# Header section
st.header("MultiBrain")

# Initialize session state for storing queries and responses
if "queries" not in st.session_state:
    st.session_state.queries = []


def submit_query():
    # Capture the current value of the query from the text area
    current_query = st.session_state.query_textarea

    if current_query:
        # Append the new query to session state with an empty response placeholder
        st.session_state.queries.append((current_query, []))
        asyncio.run(
            fetch_response(len(st.session_state.queries) - 1)
        )  # Use asyncio.run to call async function


async def fetch_response(index):
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(600.0)) as client:
            response = await client.post(
                "http://localhost:8000/query",
                json={"query": st.session_state.queries[index][0]},
                headers={"Content-Type": "application/json"},
            )

        responses = response.json().get("responses", [])

        # Update the response in session state
        st.session_state.queries[index] = (
            st.session_state.queries[index][0],
            responses,
        )

    except Exception as e:
        st.error(f"Error: {e}")


# Query form
query_textarea = st.text_area(
    "Enter your query...", height=100, on_change=None, key="query_textarea"
)
submit_button = st.button("Submit Query", on_click=submit_query)

# Display all queries and their corresponding responses
for query, responses in reversed(st.session_state.queries):
    with st.container():
        # Display the user's query in a yellow box
        st.markdown(
            f'<div class="yellow-box"><strong>Query:</strong> {query}</div>',
            unsafe_allow_html=True,
        )

        for resp in responses:
            if "error" in resp:
                st.markdown(
                    f'<div class="light-blue-box"><strong>Error:</strong> {resp["response"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                content = markdown2.markdown(resp["response"])
                if resp["source"] == "server1":
                    st.markdown(
                        f'<div class="light-blue-box">{content}</div>',
                        unsafe_allow_html=True,
                    )
                elif resp["source"] == "server2":
                    st.markdown(
                        f'<div class="green-box">{content}</div>',
                        unsafe_allow_html=True,
                    )
                elif resp["source"] == "Summary Server":
                    st.markdown(
                        f'<div class="light-pink-box">{content}</div>',
                        unsafe_allow_html=True,
                    )

# Footer section
st.markdown(
    "<footer><p><A HREF='https://spacecruft.org/deepcrayon/multibrain'>© 2025 Jeff Moe</A></p></footer>",
    unsafe_allow_html=True,
)
