# Write your code here.# Task 1: Hello
def hello():
    return "Hello!"


# Task 2: Greet with a Formatted String
def greet(name):
    return f"Hello, {name}!"


# Task 3: Calculator
def calc(num1, num2, operation="multiply"):
    try:
        if operation == "add":
            return num1 + num2
        elif operation == "subtract":
            return num1 - num2
        elif operation == "multiply":
            return num1 * num2
        elif operation == "divide":
            return num1 / num2
        elif operation == "modulo":
            return num1 % num2
        elif operation == "int_divide":
            return num1 // num2
        elif operation == "power":
            return num1 ** num2
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"


# Task 4: Data Type Conversion
def data_type_conversion(value, data_type):
    try:
        if data_type == "int":
            return int(value)
        elif data_type == "float":
            return float(value)
        elif data_type == "str":
            return str(value)
    except ValueError:
        return f"You can't convert {value} into a {data_type}."


# Task 5: Grading System, Using *args
def grade(*args):
    try:
        average = sum(args) / len(args)

        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except Exception:
        return "Invalid data was provided."


# Task 6: Use a For Loop with a Range
def repeat(string, count):
    new_string = ""

    for number in range(count):
        new_string += string

    return new_string


# Task 7: Student Scores, Using **kwargs
def student_scores(score_type, **kwargs):
    if score_type == "mean":
        return sum(kwargs.values()) / len(kwargs)

    if score_type == "best":
        best_student = ""
        best_score = 0

        for student, score in kwargs.items():
            if score > best_score:
                best_score = score
                best_student = student

        return best_student


# Task 8: Titleize, with String and List Operations
def titleize(title):
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    words = title.split()
    titleized_words = []

    for index, word in enumerate(words):
        if index == 0 or index == len(words) - 1:
            titleized_words.append(word.capitalize())
        elif word in little_words:
            titleized_words.append(word)
        else:
            titleized_words.append(word.capitalize())

    return " ".join(titleized_words)


# Task 9: Hangman, with more String Operations
def hangman(secret, guess):
    result = ""

    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"

    return result


# Task 10: Pig Latin, Another String Manipulation Exercise
def pig_latin(sentence):
    vowels = "aeiou"
    words = sentence.split()
    pig_latin_words = []

    for word in words:
        if word[0] in vowels:
            pig_latin_words.append(word + "ay")
        else:
            index = 0

            while index < len(word):
                if word[index:index + 2] == "qu":
                    index += 2
                elif word[index] in vowels:
                    break
                else:
                    index += 1

            pig_latin_words.append(word[index:] + word[:index] + "ay")

    return " ".join(pig_latin_words)