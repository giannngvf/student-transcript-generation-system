import time
import pandas as pd
import sys
import datetime
import os

requests = {}  # initialize a dictionary to store requests of each student


def startFeature():
    # Initialize two empty lists to store the selected levels and degrees of the user
    levels = []
    degrees = []
    # Read the studentDetails.csv file using pandas and store it in a variable called 'df'
    df = pd.read_csv('studentDetails.csv')
    # Print a welcome message to the user
    print("\nWelcome to the Student Transcript Generation System!\n")
    # Ask the user to select the student level
    while True:
        level = input(
            'Please select the student level (U) Undergraduate, (G) Graduate, or (B) Both: ').upper()
        # If the user's input is valid, store the selected student level and break out of the loop
        if level in ['U', 'G', 'B']:
            if level == 'U':
                levels.append('U')
                degrees.append('BS1')
            if level == 'G':
                levels.append('G')
            if level == 'B':
                levels.extend(['U', 'G'])
                degrees.append('BS1')
            break
        # If the user's input is invalid, print an error message and ask again
        else:
            print('Invalid input. Please try again.')
    # Ask for degree if the user selects student level G or B
    if level in ['G', 'B']:
        while True:
            degree = input(
                'Please select the student degree (M) Master, (D) Doctorate, or (B0) Both: ').upper()
            # If the user's input is valid, store the selected degree and break out of the loop
            if degree in ['M', 'D', 'B0']:
                if degree == 'M':
                    degrees.append('M1')
                if degree == 'D':
                    degrees.append('D1')
                if degree == 'B0':
                    degrees.extend(['M1', 'D1'])
                break
            # If the user's input is invalid, print an error message and ask again
            else:
                print('Invalid input. Please try again.')
    # Ask the user to enter their student ID and check if it exists in the CSV file
    while True:
        stdID = int(input('Please enter the student ID (i.e. 202006000): '))
        # If the user's input is the special case of 201008000 and matches the selected level and degree, ask for a master degree
        if stdID == 201008000 and level in ['G', 'B'] and degree in ['M', 'B0']:
            masterDegree = input(
                "What master degree do you want to know? (M1) or (M2): ")
            if masterDegree in ['M1', 'M2']:
                degrees.clear()
                degrees.append(masterDegree)
                break
            else:
                print('Invalid master degree.')
        # If the user's input is not in the CSV file, print an error message and ask again
        elif df[df['stdID'] == int(stdID)].empty:
            print('Invalid student ID. Please try again.')
        # If the user's input is valid, break out of the loop
        else:
            break
    # Print message and call function clearOutput() and go to menu with returned stdID, levels, degrees values
    print("\nRedirecting to menu...\n")
    clearOutput()
    menuFeature(stdID, levels, degrees)


def menuFeature(stdID, levels, degrees):
    while True:
        # Print the menu details
        print("Student Transcript Generation System Menu")
        print("1. Student Details")
        print("2. Statistics")
        print("3. Transcript based on major courses")
        print("4. Transcript based on minor courses")
        print("5. Full transcript")
        print("6. Previous transcript request")
        print("7. Select another student")
        print("8. Terminate the system")
        # Get the user's choice by asking them to input a number
        choice = input("Enter your choice: ")
        print('')

        # Check if the user's choice is a valid integer between 1 and 8
        if choice.isdigit() and int(choice) in range(1, 9):
            choice = int(choice)
            # If the user's choice is 1, call the detailsFeature function and record the request in the recordRequest function
            if choice == 1:
                detailsFeature(stdID, levels, degrees)
                recordRequest(stdID, 'Student Details')
            # If the user's choice is 2, call the statisticsFeature function and record the request in the recordRequest function
            elif choice == 2:
                statisticsFeature(stdID, levels, degrees)
                recordRequest(stdID, 'Statistics')
            # If the user's choice is 3, call the majorTranscriptFeature function and record the request in the recordRequest function
            elif choice == 3:
                majorTranscriptFeature(stdID, levels, degrees)
                recordRequest(stdID, 'Major Transcript')
            # If the user's choice is 4, call the minorTranscriptFeature function and record the request in the recordRequest function
            elif choice == 4:
                minorTranscriptFeature(stdID, levels, degrees)
                recordRequest(stdID, 'Minor Transcript')
            # If the user's choice is 5, call the fullTranscriptFeature function and record the request in the recordRequest function
            elif choice == 5:
                fullTranscriptFeature(stdID, levels, degrees)
                recordRequest(stdID, 'Full Transcript')
            # If the user's choice is 6, call the previousRequestsFeature function
            elif choice == 6:
                printPreviousRequest(stdID)
            # If the user's choice is 7, call the startFeature function
            elif choice == 7:
                startFeature()
            # If the user's choice is 8, print a message indicating that the system is terminating,
            # call the previousRequestsFeature function , and exit the program
            else:
                previousRequestsFeature(stdID)
                sys.exit()
        # If the user's choice is not a valid integer between 1 and 8, print an error message
        else:
            print("Invalid choice. Please try again.")


