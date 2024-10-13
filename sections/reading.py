from groq import Groq

class ReadingGenerator:
    def __init__(self):
        # Initialize the Groq client and set the model to use.
        self.client = Groq()
        self.model = "llama3-70b-8192"

    def generate_passage(self, topic):
        # Improve the passage prompt for clarity and tone.
        prompt = f"""
        Generate an academic passage of 100-150 words on the topic: '{topic}' for the TOEFL reading section.\n
        The passage must:
        - Have a clear structure, including an introduction, body, and conclusion.
        - Explore key aspects of the topic in a concise and informative manner.
        - Be written in a neutral, formal tone, similar to academic textbooks or journal articles.
        - Use precise language and avoid overly complex vocabulary, ensuring it is accessible to non-native English speakers.
        - Avoid opinion or bias, focusing solely on factual and objective information.

        Ensure that the passage remains well-organized and within the specified word count.
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


    def generate_questions(self, passage):
        # Improve question-generation prompt to ensure clarity and correctness.
        prompt_1 = f"""
        Generate three TOEFL-style multiple-choice questions from the provided passage. Each question should:
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

        Passage: {passage}
        """

        chat_completion_1 = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_1,
                }
            ],
            model=self.model,
        )

        question_answers = chat_completion_1.choices[0].message.content

        # Improve validation prompt for clarity and brevity.
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
            messages=[
                {
                    "role": "user",
                    "content": prompt_2,
                }
            ],
            model=self.model,
        )

        return chat_completion_2.choices[0].message.content

    def create_reading_resource(self, topic):
        # Generate the passage and the corresponding questions and options.
        passage = self.generate_passage(topic)
        questions = self.generate_questions(passage)
        # Return the passage and parsed questions as a dictionary.
        return {
            "passage": passage,
            "questions_and_options": eval(questions)
        }