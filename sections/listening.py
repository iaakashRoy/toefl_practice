from groq import Groq

class ListeningGenerator:
    def __init__(self):
        # Initialize the Groq client and set transcription options
        self.client = Groq()
        self.model = "llama3-70b-8192"  # Model for question generation
        self.transcript_model = "distil-whisper-large-v3-en"  # Transcription model
        self.prompt = "Specify context or spelling"  # Optional prompt for transcription
        self.response_format = "json"  # Response format
        self.language = "en"  # Transcription language
        self.temperature = 0.0  # Model temperature setting

    def audio_transcript(self, filepath):
        """
        Generate a transcript from an audio file using the Groq API.
        :param filepath: Path to the audio file
        :return: Transcribed text from the audio file
        """
        with open(filepath, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                file=(filepath, file.read()),  # Audio file for transcription
                model=self.transcript_model,  # Model for transcription
                prompt=self.prompt,  # Optional prompt
                response_format=self.response_format,  # Format of the response
                language=self.language,  # Language of the audio
                temperature=self.temperature  # Model temperature
            )
        return transcription.text

    def generate_questions(self, transcript):
        """
        Generate TOEFL-style multiple-choice questions based on the transcript.
        :param transcript: Transcribed text
        :return: JSON array of questions with options and correct answers
        """
        prompt_1 = f"""
        Generate three TOEFL-style multiple-choice questions from the provided transcript for the listening section. Each question should:
        - Test comprehension of key ideas in the passage.
        - Include four answer options (A, B, C, D).
        - Indicate the correct answer using its position (1 for A, 2 for B, 3 for C, 4 for D).

        **Output Format:**
        [
            ["Question 1", "Option A", "Option B", "Option C", "Option D", correct_option_index],
            ["Question 2", "Option A", "Option B", "Option C", "Option D", correct_option_index]
            ["Question 3", "Option A", "Option B", "Option C", "Option D", correct_option_index]
        ]

        - Correct answer indices must be integers (1-4) only, without any explanation.
        - Ensure that the output strictly follows the given format without extra text or comments.
        
        Transcript: {transcript}
        """

        chat_completion_1 = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_1}],
            model=self.model,
        )
        question_answers = chat_completion_1.choices[0].message.content

        # Validation prompt to ensure the output is in the correct format
        prompt_2 = f"""
        Validate the following array: {question_answers}. 
        Ensure:
        1. All brackets are properly closed.
        2. Each correct option index is an integer.

        Output the corrected array in the format:
        [
            ["Question 1", "Option 1", "Option 2", "Option 3", "Option 4", correct_option_index],
            ["Question 2", "Option 1", "Option 2", "Option 3", "Option 4", correct_option_index],
            ["Question 3", "Option 1", "Option 2", "Option 3", "Option 4", correct_option_index]
        ]

        Do not add any additional text or explanations.
        """

        chat_completion_2 = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_2}],
            model=self.model,
        )

        return chat_completion_2.choices[0].message.content

    def create_listening_resource(self, filepath):
        """
        Create a listening resource by generating a transcript and multiple-choice questions from an audio file.
        :param filepath: Path to the audio file
        :return: Dictionary containing the transcript and generated questions
        """
        transcript = self.audio_transcript(filepath)
        questions = self.generate_questions(transcript)
        
        return {
            "transcript": transcript,
            "questions_and_options": eval(questions)
        }