def detailsFeature(stdID, level, degree):
    # Initialize a boolean variable to track if any data was found
    foundData = False
    # Read the contents of the student details from a CSV file using pandas
    df = pd.read_csv('studentDetails.csv')
    # Filter the DataFrame based on stdID, level, and degree
    filteredData = df[(df['stdID'] == int(stdID)) & (
        df['Level'].isin(level)) & (df['Degree'].isin(degree))]
    # Check if any matching data was found
    if filteredData.empty:
        # If not, print a message and return nothing
        print('No data found with the stdID, level, and degree you entered!\n')
        return
    # If matching data was found, create a string with the student details like name, stdID, etc
    output = ''
    levels = filteredData['Level'].unique()
    output += "Student Details:\n" \
              f"Name: {filteredData['Name'].iloc[0]}\n" \
              f"stdID: {filteredData['stdID'].iloc[0]}\n" \
              f"Level(s): {', '.join(levels)}\n" \
              f"Number of terms: {filteredData['Terms'].sum()}\n" \
              f"College(s): {', '.join(filteredData['College'].unique().tolist())}\n" \
              f"Department(s): {', '.join(filteredData['Department'].unique().tolist())}"
    # Indicate that data has been found for this student
    foundData = True
    # Write the output string to a text file and print it
    outputTXTFile = f"std{stdID}details.txt"
    with open(outputTXTFile, 'w') as f:
        f.write(output)
    print(output)
    # Print message and call function clearOutput()
    print("\nRedirecting to menu...\n")
    clearOutput()


def statisticsFeature(stdID, levels, degrees):
    # Initialize a boolean variable to track if any data was found
    foundData = False
    # Read the contents of student's course details
    df = pd.read_csv(f'{stdID}.csv')
    # Initialize an empty string to store the output
    output = ""
    # Iterate over the selected student levels and degrees of the user to calculate statistics
    for level in levels:
        # Set a string for the level name based on whether it is undergraduate or graduate
        levelName = 'Undergraduate' if level == 'U' else 'Graduate'
        for degree in degrees:
            # Filter the DataFrame based on the selected level and degree
            filteredData = df[(df['Level'] == level) &
                              (df['Degree'] == degree)]
            if filteredData.empty:
                # If no data was found for the current level and degree, continue to the next iteration
                continue
            # Calculate overall statistics of the student's course details
            overallAverage = filteredData['Grade'].mean()
            termAverages = filteredData.groupby('Term')['Grade'].mean()
            termMax = filteredData['Grade'].max()
            maxGrades = filteredData[filteredData['Grade'] == termMax]
            termMin = filteredData['Grade'].min()
            minGrades = filteredData[filteredData['Grade'] == termMin]
            # Format the output string with the calculated statistics
            statTitle = f"     {levelName} ({degree}) Level     "
            output += "=" * 60 + "\n"
            output += f"{statTitle.center(60, *'*')}\n"
            output += "=" * 60 + "\n"
            output += f"Overall average (major and minor) for all terms: {overallAverage:.2f}\n"
            output += "Average (major and minor) of each term:\n"
            for term, avg in termAverages.items():
                output += f"\tTerm {term}: {avg:.2f}\n"
            output += "Maximum grade(s) and in which term(s):\n"
            for _, row in maxGrades.iterrows():
                output += f"\tTerm {row['Term']}: {row['Grade']}\n"
            output += "Minimum grade(s) and in which term(s):\n"
            for _, row in minGrades.iterrows():
                output += f"\tTerm {row['Term']}: {row['Grade']}\n"
            # Set foundData to True to indicate that data has been found for this student
            foundData = True
    # If any data was found, write the output string to store in text file and print it
    if foundData:
        outputTXTFile = f"std{stdID}statistics.txt"
        with open(outputTXTFile, 'w') as f:
            f.write(output)
        print(output)
    else:
        # If no data was found, print a message
        print('No data found with the stdID, level, and degree you entered!\n')
    # Print message and call function clearOutput()
    print("\nRedirecting to menu...\n")
    clearOutput()


