from questions import QuizQuestion, FreeFormQuestion, Question
import json
import os
import random
from datetime import datetime

def save_questions(filename, questions):
    """This function saves the questions in the questions.json file"""
    with open(filename, 'w') as file:
        json.dump([q.to_dict() for q in questions], file)


def load_questions(filename):
    """This function returns a list of questions retrieved from the questions.json file."""
    # If a file with this name does not exist, return empty list
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        try:
            questions_data = json.load(file)
        except json.JSONDecodeError:
            # If file is empty return empty list
            return []
        return [Question.from_dict(q) for q in questions_data]
    
    
def save_test_results(score, question_amount):
    """This function records the test result in the results.json file."""
    results = []

    try:
        with open('data/results.json', 'r') as file:
            results = json.load(file)
    except FileNotFoundError:
        pass

    current_datetime = datetime.now()
    formatted_date_time = current_datetime.strftime("%Y-%m-%d %H:%M")

    record = {
        'time': formatted_date_time,
        'score': f"{score}/{question_amount}"
    }

    results.append(record)

    with open('data/results.json', 'w') as file:
        json.dump(results, file, indent=4)

    
def input_quiz_question():
    prompt = input("Enter the question prompt: ")
    choices = []
    print("Enter the choices and type 'done' when finished: ")

    while True:
        choice = input("Choice: ")
        if choice.strip().lower() == 'done':
            break
        choices.append(choice)
    
    answer = input("Enter the correct answer: ").strip()
    return QuizQuestion(prompt, choices, answer)


def input_free_form_question():
    prompt = input("Enter the question prompt: ").strip()
    answer = input("Enter the answer: ").strip()
    return FreeFormQuestion(prompt, answer)


def add_questions():
    """This function adds a question to the questions.json file. The users needs to select either a quiz question or a free form question type. Quiz questions need multiple choice answers, whereas free form question only has a single answer"""
    questions = load_questions('data/questions.json')

    while True:
        print("\nChoose question type:")
        print("1. Quiz Question")
        print("2. Free-Form Question")
        print("3. Exit and Save")
        choice = input("Enter choice (1/2/3): ")

        if choice == '1':
            questions.append(input_quiz_question())
        elif choice == '2':
            questions.append(input_free_form_question())
        elif choice == '3':
            save_questions('data/questions.json', questions)
            print("Questions saved to 'questions.json'.")
            break
        else:
            print("Invalid choice. Please try again.")


def show_statistics():
    """This function prints out all the questions in questions.json file"""
    questions = load_questions('data/questions.json')

    if not questions:
        print("\n No saved questions.")
        return

    print("\n Statistics:")
    for i, question in enumerate(questions):
        status = "Active" if question.active else "Inactive"
        print(f"\n Index: {i + 1}. {question.prompt}")
        print(f" Active: {status}")
        print(f" Asked: {question.asked}")
        print(f" Correctly Answered: {question.correctly_answered}")

def toggle_active():
    """This function changes the questions status from 'Active' to 'Inactive' and vice versa."""
    questions = load_questions('data/questions.json')

    if not questions:
        print("No questions available.")
        return

    print("\nList of questions:")
    for i, question in enumerate(questions):
        status = "Active" if question.active else "Inactive"
        answer = getattr(question, 'answer', 'N/A')
        print(f"\nID: {i + 1}. Active: {status}")
        print(f"Question: {question.prompt}")
        print(f"Answer: {answer}")

    while True:
        id_input = input("To change the active status of the question, type its ID or type 'done' to quit this mode: ").strip()

        if id_input.lower() == 'done':
            break

        try:
            id = int(id_input) - 1

            if 0 <= id < len(questions):
                current_status = "Active" if questions[id].active else "Inactive"
                new_status = "Inactive" if questions[id].active else "Active"
                answer = getattr(questions[id], 'answer', 'N/A')
                print(f"\nID: {id + 1}. Question: {questions[id].prompt}, Answer: {answer}, Active: {current_status}")
                confirm = input(f"The question is currently set to {current_status}. Are you sure you want to set it to {new_status}? (y/n): ").strip().lower()

                if confirm == 'y':
                    questions[id].set_active(not questions[id].active)
                    print(f"Change confirmed: The question status is now set to {new_status}.")
                    save_questions('questions.json', questions)
                elif confirm == 'n':
                    print("No changes were made.")
            else:
                print("Invalid index. Please try again.")

        except ValueError:
            print(f"Invalid input. Please enter a valid ID.")


