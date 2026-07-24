# Task 3: List Comprehensions Practice

import csv

with open("../csv/employees.csv", "r") as file:
    reader = csv.reader(file)
    employees = list(reader)

employee_names = [
    employee[1] + " " + employee[2]
    for employee in employees[1:]
]

print(employee_names)

names_with_e = [
    name
    for name in employee_names
    if "e" in name
]

print(names_with_e)