def majorTranscriptFeature(stdID, levels, degrees):
    # Initialize a boolean variable to track if any data was found
    foundData = False
    # Load the student details into data frames
    detailsDF = pd.read_csv('studentDetails.csv')
    stdDF = pd.read_csv(f'{stdID}.csv')
    # Initialize an empty string to store the output
    output = ""
    # Iterate over the selected student level and degree of the user
    for level in levels:
        for degree in degrees:
            # Filter the DataFrame to only include data for the selected student stdID, level and degree
            detailsfilteredData = detailsDF[(detailsDF['stdID'] == int(stdID)) & (
                detailsDF['Level'] == level) & (detailsDF['Degree'] == degree)]
            # If there is no data found, skip and continue
            if detailsfilteredData.empty:
                continue
            # If matching data was found, add the student details to the output string like name, stdID, college etc
            border = 60 * "=" + "\n"
            footer = f"     Major Transcript for Level ({level} - {degree})     "
            output += border
            output += f"{footer.center(60, *'*')}\n"
            output += f"{border}\n"
            output += f"Name: {detailsfilteredData['Name'].iloc[0]}\t\t\t\t\t\t"
            output += f"stdID: {detailsfilteredData['stdID'].iloc[0]}\n"
            output += f"College: {detailsfilteredData['College'].iloc[0]}\t\t\t\t\t\t\t"
            output += f"Department: {detailsfilteredData['Department'].iloc[0]}\n"
            output += f"Major: {detailsfilteredData['Major'].iloc[0]}\t\t\t\t\t\t"
            output += f"Minor: {detailsfilteredData['Minor'].iloc[0]}\n"
            output += f"Level: {detailsfilteredData['Level'].iloc[0]}\t\t\t\t\t\t\t\t"
            output += f"Number of terms: {detailsfilteredData['Terms'].sum()}\n\n"
            # Filter the DataFrame to only include data for the selected student level and degree
            stdfilteredData = stdDF[(stdDF['Level'] == level) & (
                stdDF['Degree'] == degree)]
            # Get a list of terms to be counted
            terms = stdfilteredData['Term'].unique()
            # Iterate over each term
            for term in terms:
                # Filter the DataFrame to only include data for the term
                termFilteredData = stdfilteredData[(
                    stdfilteredData['Term'] == term)]
                # Filter the DataFram to only include data for major courses
                majorFilteredData = termFilteredData[termFilteredData['courseType'] == 'Major']
                # Add the major courses information like type, name, grade to the output string
                titleTerm = f"     Term ({term})     "
                border = 60 * "=" + "\n"
                output += border
                output += f"{titleTerm.center(60, *'*')}\n"
                output += border
                output += "{:^15} {:^15} {:^15} {:^15}\n".format(
                    "courseID", "courseName", "creditHours", "Grade")
                for row in majorFilteredData.itertuples(index=False):
                    output += "{:^15} {:^15} {:^15} {:^15}\n".format(
                        row.courseID, row.courseName, row.creditHours, row.Grade)
                output += "\n\n"
                output += f"Major Average: {majorFilteredData['Grade'].mean():.2f}   \t\t\t\t"
                output += f"Overall Average: {termFilteredData['Grade'].mean():.2f}\n\n"
            footer = f"     End of Transcript for Level ({level} - {degree})     "
            output += border
            output += f"{footer.center(60, *'*')}\n"
            output += border
            # Set foundData to True to indicate that data has been found for this student
            foundData = True

    # If any data was found, write the output string to store in text file and print it
    if foundData:
        # Write the output string to a TXT file
        outputTXTFile = f"std{stdID}MajorTranscript.txt"
        with open(outputTXTFile, 'w') as f:
            f.write(output)
        # Print output
        print(output)
    else:
        # If no data was found, print a message
        print('No data found with the stdID, level, and degree you entered!\n')
    # Print message and call function clearOutput()
    print("\nRedirecting to menu...\n")
    clearOutput()


