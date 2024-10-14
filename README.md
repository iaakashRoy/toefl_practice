# Streamlit TOEFL Test App
This project is a web application designed to simulate the TOEFL test experience, with AI-generated questions and real-time evaluation.

## Setup

Follow the steps below to set up the project on your local machine:

### Step 1: Clone the Repository

```bash
git clone https://github.com/iaakashRoy/toefl_practice.git
```

### Step 2: Create or Check .env File

Create a `.env` file (if not already present) and add your `GROQ_API_KEY`:
```
GROQ_API_KEY=your_api_key_here
```

### Step 3: Build the Docker Image

Use the following command to build the Docker image:
```bash
docker build -t my-streamlit-app .
```

### Step 4: Run the Docker Image

Run the container with the following command:
```bash
docker run -p 2222:8501 my-streamlit-app
```

### Step 5: Open the Application

Once the container is running, open the application in your browser at:
[http://localhost:2222](http://localhost:2222)

## Technical Details

For now, please refer to the code files for technical clarity. More detailed documentation will be added as the project progresses.

You can copy this markdown content as-is into your `README.md` file.
