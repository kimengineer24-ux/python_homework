import csv
import os
import traceback
from datetime import datetime
import custom_module


def print_exception(e):
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = []

    for trace in trace_back:
        stack_trace.append(
            f"File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}"
        )

    print(f"Exception type: {type(e).__name__}")

    message = str(e)
    if message:
        print(f"Exception message: {message}")

    print(f"Stack trace: {stack_trace}")


# Task 2: Read a CSV File
def read_employees():
    employees_dict = {}
    rows = []

    try:
        with open("../csv/employees.csv", "r") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    employees_dict["fields"] = row
                else:
                    rows.append(row)

            employees_dict["rows"] = rows

    except Exception as e:
        print_exception(e)

    return employees_dict


employees = read_employees()


# Task 3: Find the Column Index
def column_index(column_name):
    return employees["fields"].index(column_name)


employee_id_column = column_index("employee_id")


# Task 4: Find the Employee First Name
def first_name(row_number):
    first_name_column = column_index("first_name")
    return employees["rows"][row_number][first_name_column]


# Task 5: Find the Employee
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))
    return matches


# Task 6: Find the Employee with a Lambda
def employee_find_2(employee_id):
    matches = list(
        filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"])
    )
    return matches


# Task 7: Sort the Rows by last_name
def sort_by_last_name():
    last_name_column = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_column])
    return employees["rows"]


# Task 8: Create a dict for an Employee
def employee_dict(row):
    result = {}

    for index, field in enumerate(employees["fields"]):
        if field != "employee_id":
            result[field] = row[index]

    return result


# Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    result = {}

    for row in employees["rows"]:
        employee_id = row[employee_id_column]
        result[employee_id] = employee_dict(row)

    return result


# Task 10: Use the os Module
def get_this_value():
    return os.getenv("THISVALUE")


# Task 11: Creating Your Own Module
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


def read_minutes_file(file_name):
    minutes_dict = {}
    rows = []

    try:
        with open(file_name, "r") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    minutes_dict["fields"] = row
                else:
                    rows.append(tuple(row))

            minutes_dict["rows"] = rows

    except Exception as e:
        print_exception(e)

    return minutes_dict


# Task 12: Read minutes1.csv and minutes2.csv
def read_minutes():
    minutes1_dict = read_minutes_file("../csv/minutes1.csv")
    minutes2_dict = read_minutes_file("../csv/minutes2.csv")

    return minutes1_dict, minutes2_dict


minutes1, minutes2 = read_minutes()


# Task 13: Create minutes_set
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])

    return set1.union(set2)


minutes_set = create_minutes_set()


# Task 14: Convert to datetime
def create_minutes_list():
    minutes_list_result = list(minutes_set)

    minutes_list_result = list(
        map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list_result)
    )

    return minutes_list_result


minutes_list = create_minutes_list()


# Task 15: Write Out Sorted List
def write_sorted_list():
    minutes_list.sort(key=lambda row: row[1])

    converted_list = list(
        map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list)
    )

    with open("./minutes.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(minutes1["fields"])
        writer.writerows(converted_list)

    return converted_list
