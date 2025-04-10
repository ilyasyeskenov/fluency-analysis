import os
import streamlit as st
from fluency.fluency import Fluency

# Create the temp directory if it doesn't exist
if not os.path.exists('./temp'):
    os.makedirs('./temp')

# Set up the Streamlit app
st.title("Audio Analysis Tool")
st.write("Upload a .wav or .mp3 audio file to analyze its fluency.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a file", type=["wav", "mp3"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    audio_path = f"./temp/{uploaded_file.name}"
    
    # Write the uploaded file to the temp directory
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Create an instance of the Fluency class
    fluency_instance = Fluency(uploaded_file.name, audio_path)
    
    # Analyze the audio file
    result = fluency_instance.get_result()

    # Clean up the temporary file
    os.remove(audio_path)

    # Display the results
    st.write("Analysis Results:")
    st.json(result)  # Display results in JSON format
    