from groq import Groq

class SpeakingGenerator:
    def __init__(self):
        # Initialize the Groq client and set transcription options
        self.client = Groq()
        self.model = "llama3-70b-8192"  # Model for question generation
        self.transcript_model = "distil-whisper-large-v3-en" # Transcription model
        self.prompt = "Specify context or spelling"  # Optional prompt for transcription
        self.response_format = "json"  # Response format
        self.language = "en"  # Transcription language
        self.temperature = 0.0  # Model temperature setting

    def generate_speaking_question(self, topic):
        # Improve the passage prompt for clarity and tone.
        prompt = f"""
        Generate a TOEFL Independent Speaking question on the topic: '{topic}'.

        - The question should present a choice or ask for a preference/opinion relevant to the topic.
        - The question must be clear, concise, and open-ended, allowing for a variety of opinions.
        - Avoid any introductory text, such as "Here is a TOEFL question" or similar.
        - Only output the question itself, without any additional commentary or explanations.

        Example Questions:
        1. Do you prefer to study alone or in a group? Why?
        2. Is it better to live on campus or off campus while attending university? Explain your choice.
        3. Do you prefer taking online courses or attending in-person classes?

        Generate only the question text.
        """

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        return chat_completion.choices[0].message.content
    
    def audio_transcript(self, file_buffer):
        """
        Generate a transcript from an audio file or file-like object using the Groq API.
        :param file_buffer: File or file-like object (e.g., BytesIO) containing the audio
        :return: Transcribed text from the audio
        """
        transcription = self.client.audio.transcriptions.create(
            file=("audio.wav", file_buffer.export().read()),  # Pass the buffer directly
            model=self.transcript_model,  # Model for transcription
            prompt=self.prompt,  # Optional prompt
            response_format=self.response_format,  # Format of the response
            language=self.language,  # Language of the audio
            temperature=self.temperature  # Model temperature
        )
        return transcription.text

    def evaluation(self, question, transcript):
        # Evaluate the user's response based on the transcript
        prompt = f"""You are a TOEFL Speaking evaluator. Evaluate the following response to the speaking question:\n
        Question: {question}\n
        Transcript: {transcript}\n
        Provide feedback on the following aspects:\n
        - Content relevance and coherence
        - Language fluency and accuracy
        - Pronunciation and intonation
        - Overall response quality\n

        At the end, provide a score from 0 to 4 based on the TOEFL Speaking rubric:
        """
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )

        return chat_completion.choices[0].message.content

    # def record_audio(self, file_path=None, duration=5, fs=44100):
    #     """
    #     Records audio from a file or the microphone.
    #     If file_path is provided, reads audio from the file instead of recording live.
    #     """
    #     if file_path:
    #         # Read pre-recorded audio file
    #         print(f"Reading audio from file: {file_path}")
    #         with open(file_path, 'rb') as f:
    #             return f.read()  # Return the audio file contents as a buffer
    #     else:
    #         try:
    #             # Record live audio from the microphone
    #             print(f"Recording audio for {duration} seconds...")
    #             recording = audiorecorder("Click to record", "Click to stop recording")
    #             while not recording.is_recording:
    #                 pass  # Wait until recording is finished
    #             print("Recording finished.")
    #             return recording
    #         except Exception as e:
    #             # Handle any exception that occurs during recording
    #             print(f"An error occurred during audio recording: {e}")
    #             return None

# Example usage
# speaking_gen = SpeakingGenerator()
# audio_data = speaking_gen.record_audio(duration=5)