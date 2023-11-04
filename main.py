import pyrebase


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

def authenticate_user(email, password):
    """
    Authenticate user with email and password.

    Args:
        email (str): User's email address.
        password (str): User's password.

    Returns:
        dict: User's authentication token and other details.
    """
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        auth.send_email_verification(user['idToken'])
        return user
    except Exception as e:
        print("Authentication failed")

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
        print("Signup successful!")
        authenticate_user(email, password)
        return user
    except Exception as e:
        print("Signup failed: ", e)

print(signup())


