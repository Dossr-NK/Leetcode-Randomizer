from datetime import datetime
import random as rand
import time

"""
Function of this file is to take the data from the MySQL database/file and randomly select a question to solve.
The question will be marked as complete in the database/file.
This will be set up to either run once or run continuously on a schedule and provide the user with a question to solve
depending on the day.
Schedule of problems to solve:
    Daily - 1 Easy (Monday - Saturday)
    Weekly - 1 Medium (Sunday)
    Monthly - 1 Hard (Last day of the month) (will add later, will mainly focus on easy and medium questions for now)
"""


def single_random_question():
    # Open the file and obtain all the questions
    file = open('questions.txt', 'r')
    questions = file.readlines()
    file.close()

    if datetime.now().day % 7 == 0:
        filtered_questions = [line for line in questions if 'Medium' in line]  # Obtains all the medium questions
    # elif datetime.now().day == 31:
    #     filtered_questions = [line for line in file if 'Hard' in line]  # Obtains all the hard questions
    else:
        filtered_questions = [line for line in questions if 'Easy' in line]  # Obtains all the easy questions

    # Randomly select a question and print it to the console for the user to solve
    deeply_filtered_questions = [line for line in filtered_questions if 'False' in line]
    location = rand.randint(0, len(deeply_filtered_questions) - 1)
    question = deeply_filtered_questions[location]
    question_parts = question.split('|')

    print("Complete the following question: ")
    print("Question number: " + question_parts[0])
    print("Difficulty: " + question_parts[1])
    print("Question Title: " + question_parts[2])
    print("Completion Status: " + question_parts[3])
    print("Question Link: " + question_parts[4])

    time.sleep(5)
    completed = input("Is the question complete? (Y/N): ")
    if completed == 'Y' or completed == 'y':
        question_parts[3] = 'True'

        # Update the original questions list
        questions[questions.index(question)] = '|'.join(question_parts)

        # Write the updated list back to the file
        with open('questions.txt', 'w') as file:
            file.writelines(questions)


single_random_question()
