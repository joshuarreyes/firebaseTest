import pyrebase # pip install pyrebase4
import requests
import re
import json
'''
Firebase file functions

 processHttpError(e): Process HTTP error. Returns None.

 authenticate_user(user): Authenticate user with email and password. 
 Returns True if authentication is successful, False otherwise.

 signup(): Sign up a new user. 
 Returns user's authentication token and other details.

 signin(): Sign in an existing user. 
 Returns user's authentication token and other details.

 emailVerified(user): Check if user's email is verified. 
 Returns True if email is verified, False otherwise.

 setUsername(user, name): Add user's name to database. Returns None.

 updateUsername(user, name): Update user's name to database. Returns None.
'''
 

firebaseConfig = {
  "apiKey": "AIzaSyCRKlOgiKat20IdHzolR012qFffMek9vKU",
  "authDomain": "fir-2fb72.firebaseapp.com",
  "databaseURL": "https://fir-2fb72-default-rtdb.firebaseio.com",
  "projectId": "fir-2fb72",
  "storageBucket": "fir-2fb72.appspot.com",
  "messagingSenderId": "385173182800",
  "appId": "1:385173182800:web:b1abc52a221bbe86a3f455",
  "measurementId": "G-TD2RS83DT1"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database = firebase.database()

def processHttpError(e):
    """
    Process HTTP error.

    Args:
        e (requests.HTTPError): HTTP error.

    Returns:
        None
    """
    error_json = e.args[1]
    error = json.loads(error_json)['error']
    print("Error:", error['message'])
    return None

def authenticate_user(user):
    """
    Authenticate user with email and password.

    Args:
        email (str): User's email address.
        password (str): User's password.

    Returns:
        True if authentication is successful, False otherwise.
    """
    try:
        auth.send_email_verification(user['idToken'])
        return True
    except requests.HTTPError as e:
        processHttpError(e)
        return False

def signup():
    """
    Sign up a new user.

    Returns:
        dict: User's authentication token and other details.
        None: If signup fails.
    """
    try:
        email = input("Enter your email: ")

        # Check if email ends with @gmu.edu
        if not re.match(r"[^@]+@gmu\.edu", email):
            print("Please use a GMU email address.")
            return None
        
        password = input("Enter your password: ")      
        user = auth.create_user_with_email_and_password(email, password)
        print("Signup successful, verify your email to use app.")
        authenticate_user(user)
        return user
    except requests.HTTPError as e:
        return processHttpError(e)

def signin():
    """
    Sign in an existing user.

    Returns:
        dict: User's authentication token and other details.
        None: If signin fails.
    """
    try:
        email = input("Enter your email: ")
        password = input("Enter your password: ")      
        user = auth.sign_in_with_email_and_password(email, password)
        print("Signin successful!")
        return user
    except requests.HTTPError as e:
        return processHttpError(e)

def emailVerified(user):
    """
    Check if user's email is verified.

    Args:
        user (dict): User's authentication token and other details.

    Returns:
        bool: True if email is verified, False otherwise.
    """
    if user is None:        
        return False
    try:
        if auth.get_account_info(user['idToken'])['users'][0]['emailVerified']:
            return True
        else:
            return False
    except requests.HTTPError as e:
        return processHttpError(e)


def setUsername(user, name):
    """
    Add user's name to database for the first time.
    """
    try:
        email = auth.get_account_info(user['idToken'])['users'][0]['email']
        data = {"name": name, "email": email}
        database.child("users").child(user['localId']).set(data, user['idToken'])
    except Exception as e:
        print("Database Error", e)

def updateUsername(user, name):
    """
    Update user's name to database.
    """
    try:
        data = {"name": name}
        database.child("users").child(user['localId']).update(data, user['idToken'])
    except Exception as e:
        print("Database Error", e)

def main():
    """
    Main function.
    """
    running = True
    user = None
    while running:
        print("1. Sign up")
        print("2. Sign in")
        print("3. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            user = signup()
        elif choice == 2:
            user = signin()

            if user is None:
                continue

            if emailVerified(user):
                print("Email verified!")
                setUsername(user, input("Enter your username: "))
                print("Username added to database!")
            else:
                print("Email not verified!")
                user = None
        elif choice == 3:
            running = False
        else:
            print("Invalid choice!")



if __name__ == "__main__":
    main()