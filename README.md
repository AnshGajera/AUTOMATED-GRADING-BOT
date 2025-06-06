# 📚 AI Assignment Grading Assistant

## Project Overview
This project is an AI-powered assignment grading assistant designed to streamline the evaluation process for educators. It leverages a team of specialized AI agents (built with the `agno` framework and powered by Google's Gemini model) to read student assignments, apply a grading rubric, provide detailed feedback, and offer specific justifications for scores. The application features a user-friendly web interface built with Streamlit, allowing users to easily upload PDF or DOCX assignment files.

## Features
* **File Upload:** Supports PDF and DOCX assignment file uploads.
* **Text Extraction:** Automatically extracts clean text content from uploaded documents.
* **AI-Powered Grading:** Utilizes a multi-agent system to grade assignments based on a predefined rubric (Content Relevance, Accuracy, Structure/Clarity, Grammar/Presentation).
* **Constructive Feedback:** Generates detailed feedback highlighting strengths, weaknesses, and suggestions for improvement.
* **Grade Justification:** Provides specific, detailed explanations for low scores (C or below) and general encouragement for higher grades.
* **Intuitive UI:** A simple and clear web interface for interacting with the grading system.

## How It Works
The grading pipeline involves several AI agents working in sequence:
1.  **AssignmentReader:** Extracts and cleans text from the uploaded assignment.
2.  **GradingAgent:** Evaluates the cleaned text against a rubric and provides a score and letter grade.
3.  **FeedbackAgent:** Generates constructive feedback based on the assignment content and assigned grade.
4.  **GradeJustifier:** Provides additional justification for the grade, particularly detailed for lower scores, including what the correct answer should contain and improvement suggestions.

## Setup and Installation

### Prerequisites
* Python 3.8+
* A Google Gemini API Key

### Steps
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/AnshGajera/AUTOMATED-GRADING-BOT.git](https://github.com/AnshGajera/AUTOMATED-GRADING-BOT.git)
    cd AUTOMATED-GRADING-BOT
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Gemini API Key:**
    Create a file named `.env` in the root directory of your project (where `main.py` is located) and add your Gemini API key:
    ```
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
    ```
    **Important:** Do not commit your `.env` file to GitHub! It's already included in the `.gitignore` below.

## Running the Application
Once setup is complete, you can run the Streamlit application:

```bash
streamlit run app.py
