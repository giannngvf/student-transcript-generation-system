# Student Transcript Generation System

This Python program is designed to generate student transcripts based on provided student details and course information. The system allows users to select various student levels and degrees, retrieve student details, and generate transcripts and statistics based on the selected criteria.

## Features

1. **Student Details:** View detailed information about a student.
2. **Statistics:** View statistical information about a student's grades.
3. **Transcript Based on Major Courses:** Generate a transcript based on the student's major courses.
4. **Transcript Based on Minor Courses:** Generate a transcript based on the student's minor courses.
5. **Full Transcript:** Generate a complete transcript for the student.
6. **Previous Transcript Requests:** View previous transcript requests.
7. **Select Another Student:** Switch to another student.
8. **Terminate the System:** Exit the program.

## Installation

1. Ensure you have Python installed on your system.
2. Install the required dependencies using pip:
    ```bash
    pip install pandas
    ```

## Usage

1. **Run the Program:**
    ```bash
    python transcript_system.py
    ```

2. **Follow the On-Screen Instructions:**
   - Select the student level (Undergraduate, Graduate, or Both).
   - Select the student degree (Master, Doctorate, or Both) if applicable.
   - Enter the student ID.
   - Navigate through the menu to view details, generate transcripts, or exit the system.

## Code Overview

### Main Functions

- **startFeature():** Initializes the program, prompts the user for student level and degree, and verifies student ID.
- **menuFeature(stdID, levels, degrees):** Displays the main menu and handles user choices.
- **detailsFeature(stdID, levels, degrees):** Displays detailed student information.
- **statisticsFeature(stdID, levels, degrees):** Displays statistical information about the student's grades.
- **majorTranscriptFeature(stdID, levels, degrees):** Generates a transcript based on major courses.
- **minorTranscriptFeature(stdID, levels, degrees):** Generates a transcript based on minor courses.
- **fullTranscriptFeature(stdID, levels, degrees):** Generates a complete transcript for the student.

### Supporting Functions

- **recordRequest(stdID, requestType):** Records the type of request made by the user.
- **printPreviousRequest(stdID):** Prints previous requests made by the user.
- **clearOutput():** Clears the console output for better readability.

## File Structure

- `studentDetails.csv`: Contains the details of the students.
- `transcript_system.py`: The main Python script containing the program logic.
- `std{stdID}.csv`: CSV files named after student IDs containing the student's course details.

## Example studentDetails.csv Format

| stdID      | Name   | Level | Degree | Terms | College | Department | Major | Minor |
|------------|--------|-------|--------|-------|---------|------------|-------|-------|
| 202006000  | Alice  | U     | BS1    | 8     | Eng     | CS         | CS    | Math  |
| 201008000  | Bob    | G     | M1     | 4     | Sci     | Bio        | Bio   | Chem  |

## Example std{stdID}.csv Format

| Term | Level | Degree | courseID | courseName | creditHours | Grade | courseType |
|------|-------|--------|----------|------------|-------------|-------|------------|
| 1    | U     | BS1    | CS101    | IntroCS    | 3           | 3.5   | Major      |
| 1    | U     | BS1    | MATH101  | Calculus   | 4           | 3.0   | Minor      |

## Notes

- Ensure that the CSV files are in the same directory as the Python script.
- The program assumes specific column names and formats in the CSV files as shown in the examples above.
