import streamlit as st
from openai import OpenAI
import base64

# Page Title
st.set_page_config(page_title="SmartPantry AI", page_icon="🍳")
st.title("🍳 SmartPantry AI")
st.subheader("Upload a photo of your ingredients, and I will suggest a recipe!")

# Input for API Key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
client = OpenAI(api_key=api_key)

# File uploader
uploaded_file = st.file_uploader("Select a photo of your fridge or pantry...", type=["jpg", "png"])

if uploaded_file and api_key:
    st.image(uploaded_file, caption='Your Inventory', use_column_width=True)

    if st.button("Generate Recipe!"):
        with st.spinner('Analyzing ingredients...'):
            # Encoding the image
            image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")

            # OpenAI API Call
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": [
                        {"type": "text",
                         "text": "What can I cook with these ingredients? Provide a short, easy-to-follow recipe."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ]}
                ]
            )
            st.write("### AI Recipe Suggestion:")
            st.write(response.choices[0].message.content)