def minorTranscriptFeature(stdID, levels, degrees):
    # Initialize a boolean variable to track if any data was found
    foundData = False
    # Load the student details into data frames
    detailsDF = pd.read_csv('studentDetails.csv')
    stdDF = pd.read_csv(f'{stdID}.csv')
    # Initialize an empty string to store the output
    output = ""
    # Iterate over the selected student level and degree of the user
    for level in levels:
        for degree in degrees:
            # Filter the DataFrame to only include data for the selected student stdID, level and degree
            detailsfilteredData = detailsDF[(detailsDF['stdID'] == int(stdID)) & (
                detailsDF['Level'] == level) & (detailsDF['Degree'] == degree)]
            # If there is no data found, skip and continue
            if detailsfilteredData.empty:
                continue
            # If matching data was found, add the student details to the output string like name, stdID, college etc
            border = 60 * "=" + "\n"
            footer = f"     Minor Transcript for Level ({level} - {degree})     "
            output += border
            output += f"{footer.center(60, *'*')}\n"
            output += f"{border}\n"
            output += f"Name: {detailsfilteredData['Name'].iloc[0]}\t\t\t\t\t\t"
            output += f"stdID: {detailsfilteredData['stdID'].iloc[0]}\n"
            output += f"College: {detailsfilteredData['College'].iloc[0]}\t\t\t\t\t\t\t"
            output += f"Department: {detailsfilteredData['Department'].iloc[0]}\n"
            output += f"Major: {detailsfilteredData['Major'].iloc[0]}\t\t\t\t\t\t"
            output += f"Minor: {detailsfilteredData['Minor'].iloc[0]}\n"
            output += f"Level: {detailsfilteredData['Level'].iloc[0]}\t\t\t\t\t\t\t\t"
            output += f"Number of terms: {detailsfilteredData['Terms'].sum()}\n\n"
            # Filter the DataFrame to only include data for the selected student level and degree
            stdfilteredData = stdDF[(stdDF['Level'] == level) & (
                stdDF['Degree'] == degree)]
            # Get a list of terms to be counted
            terms = stdfilteredData['Term'].unique()
            # Iterate over each term
            for term in terms:
                # Filter the DataFrame to only include data for the term
                termFilteredData = stdfilteredData[(
                    stdfilteredData['Term'] == term)]
                # Filter the DataFrame to only include data for minor courses
                minorFilteredData = termFilteredData[termFilteredData['courseType'] == 'Minor']
                # Add the minor courses information like type, name, grade to the output string
                titleTerm = f"     Term ({term})     "
                border = 60 * "=" + "\n"
                output += border
                output += f"{titleTerm.center(60, *'*')}\n"
                output += border
                output += "{:^15} {:^15} {:^15} {:^15}\n".format(
                    "courseID", "courseName", "creditHours", "Grade")
                for row in minorFilteredData.itertuples(index=False):
                    output += "{:^15} {:^15} {:^15} {:^15}\n".format(
                        row.courseID, row.courseName, row.creditHours, row.Grade)
                output += "\n\n"
                output += f"Minor Average: {minorFilteredData['Grade'].mean():.2f}   \t\t\t\t"
                output += f"Overall Average: {termFilteredData['Grade'].mean():.2f}\n\n"
            footer = f"     End of Transcript for Level ({level} - {degree})     "
            output += border
            output += f"{footer.center(60, *'*')}\n"
            output += border
            # Set foundData to True to indicate that data has been found for this student
            foundData = True
    # If any data was found, write the output string to store in text file and print it
    if foundData:
        # Write the output string to a TXT file
        outputTXTFile = f"std{stdID}MinorTranscript.txt"
        with open(outputTXTFile, 'w') as f:
            f.write(output)
        # Print output
        print(output)
    else:
        # If no data was found, print a message
        print('No data found with the stdID, level, and degree you entered!\n')
    # Print message and call function clearOutput()
    print("\nRedirecting to menu...\n")
    clearOutput()


