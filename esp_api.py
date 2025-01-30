import pandas as pd
import numpy as np
import fitz  # PyMuPDF for reading PDFs
import os
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    # Save the uploaded PDF file to a temporary location
    with open("temp.pdf", "wb") as temp_file:
        temp_file.write(pdf_file.getbuffer())
    
    # Open the saved temporary PDF file
    doc = fitz.open("temp.pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"  # Extract text from each page
    
    # Clean up temporary file after reading
    os.remove("temp.pdf")
    
    return text

# Function to process extracted text into structured format
def extract_questions_answers(pdf_text):
    lines = pdf_text.split("\n")  # Split text into lines
    questions = []
    answers = []
    current_question = None
    current_answer = ""

    for line in lines:
        line = line.strip()
        if line.startswith("Q "):  # Detect question
            if current_question:
                questions.append(current_question)
                answers.append(current_answer.strip())  # Store previous question-answer pair
            current_question = line  # Start new question
            current_answer = ""
        elif current_question:  # Collect answer text
            current_answer += " " + line

    # Add last question-answer pair
    if current_question:
        questions.append(current_question)
        answers.append(current_answer.strip())

    return questions, answers

# Streamlit Interface
st.title("Student Answer Evaluation")

# File upload for correct answers CSV
correct_answers_file = st.file_uploader("Upload the Correct Answers CSV", type=["csv"])
if correct_answers_file:
    correct_answers = pd.read_csv(correct_answers_file)
    st.write(correct_answers)

# File upload for student answers PDF
student_pdf_file = st.file_uploader("Upload the Student Answers PDF", type=["pdf"])
if student_pdf_file:
    # Extract and process the PDF
    pdf_text = extract_text_from_pdf(student_pdf_file)
    questions, student_answers = extract_questions_answers(pdf_text)

    # Convert to DataFrame
    student_answers_df = pd.DataFrame({'Question': questions, 'Answers': student_answers})
    st.write(student_answers_df)

    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # List to store calculated marks
    marks_obtained = []

    # Loop through each student answer and calculate marks
    for index, row in student_answers_df.iterrows():
        question_id = row['Question'].strip()  # Remove extra spaces
        student_answer = row['Answers']

        # Find the correct answer for this question
        correct_answer_row = correct_answers[correct_answers['Question'].str.strip() == question_id]

        if correct_answer_row.empty:  # If no match found, skip to the next question
            st.warning(f"⚠ Warning: Question '{question_id}' not found in correct_answers.csv. Skipping...")
            marks_obtained.append(0)
            continue

        correct_answer = correct_answer_row['Correct_Answer'].values[0]  # Get correct answer text
        max_marks = correct_answer_row['Marks'].values[0]  # Get full marks for this question

        # Combine correct and student answer for vectorization
        combined_text = [correct_answer, student_answer]

        # Convert both answers into vector form
        vectors = vectorizer.fit_transform(combined_text)

        # Compute cosine similarity (ranges from 0 to 1)
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

        # Improve scoring function (boost high similarities)
        if similarity > 0.9:
            assigned_marks = max_marks  # Full marks for very high similarity
        elif similarity > 0.75:
            assigned_marks = max_marks * 1  # 90% marks
        elif similarity > 0.5:
            assigned_marks = max_marks * 0.95  # 75% marks
        elif similarity > 0.3:
            assigned_marks = max_marks * 0.8  # 50% marks
        else:
            assigned_marks = max_marks * similarity  # Proportional marks for low similarity

        marks_obtained.append(int(np.ceil(assigned_marks)))  # Round up to nearest integer

    student_answers_df['Marks_Obtained'] = marks_obtained

    # Display results
    st.subheader("Evaluation Results")
    st.write(student_answers_df)

    # Calculate total marks obtained
    total_marks_obtained = sum(marks_obtained)
    total_max_marks = correct_answers['Marks'].sum()

    st.write(f"🎯 Total Marks Obtained: {total_marks_obtained} / {total_max_marks}")
