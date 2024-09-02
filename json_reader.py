import json
import requests
from operator import itemgetter
import mysql.connector


# Json Reader reads the JSON data from the Leetcode API and writes it to either a specified MySQL database or a file
# The code found within this function is based off another person's work found here:
# https://github.com/Bishalsarang/Leetcode-Questions-Scraper/blob/master/main.py
def scrape_leetcode():
    # Leetcode API URL that stores data for all problems as JSON
    url = "https://leetcode.com/api/problems/algorithms/"

    # Base URL to create links for each problem
    base_url = "https://leetcode.com/problems/"

    # Load JSON data from API
    page = requests.get(url).content
    json_data = json.loads(page)

    # List to store all the question data from the JSON
    get_data = [
        (
            child["stat"]["question__title_slug"],
            child["difficulty"]["level"],
            child["stat"]["frontend_question_id"],
            child["stat"]["question__title"],
        )
        for child in json_data["stat_status_pairs"]
        if not child["paid_only"]
    ]

    # Sort by difficulty followed by problem id in ascending order
    get_data.sort(key=itemgetter(1, 2))

    # List to store all the data from the JSON along with links to the questions
    complete_data = []
    for question in get_data:
        link = base_url + question[0]
        ifComplete = False
        if question[1] == 1:
            complete_data.append((link, 'Easy', question[2], question[3], ifComplete))
        elif question[1] == 2:
            complete_data.append((link, 'Medium', question[2], question[3], ifComplete))
        else:
            complete_data.append((link, 'Hard', question[2], question[3], ifComplete))
    return complete_data


# Function to write the data to a MySQL database to use for the randomizer
# Will not be used until later, mainly using text file for question storage.
def write_to_database(question_data):
    # Connect to the database, replace username, password, and database_name with your own
    mydb = mysql.connector.connect(
        host="localhost",
        user="username",
        password="password",
        database="database_name"
    )

    mycursor = mydb.cursor()

    for question in question_data:
        sql = ("INSERT INTO question "
               "(question_number, question_title, question_link, question_difficulty, question_completion) "
               "VALUES (%s, %s, %s, %s, %s)")
        val = (question[2], question[3], question[0], question[1], 0)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")


def write_to_file(question_data):
    with open('questions.txt', 'w') as file:
        for question in question_data:
            file.write(str(question[2]) + "|" +     # Question Number
                       question[1] + "|" +          # Difficulty
                       question[3] + "|" +          # Question Title
                       str(question[4]) + "|" +     # Completion Status
                       question[0] + "\n")          # Question Link
    file.close()


if __name__ == "__main__":
    data = scrape_leetcode()
    # write_to_database(data) # Uncomment this line to write to a MySQL database
    write_to_file(data)