def fullTranscriptFeature(stdID, levels, degrees):
    # Initialize a boolean variable to track if any data was found
    foundData = False
    # Load the student details into data frames
    detailsDF = pd.read_csv('studentDetails.csv')
    stdDF = pd.read_csv(f'{stdID}.csv')
    # Initialize an empty string to store the output
    output = ""
    # Iterate over the selected student levels and degrees of the user
    for level in levels:
        for degree in degrees:
            # Filter DataFrame for rows matching the given stdID, level, and degree
            detailsfilteredData = detailsDF[(detailsDF['stdID'] == int(stdID)) & (
                detailsDF['Level'] == level) & (detailsDF['Degree'] == degree)]
            if detailsfilteredData.empty:
                continue  # skip and continue to next if no matching data were found
            # If matching data was found, append student's name, stdID, college, department, major, minor, level, and no of terms to output string
            border = 60 * "=" + "\n"
            footer = f"     Full Transcript for Level ({level} - {degree})     "
            output += border
            output += f"{footer.center(60, *'*')}\n"
            output += f"{border}\n"
            output += f"Name: {detailsfilteredData['Name'].iloc[0]}\t\t\t\t\t\t"
            output += f"stdID: {detailsfilteredData['stdID'].iloc[0]}\n"
            output += f"College: {detailsfilteredData['College'].iloc[0]}\t\t\t\t\t\t\t"
            output += f"Department: {detailsfilteredData['Department'].iloc[0]}\n"
            output += f"Major: {detailsfilteredData['Major'].iloc[0]}\t\t\t\t\t\t"
            output += f"Minor: {detailsfilteredData['Minor'].iloc[0]}\n"
            output += f"Level: {detailsfilteredData['Level'].iloc[0]}\t\t\t\t\t\t\t\t"
            output += f"Number of terms: {detailsfilteredData['Terms'].sum()}\n\n"
            # Filter DataFrame for rows matching the selected student level and degree
            stdFilteredData = stdDF[(stdDF['Level'] == level) & (
                stdDF['Degree'] == degree)]
            # count the no. of terms for this level and degree
            terms = stdFilteredData['Term'].unique()
            # Iterate over the terms for selected student level and degree
            for term in terms:
                # Filter DataFrames for rows matching the given term
                termFilteredData = stdFilteredData[(
                    stdFilteredData['Term'] == term)]
                minorFilteredData = termFilteredData[termFilteredData['courseType'] == 'Minor']
                majorFilteredData = termFilteredData[termFilteredData['courseType'] == 'Major']
                # Append the courseID, courseName, creditHours, and average grades for each course in this term to the output
                titleTerm = f"     Term ({term})     "
                border = 60 * "=" + "\n"
                output += border
                output += f"{titleTerm.center(60, *'*')}\n"
                output += border
                output += "{:^15} {:^15} {:^15} {:^15}\n".format(
                    "courseID", "courseName", "creditHours", "Grade")
                for row in termFilteredData.itertuples(index=False):
                    output += "{:^15} {:^15} {:^15} {:^15}\n".format(
                        row.courseID, row.courseName, row.creditHours, row.Grade)
                output += "\n\n"
                output += f"Major Average: {majorFilteredData['Grade'].mean():.2f}   \t\t\t\t"
                output += f"Minor Average: {minorFilteredData['Grade'].mean():.2f}\n"
                output += f"Term Average: {termFilteredData['Grade'].mean():.2f}   \t\t\t\t"
                output += f"Overall Average: {stdFilteredData['Grade'].mean():.2f}\n\n"
            footer = f"     End of Transcript for Level ({level} - {degree})     "
            output += border
            output += f"{footer.center(60, *'*')}\n"
            output += border
            # Set foundData to True to indicate that data has been found for this student
            foundData = True
    # If data was found for the student, write the output string to a TXT file and print it
    if foundData:
        # Write the output string to a TXT file
        outputTXTFile = f"std{stdID}FullTranscript.txt"
        with open(outputTXTFile, 'w') as f:
            f.write(output)
        # Print output
        print(output)
    else:
        # If no data was found, print a message
        print('No data found with the stdID, level, and degree you entered!\n')
    # Print message and call function clearOutput()
    print("\nRedirecting to menu...\n")
    clearOutput()


