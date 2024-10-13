from groq import Groq

class WritingGenerator:
    def __init__(self):
        # Initialize the Groq client and set the model to use.
        self.client = Groq()
        self.model = "llama3-70b-8192"

    def generate_question(self, topic):
        # Improve the passage prompt for clarity and tone.
        prompt = f"""
        Generate an TOEFL Independent Writing question on the topic: '{topic}'.
        - The question should present a choice or ask for a preference/opinion relevant to the topic.
        - The question must be clear, concise, and open-ended, allowing for a variety of opinions.
        - Avoid any introductory text, such as "Here is a TOEFL question" or similar.
        - Only output the question itself, without any additional commentary or explanations.
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
    
    def evaluate_essay(self, question, essay):
        # Improve question-generation prompt to ensure clarity and correctness.
        prompt = f"""
        Evaluate the following TOEFL Independent Writing essay based on the criteria below:
        - Structure: Does the essay have a clear introduction, body, and conclusion?
        - Content: Does the essay address the topic with relevant examples and explanations?
        - Check the grammar, vocabulary, and coherence of the essay.
        - Give a score from 1 to 4 based on the quality of the essay
        - Provide constructive feedback on how the essay can be improved.

        Question: {question}
        Essay: {essay}
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
    
