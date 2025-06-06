import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.team.team import Team
from textwrap import dedent
import re # Import re for regex parsing

load_dotenv()
model = Gemini(api_key=os.getenv("GEMINI_API_KEY"))

# Agent 1: Reader
reader_agent = Agent(
    name="AssignmentReader",
    model=model,
    instructions=dedent("""
        You are an assistant that extracts and cleans the text from a student's assignment.
        Output only the relevant clean text for grading. Do not add any introductory or concluding remarks.
    """),
)

# Agent 2: Grader
grading_agent = Agent(
    name="GradingAgent",
    model=model,
    instructions=dedent("""
        You are a strict but fair grading assistant.
        Use this rubric:
        - Content relevance: 30%
        - Accuracy: 30%
        - Structure and clarity: 20%
        - Grammar and presentation: 20%
        Output ONLY the total score (0-100) and grade (A/B/C/D/F) in the format:
        Score: <number>/100
        Grade: <letter>
    """),
)

# Agent 3: Feedback Generator
feedback_agent = Agent(
    name="FeedbackAgent",
    model=model,
    instructions=dedent("""
        You generate constructive feedback on the student's assignment.
        Mention: strengths, weaknesses, and improvement suggestions.
        Output ONLY the feedback, starting with "Feedback:".
    """),
)

# Agent 4: Grade Justifier (new agent)
grade_justifier_agent = Agent(
    name="GradeJustifier",
    model=model,
    instructions=dedent("""
        You review grading decisions and provide additional justification for scores.
        If the input grade is C or below, explain in detail why the answer was marked low,
        provide what the correct answer should include, and offer specific improvement suggestions.
        This detailed analysis should be a single paragraph between 100-150 words.

        If the input grade is B or above, simply acknowledge the good work and suggest minor changes.
        This acknowledgment should be under 50 words.

        Output ONLY the justification, starting with "Grade Justification:".
    """),
)

# Combine into a Team
team = Team(
    name="AssignmentReviewTeam",
    model=model,
    members=[reader_agent, grading_agent, feedback_agent, grade_justifier_agent]
)

def run_grading_pipeline(assignment_text: str) -> dict:
    try:
        # Step 1: Reader cleans the text
        cleaned_text_response = reader_agent.run(message=f"Clean and extract text from: {assignment_text}")
        cleaned_text = cleaned_text_response.final_output if hasattr(cleaned_text_response, "final_output") else cleaned_text_response.content

        # Step 2: Grader evaluates and gives score/grade
        grading_response = grading_agent.run(message=f"Grade the following assignment based on the rubric:\n{cleaned_text}")
        grading_output = grading_response.final_output if hasattr(grading_response, "final_output") else grading_response.content

        score_match = re.search(r"Score:\s*(\d{1,3})", grading_output)
        grade_match = re.search(r"Grade:\s*([A-F][+]?)", grading_output)

        score = int(score_match.group(1)) if score_match else "N/A"
        grade = grade_match.group(1).strip() if grade_match else "N/A"

        # Step 3: Feedback Generator provides feedback
        feedback_response = feedback_agent.run(message=f"Generate constructive feedback for the following assignment, which received a grade of {grade}:\n{cleaned_text}")
        feedback_output = feedback_response.final_output if hasattr(feedback_response, "final_output") else feedback_response.content

        # Step 4: Grade Justifier provides justification based on the grade
        justification_response = grade_justifier_agent.run(message=f"Provide justification for this grade: {grade} on the following assignment:\n{cleaned_text}")
        justification_output = justification_response.final_output if hasattr(justification_response, "final_output") else justification_response.content

        # Assemble the final dictionary
        return {
            "marks": score,
            "grade": grade,
            # Rationale can be derived from the feedback/justification if not explicitly generated
            "rationale": f"Overall assessment: {grade}. See detailed feedback and justification below.",
            "feedback": feedback_output.replace("Feedback:", "").strip(),
            "grade_justification": justification_output.replace("Grade Justification:", "").strip()
        }

    except Exception as e:
        return {"error": str(e)}