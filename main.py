import pyrebase
import requests
import json

firebaseConfig = {
  "apiKey": "AIzaSyCRKlOgiKat20IdHzolR012qFffMek9vKU",
  "authDomain": "fir-2fb72.firebaseapp.com",
  "databaseURL": "https://fir-2fb72.firebaseio.com",
  "projectId": "fir-2fb72",
  "storageBucket": "fir-2fb72.appspot.com",
  "messagingSenderId": "385173182800",
  "appId": "1:385173182800:web:b1abc52a221bbe86a3f455",
  "measurementId": "G-TD2RS83DT1"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

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
    except Exception as e:
        print("Authentication failed")
        return False

def signup():
    """
    Sign up a new user.

    Returns:
        dict: User's authentication token and other details.
    """
    try:
        email = input("Enter your email: ")
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
            else:
                print("Email not verified!")
                user = None
        elif choice == 3:
            running = False
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()