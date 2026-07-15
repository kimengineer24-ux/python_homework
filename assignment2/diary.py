import traceback

try:
    with open("diary.txt", "a") as file:
        first_entry = True

        while True:
            if first_entry:
                line = input("What happened today? ")
                first_entry = False
            else:
                line = input("What else? ")

            file.write(line + "\n")

            if line == "done for now":
                break

except Exception as e:
    print("An exception occurred.")
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
