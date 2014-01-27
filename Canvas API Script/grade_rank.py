'''
When a new user signs up to ScholarBounty, they get points from all of their past
accomplishments. This script gets all their grades, not including courses the 
user is currently enrolled in.
'''
import requests
import simplejson
from pprint import pprint
import datetime

# Base URL for easy access
base_url = 'https://webcourses.ucf.edu/api/v1/'

# Access Token for easy access
simon_access_token = 'xxxxxxxxxx'
britt_access_token = 'yyyyyyyyyy'

# Main function is used to call the other functions
def main():
    token = select_user_token()
    # Calling function that lists all the grades from the start
    new_user_score = grades_from_start_score(token)
    # User's full name
    user_full_name = get_user_name(token)
    first_semester = get_first_semester(token)

    print user_full_name + "," " you have accumulated", new_user_score, "points since", first_semester + "."

# This function lets you pick which access token you want to user
def select_user_token():
    # Printing command to allow user to pick token
    print "Which user are you testing: "
    selection = input("Type 1 for Simon\nType 2 for Brittany\n")
    # Checks to see if user enters a correct value
    if selection < 1 or selection > 2:
        print "You entered an incorrect tester"
        select_user_token()
    
    return selection


# Get the user's first semester
def get_first_semester(token_selector):
    # Setting the entered token selector
    if token_selector == 1:
        # Simon's UCF Canvas Token
        parameters = {'access_token': simon_access_token
        , 'include[]' : 'total_scores'}
    else:
        # Brittany's UCF Canvas Token
        parameters = {'access_token': britt_access_token
        , 'include[]' : 'total_scores'}
    

    # List all my UCF courses
    get_courses = requests.get(base_url + 'courses', params=parameters)
    mc = get_courses.content
    
    # Storing json list in dictionary
    course_list = simplejson.loads(mc)
    
    # First semester's year
    first_year = course_list[0]['start_at'][0:4]
    # First semester's month
    first_month = course_list[0]['start_at'][5:7]

    # If first_month is 01 then the semester is Spring, 05 == Summer, else == Fall
    if int(first_month) == 01:
        semester = "Spring " + first_year
    elif int(first_month) == 05:
        semester = "Summer " + first_year
    else:
        semester = "Fall " + first_year

    return semester


# Get's the user's grades from the start and returns a score based on final grade
def grades_from_start_score(token_selector):
    # Setting the entered token selector
    if token_selector == 1:
        # Simon's UCF Canvas Token
        parameters = {'access_token': simon_access_token
        , 'include[]' : 'total_scores', 'enrollment_type': 'student'}
    else:
        # Brittany's UCF Canvas Token
        parameters = {'access_token': britt_access_token
        , 'include[]' : 'total_scores', 'enrollment_type': 'student'}
    
    # List all my UCF courses
    get_courses = requests.get(base_url + 'courses', params=parameters)
    mc = get_courses.content
    
    # Storing json list in dictionary
    course_list = simplejson.loads(mc)
    #pprint(course_list) #---------- pprint is for checking returned json object

    # Getting the current month
    current_month = get_current_month()
    
    # Creating list that stores the course name
    course_name_list = []

    # Creating list that stores the grade
    grade_list = []

    # Loop through the JSON course object dictionary
    for i in course_list:
        '''
        course_end_month is the month that the course ends, 
        this helps shave off classes that the user is currently enrolled in
        '''
        course_end_month = i['end_at'][5:7]

        if i['hide_final_grades'] is True:
            continue

        if i['enrollments'][0]['computed_current_score'] is None:
            continue

        '''
        If the current month is greater than the course_end_month,
        then that means the course is not currently in progress
        '''
        if current_month > int(course_end_month):
            # Putting past course in a list called course_name_list
            course_name_list.append(i['name']) 
            # Putting past course grade in a list called grade_list
            grade_list.append(i['enrollments'][0]['computed_current_score'])
        

    # Initializing score to 0
    score = 0
    # Loops through the list of grades. This is where the grades turn into a score
    for i in grade_list:
        '''
        Score algorithm works by dividing final grades by 10 and then 
        adding them together
        '''
        score += (i / 10)
    # Rounds the score to closest number
    score = round(score, 0)

    # Returning the score
    return int(score)


             
# Get's the current user's name and returns it
def get_user_name(token_selector):
    # Setting the entered token selector
    if token_selector == 1:
        # Simon's UCF Canvas Token
        parameters = {'access_token': simon_access_token
        , 'include[]' : 'total_scores'}
    else:
        # Brittany's UCF Canvas Token
        parameters = {'access_token': britt_access_token
        , 'include[]' : 'total_scores'}
    
    # Calling Canvas API to get user profile information
    get_user = requests.get(base_url + "users/self/profile", params=parameters)
    ui = get_user.content

    # Storing user info into dictionary
    user_info = simplejson.loads(ui)
    
    # Storing User's Name   
    name = user_info["name"]

    # Returns the name
    return name

# Gets the current date
def get_current_month():
    # now is set to the current date
    now = datetime.datetime.now()
    # month is the current month
    month = now.month
    # Returns the month
    return month

# Calling the main function
main()

