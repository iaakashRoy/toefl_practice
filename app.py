import streamlit as st
from sections.reading import ReadingGenerator
from sections.listening import ListeningGenerator
from sections.speaking import SpeakingGenerator
from sections.writing import WritingGenerator
from necessay.resources import display_timer, record_audio, generate_listening_audio
import numpy as np
from scipy.io.wavfile import write
import io
import os
from dotenv import load_dotenv
load_dotenv()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

reading = ReadingGenerator()
listening = ListeningGenerator()
speaking = SpeakingGenerator()
writing = WritingGenerator()

# Set Streamlit page to wide mode for better use of space
st.set_page_config(layout="wide")

# Call the function to display the timer
display_timer()

# Section selection moved to the sidebar
with st.sidebar:
    st.title("TOEFL Test Website")
    st.subheader("Start Test")
    section = st.selectbox("Select Section", ["Reading", "Listening", "Speaking", "Writing"])

# Main content area, divided into two columns (for passage and questions)
if section == "Reading":
    # Check if reading data is already in session state, if not, create and store it
    if "reading_data" not in st.session_state:
        st.session_state.reading_data = reading.create_reading_resource("Kolkata")
    
    reading_data = st.session_state.reading_data 
    st.write(reading_data)

    # Create two columns for the passage and questions, taking all space
    col1, col2 = st.columns(2)

    # Display the passage on the left side
    with col1:
        st.subheader("Reading Passage")
        st.write(reading_data['passage'])

    # Initialize an empty dictionary to store user answers
    user_answers = {}

    # Display each question with options on the right side
    with col2:
        st.subheader("Questions")
        for i, question_data in enumerate(reading_data["questions_and_options"], 1):
            question = question_data[0]
            options = question_data[1:-1]  # Options without the correct answer index
            
            st.write(f"Question {i}: {question}")
            
            # Display options and capture the user's selection
            user_answer = st.radio(f"Choose your answer for Question {i}", options, key=f"q{i}")
            
            # Record user answer in the dictionary
            user_answers[question] = user_answer

    # Submit button to finalize answers
    if st.button("Submit"):
        st.subheader("Your Answers")
        st.write(user_answers)

        # Compare the user's answers to the correct answers and show correct answers
        st.subheader("Correct Answers")
        correct_answers = {}
        score = 0
        for i, question_data in enumerate(reading_data["questions_and_options"], 1):
            question = question_data[0]
            options = question_data[1:-1]
            correct_answer_index = int(question_data[-1])
            correct_answer = options[correct_answer_index - 1]  # Subtract 1 to convert to zero-based index
            
            correct_answers[question] = correct_answer
            
            # Check if user's answer is correct
            if user_answers[question] == correct_answer:
                score += 1
        
        st.write(correct_answers)

        # Display the user's score
        st.subheader(f"Your Score: {score}/{len(reading_data['questions_and_options'])}")

elif section == "Listening":

    # Check if listening data is already in session state, if not, create and store it
    audio_file_path = os.path.join(script_dir, "resources/conv2.mp3")

    if "listening_data" not in st.session_state:
        st.session_state.listening_data = listening.create_listening_resource(audio_file_path)
    
    # Retrieve listening data from session state
    listening_data = st.session_state.listening_data

    # Create two columns for the audio and questions
    col1, col2 = st.columns(2)

    # Display the audio on the left side
    with col1:
        st.subheader("Listening Audio")
        st.audio(audio_file_path)

        with st.expander("Show Transcript"):
            st.write(listening_data["transcript"])

    # Initialize an empty dictionary to store user answers
    user_answers = {}

    # Display each question with options on the right side
    with col2:
        st.subheader("Questions")
        for i, question_data in enumerate(listening_data["questions_and_options"], 1):
            question = question_data[0]
            options = question_data[1:-1]  # Options without the correct answer index
            
            st.write(f"Question {i}: {question}")
            
            # Display options and capture the user's selection
            user_answer = st.radio(f"Choose your answer for Question {i}", options, key=f"q{i}")
            
            # Record user answer in the dictionary
            user_answers[question] = user_answer

    # Submit button to finalize answers
    if st.button("Submit"):
        st.subheader("Your Answers")
        st.write(user_answers)

        # Compare the user's answers to the correct answers and show correct answers
        st.subheader("Correct Answers")
        correct_answers = {}
        score = 0
        for i, question_data in enumerate(listening_data["questions_and_options"], 1):
            question = question_data[0]
            options = question_data[1:-1]
            correct_answer_index = int(question_data[-1])
            correct_answer = options[correct_answer_index - 1]  # Subtract 1 to convert to zero-based index
            
            correct_answers[question] = correct_answer
            
            # Check if user's answer is correct
            if user_answers[question] == correct_answer:
                score += 1
        
        st.write(correct_answers)

        # Display the user's score
        st.subheader(f"Your Score: {score}/{len(listening_data['questions_and_options'])}")

elif section == "Speaking":
    # Create two columns for the sample question and recording functionality
    col1, col2 = st.columns(2)

    # Left column: Display a sample speaking question
    with col1:
        st.subheader("Speaking Question")
        question = speaking.generate_speaking_question("student life")
        st.write(question)

    # Right column: Implement recording functionality
    with col2:
        st.subheader("Record Your Answer")
        st.write("Please record your answer for 45 seconds.")

        # Button to start recording
        if st.button("Start Recording"):
            # Record for 45 seconds
            duration = 45
            recording = record_audio(duration)

            # Convert the float64 data to int16 (WAV format requirement)
            recording_int16 = np.int16(recording / np.max(np.abs(recording)) * 32767)

            # Save to WAV buffer
            wav_buffer = io.BytesIO()
            write(wav_buffer, 44100, recording_int16)  # Write WAV file to buffer
            wav_buffer.seek(0)  # Go to the beginning of the buffer

            # Play WAV audio in Streamlit
            st.audio(wav_buffer, format='audio/wav')
            # Generating the Transcript
            transcript = speaking.audio_transcript(wav_buffer)
            # Print the transcript
            with st.expander("Show Transcript"):
                st.write(transcript)
            # Evaluate the user's response based on the transcript 
            evaluation = speaking.evaluation(question, transcript)

            st.write(evaluation)


# Writing Section
elif section == "Writing":

    # Check if reading data is already in session state, if not, create and store it
    if "question" not in st.session_state:
        st.session_state.question = writing.generate_question("work-life balance")
    
    question = st.session_state.question 

    # Create two columns for the sample question and response functionality
    col1, col2 = st.columns(2)

    # Left column: Display a sample writing question
    with col1:
        st.subheader("Writing Question")
        st.write(question)

    # Right column: Implement response functionality with a larger text area
    with col2:
        st.subheader("Write Your Response Below")
        response = st.text_area("Your answer:", height=450)  # Increased height for a bigger text area

        if st.button("Submit Response"):
            with st.spinner("Evaluating your essay..."):
                evaluation = writing.evaluate_essay(question, response)
                st.write(evaluation)