def practice():
    """Practice mode provides the user with questions and keeps the record of the amount of times the question was asked and answered correctly. Questions are picked randomly from the questions saved in the questions.json file. Only questions that have the status set to 'Active' can be picked for practice. The chance of the question to appear in practice increases if the question is answered incorrectly."""
    questions = load_questions('data/questions.json')

    if len(questions) < 5:
        print("\nNeed at least 5 saved questions for this mode.")
        return
    
    practice_on = True

    # Filter out inactive questions
    active_questions = []
    for question in questions:
        if question.active:
            active_questions.append(question)

    # Get weights based on the times question was asked - question answered correctly (+1 so the weight is never less than 1 and the question actually appears in the practice)
    weights = []
    for question in active_questions:
        weight = question.asked - question.correctly_answered + 1
        weights.append(weight)

    while practice_on:
        selected_question = random.choices(active_questions, weights, k=1)

        print(f"\n{selected_question[0].prompt}")

        # Checking if the question is of the QuizQuestion class
        if isinstance(selected_question[0], QuizQuestion):
            for choice in selected_question[0].choices:
                print(f"{choice}")
        answer = input("Your answer: ")

        if answer.strip().lower() == 'done':
            save_questions('data/questions.json', questions)
            practice_on = False
        else:
            if selected_question[0].check_answer(answer):
                print("\nCorrect!")
            else:
                print("\nIncorrect.")


def test():
    """Test mode lets the user take the test by specifying the amount of questions. The questions are picked from questions.json file. Only the questions that have the status set to 'Active' can be present in a test. After the test is complete the test record is stored in results.json"""
    questions = load_questions('data/questions.json')

    if len(questions) < 5:
        print("\nNeed at least 5 saved questions for this mode.")
        return
    
    # Filter out inactive questions
    active_questions = []
    for question in questions:
        if question.active:
            active_questions.append(question)

    
    if not active_questions:
        print("No active questions available.")
        return

    while True:
        try:
            question_amount_int = int(input(f"Please enter the number of questions for this test (max {len(active_questions)}): "))
            if 1 <= question_amount_int <= len(active_questions):
                break
            else:
                print(f"Please enter a number between 1 and {len(active_questions)}.")
        except ValueError:
            print(f"Invalid input. Please enter a valid number.")

    selected_questions = random.sample(active_questions, question_amount_int)

    print("\nGood luck!")
    score = 0
    for i, question in enumerate(selected_questions):
        print(f"\nQuestion {i + 1}: {question.prompt}")
        if isinstance(question, QuizQuestion):
            for j, choice in enumerate(question.choices):
                print(f"{j + 1}. {choice}")
        answer = input("Your answer: ")

        if question.check_answer(answer):
            score +=1
            print("Correct!")
        else:
            print("Incorrect.")
    
    print("\nTest completed.")
    print(f"Your score: {score}/{question_amount_int}")

    # Save results
    save_test_results(score, question_amount_int)
 

def mode_selection():
    """This function displays and lets interact with the main menu"""
    
    while True:
        print("\nSelect one of these modes:")
        print("1. Add questions")
        print("2. Statistics")
        print("3. Disable/enable questions")
        print("4. Practice")
        print("5. Test")
        print("6. Exit")
        choice = input("Enter choice (1/2/3/4/5): ")

        if choice == '1':
            add_questions()
        elif choice == '2':
            show_statistics()
        elif choice == '3':
            toggle_active()
        elif choice == '4':
            practice()
        elif choice == '5':
            test()
        elif choice == '6':
            os._exit(0)
        else:
            print("Invalid choice. Please try again.")


def main():
    mode_selection()


if __name__ == "__main__":
    main()


# Link to the repository from part 3 https://github.com/MartynasVidziunas/war-game.git