def recordRequest(stdID, request):
    if stdID not in requests:
        requests[stdID] = {'requestType': [], 'dateNow': [], 'timeNow': []}
    # Add the request type to the student's requestType list
    requests[stdID]['requestType'].append(request)
    # Get the current date and time
    date = datetime.datetime.now().strftime("%d/%m/%Y")  # format: day/month/year
    time = datetime.datetime.now().strftime("%I:%M %p")  # format: hour:minute AM/PM
    # Add the current date and time to student's dateNow and timeNow lists
    requests[stdID]['dateNow'].append(date)
    requests[stdID]['timeNow'].append(time)


def previousRequestsFeature(stdID):
    try:
        # Create the file name based on the student ID
        filename = f"std{stdID}PreviousRequests.txt"
        # Open the file in append mode or create it if it doesn't exist
        with open(filename, "a+") as f:
            # Move the cursor to the beginning of the file
            f.seek(0)
            # Read the first line of the file
            firstLine = f.readline()
            # If the header is not in the first line
            if 'Request Type' not in firstLine:
                # write the header to the file
                f.write("Request Type\t\t Time\t\tDate\n")
            # Iterate over the student's requestType list
            for i in range(len(requests[stdID]['requestType'])):
                # write each request type, time and date to the file
                f.write('{:<20} {:<10} {:<10}\n'.format(
                    requests[stdID]['requestType'][i], requests[stdID]['timeNow'][i], requests[stdID]['dateNow'][i]))
        # Display the previous requests
        print(f"Previous requests for {stdID}:")
        with open(filename) as f:
            # Read all lines of the file
            lines = f.readlines()
            # Iterate over each line
            for line in lines:
                # Print each line and add a newline character
                print(line.strip(), end='\n')
        # Print message and call function clearOutput()
        print("\nTerminating...\n")
        clearOutput()
    except KeyError:
        # Print message and call function clearOutput()
        print("No request(s) were recorded this time.")
        print("\nTerminating...\n")
        clearOutput()


def printPreviousRequest(stdID):
    try:
        # Open the file name based on the student ID
        filename = f"std{stdID}PreviousRequests.txt"
        # Display the previous requests
        print(f"Previous requests for {stdID}:")
        with open(filename) as f:
            # Read all lines of the file
            lines = f.readlines()
            # Iterate over each line
            for line in lines:
                # Print each line and add a newline character
                print(line.strip(), end='\n')
        # Print message and call function clearOutput()
        print("\nRedirecting to the menu...\n")
        clearOutput()
    except FileNotFoundError:
        # Print message and call function clearOutput()
        print("No previous request(s) were recorded as of now.")
        print("\nRedirecting to the menu...\n")
        clearOutput()


def clearOutput():
    # Wait for 3 seconds
    time.sleep(3)
    # Clear output
    def clear(): return os.system('cls')
    clear()


startFeature()
