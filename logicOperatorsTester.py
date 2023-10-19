import random
import csv
import os
import pandas as pd

def generate_logical_exercise():
    operators = ['and', 'or', 'not', 'nand', 'nor', 'xor',
                 'implies', 'equivalent']  # Logical operators
    operands = [True, False]  # Operands

    # Randomly choose operator and operands
    operator = random.choice(operators)
    operand1 = random.choice(operands)
    operand2 = random.choice(operands)

    # Generate expression
    if operator == 'not':
        expression = f"{operator} {operand1}"
    else:
        expression = f"({operand1} {operator} {operand2})"

    # Calculate the result
    if operator == 'and':
        result = operand1 and operand2
    elif operator == 'or':
        result = operand1 or operand2
    elif operator == 'not':
        result = not operand1
    elif operator == 'nand':
        result = not (operand1 and operand2)
    elif operator == 'nor':
        result = not (operand1 or operand2)
    elif operator == 'xor':
        result = operand1 != operand2
    elif operator == 'implies':
        result = not operand1 or operand2
    elif operator == 'equivalent':
        result = operand1 == operand2

    # Exercise formatting
    exercise = f"What is the result of the expression: {expression}?"

    return operand1, operator, operand2, result, exercise


def save_to_csv(exercises, filename):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for exercise in exercises:
            writer.writerow(exercise)


def load_from_csv(filename):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Index', 'Round', 'Operand 1', 'Operator', 'Operand 2', 'Result', 'User Result'])

    exercises = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header
        for row in reader:
            if len(row) >= 7:
                index = int(row[0])
                round_num = int(row[1])
                operand1 = bool(row[2])
                operator = row[3]
                operand2 = bool(row[4])
                result = bool(row[5])
                user_result = bool(row[6])
                exercises.append((index, round_num, operand1, operator, operand2, result, user_result))
    return exercises


def calculate_metrics(exercises):
    total_exercises = len(exercises)
    if total_exercises == 0:
        print("There are no exercises to calculate metrics.")
        return

    total_correct = 0
    total_error = 0
    accuracy_by_operator = {}
    error_by_operator = {}

    for exercise in exercises:
        result = exercise[4]
        user_result = exercise[6]
        operator = exercise[3]

        if result == user_result:
            total_correct += 1
            if operator in accuracy_by_operator:
                accuracy_by_operator[operator] += 1
            else:
                accuracy_by_operator[operator] = 1
        else:
            total_error += 1
            if operator in error_by_operator:
                error_by_operator[operator] += 1
            else:
                error_by_operator[operator] = 1

    accuracy = total_correct / total_exercises
    error = total_error / total_exercises

    metrics = {
        "total_exercises": total_exercises,
        "total_correct": total_correct,
        "total_error": total_error,
        "accuracy": accuracy,
        "error": error,
        "accuracy_by_operator": accuracy_by_operator,
        "error_by_operator": error_by_operator,
    }

    return metrics


filename = 'exercises.csv'
exercises = load_from_csv(filename)

# Get the last index and round number
if len(exercises) > 0:
    last_index = exercises[-1][0]
    last_round = exercises[-1][1]
    # print(last_index)
    # print(last_round)
else:
    last_index = -1
    last_round = 0

# Increment the index and round number
index = last_index + 1
round_num = last_round + 1

# Generate 5 exercises
new_exercises = []
for i in range(2):
    operand1, operator, operand2, result, exercise = generate_logical_exercise()
    new_exercises.append((index, round_num, operand1, operator, operand2, result, None, exercise))
    exercises.append((index, round_num, operand1, operator, operand2, result, None, exercise))
    index += 1
    print(exercise)

    # Read user response
    user_result = input("Answer (0 for False, 1 for True): ")

    if user_result == "0":
        user_result = False
    else:
        user_result = True

    # Store user response
    new_exercises[-1] = new_exercises[-1][:6] + (user_result,)

    # Check if the response is correct
    if result == user_result:
        print("Correct answer!")
    else:
        print("Incorrect answer!")
    print()

# Save new exercises to the CSV file
save_to_csv(new_exercises, filename)

# Calculate metrics
metrics = calculate_metrics(exercises)

# Display metrics
print("Metrics:")
print(f"Average accuracy in the current run: {metrics['accuracy']*100:.2f}%")
print(f"Average errors in the current run: {metrics['error']*100:.2f}%")

if metrics["total_exercises"] > 0:
    print(f"Percentage of correct answers in the current run: {metrics['accuracy']*100:.2f}%")
    print(f"Percentage of errors in the current run: {metrics['error']*100:.2f}%")
    print()
    print("Metrics by operator:")
    for operator, accuracy_count in metrics["accuracy_by_operator"].items():
        error_count = metrics["error_by_operator"].get(operator, 0)
        total_count = accuracy_count + error_count
        accuracy_percentage = accuracy_count / total_count * 100
        error_percentage = error_count / total_count * 100
        print(f"Operator {operator}:")
        print(f"   Accuracy percentage: {accuracy_percentage:.2f}%")
        print(f"   Error percentage: {error_percentage:.2f}%")
else:
    print("There are no exercises to calculate metrics.")
