import streamlit as st
import time
from gtts import gTTS

# Function to display the timer using HTML and JavaScript
def display_timer():
    my_html = """
    <style>
    /* CSS to change font and position the timer in the top right corner */
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
    #timer-container {
        position: absolute;  /* Make the timer container absolute */
        top: 10px;           /* Position from the top */
        right: 10px;         /* Position from the right */
        height: 20px;        /* Reduced height for less space */
        padding: 5px;        /* Padding around the text */
        font-size: 20px;     /* Adjust font size */
        font-weight: bold;   /* Make font bold */
        color: #fff;         /* Change color to white for dark mode */
        background-color: rgba(0, 0, 0, 0.8); /* Dark background for better visibility in dark mode */
        border-radius: 5px;  /* Rounded corners for aesthetics */
    }
    </style>
    
    <script>
    function startTimer(duration, display) {
        var timer = duration, minutes, seconds;
        setInterval(function () {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                timer = duration;
                // Optionally, you can add actions when the timer reaches zero.
            }
        }, 1000);
    }

    window.onload = function () {
        var twentyMinutes = 60 * 20,
            display = document.querySelector('#time');
        startTimer(twentyMinutes, display);
    };
    </script>

    <div id="timer-container">
        Time Remaining: <span id="time">20:00</span>
    </div>
    """
    st.components.v1.html(my_html)


 # Function to record audio for a given duration
# def record_audio(duration, fs=44100):
#     # Create placeholders for animation and stopwatch
#     animation_placeholder = st.empty()
#     stopwatch_placeholder = st.empty()

#     # Start the recording
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')

#     # Show a rotating animation and a stopwatch while recording
#     spinner = ["⠋", "⠙", "⠹", "⠼", "⠦", "⠧", "⠇", "⠏"]  # More complex spinner
#     start_time = time.time()  # Record the start time

#     for i in range(duration * 10):  # Loop for the duration of the recording
#         elapsed_time = time.time() - start_time  # Calculate elapsed time
#         minutes, seconds = divmod(int(elapsed_time), 60)  # Convert to minutes and seconds
#         animation_placeholder.write(f" {minutes:02}{spinner[i % len(spinner)]}{seconds:02}")  # Update spinner
#         time.sleep(0.1)  # Adjust the speed of the animation

#     sd.wait()  # Wait until the recording is finished
#     animation_placeholder.empty()  # Clear the animation after recording
#     stopwatch_placeholder.empty()  # Clear the stopwatch after recording
#     return recording


def generate_listening_audio(prompt, filename='resources/audio_output.mp3'):
    # Create a gTTS object
    tts = gTTS(text=prompt, lang='en')
    tts.save(filename)

    return filename

# prompt = "Good morning! What are your thoughts on studying abroad?"
# audio_file = generate_listening_audio(prompt)user_answers

    # filename = "resources/listening_prompt.mp3"
    # tts.save(filename)