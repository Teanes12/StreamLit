import streamlit as st
import openai
import datetime

# Get your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state for user accounts and login status
if 'users' not in st.session_state:
    st.session_state['users'] = {}  # Dictionary to store usernames and passwords
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = ""
if 'leaderboard' not in st.session_state:
    st.session_state['leaderboard'] = []  # Leaderboard list to store scores

# Function to register a new user
def register_user(username, password):
    if username in st.session_state['users']:
        st.warning("Username already exists. Please choose another one.")
    else:
        st.session_state['users'][username] = password
        st.success("Registration successful! You can now log in.")

# Function to log in a user
def login_user(username, password):
    if username in st.session_state['users'] and st.session_state['users'][username] == password:
        st.session_state['logged_in'] = True
        st.session_state['current_user'] = username
        st.success(f"Welcome, {username}!")
    else:
        st.error("Incorrect username or password.")

# Function to log out a user
def logout_user():
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = ""
    st.success("You have been logged out.")

# Function to generate a random phishing scenario using OpenAI API
def generate_scenario():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a cybersecurity assistant. Your role is to provide users with phishing scenarios and elaborate on their answers, guiding them in understanding the implications of phishing."
            },
            {
                "role": "user",
                "content": "Generae a phishing email scenario."
            },
        ],
        temperature=1.3,
        max_tokens=2000,
    )
    return response['choices'][0]['message']['content']

# Function to generate elaboration based on user's answer
def generate_elaboration(scenario_text, answer):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a cybersecurity expert providing feedback on user responses."
            },
            {
                "role": "user",
                "content": f"The user answered '{answer}' for the scenario: '{scenario_text}'. Please provide feedback and elaborate on the implications of phishing."
            },
        ],
        temperature=1.3,
        max_tokens=2000,
    )
    return response['choices'][0]['message']['content']

# Function to play the game
def play_game():
    st.header("Phishing Awareness Game")
    st.write("Identify if the given email scenario is a phishing attempt or not.")

    # Generate a random phishing scenario
    scenario_text = generate_scenario()
    st.write(scenario_text)

    # Collect user answer
    answer = st.radio("Is this email a phishing attempt?", ("Yes", "No"))

    # Analyze response
    if st.button("Submit Answer"):
        # Mock phishing determination for demonstration purposes
        is_phishing = "phishing" in scenario_text.lower()  # Simple check (for demo purposes)

        if (answer == "Yes" and is_phishing) or (answer == "No" and not is_phishing):
            st.success("Correct! You've earned 10 points.")
            score = 10
        else:
            st.error("Incorrect. No points earned this time.")
            score = 0

        # Elaborate on the user's answer
        if st.session_state['logged_in']:
            elaboration = generate_elaboration(scenario_text, answer)
            st.write(elaboration)

        # Record the score with a timestamp if logged in
        if st.session_state['logged_in']:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            username = st.session_state['current_user']
            st.session_state['leaderboard'].append((username, score, timestamp))
            st.write("Your answer has been recorded.")

# Function to show the leaderboard
def show_leaderboard():
    st.header("Leaderboard")
    if st.session_state['leaderboard']:
        leaderboard_sorted = sorted(st.session_state['leaderboard'], key=lambda x: x[1], reverse=True)
        st.write("### Top Scores")
        for i, (user, score, timestamp) in enumerate(leaderboard_sorted, start=1):
            st.write(f"{i}. **{user}** - {score} points (Answered at: {timestamp})")
    else:
        st.write("No scores recorded yet.")

# Main app flow
st.title("Phishing Awareness Game with Leaderboard")

# User Authentication
st.sidebar.header("User Authentication")
if st.session_state['logged_in']:
    st.sidebar.write(f"Logged in as: {st.session_state['current_user']}")
    if st.sidebar.button("Logout"):
        logout_user()
else:
    login_username = st.sidebar.text_input("Username")
    login_password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        login_user(login_username, login_password)

    # Registration section
    st.sidebar.subheader("Register")
    register_username = st.sidebar.text_input("Register Username")
    register_password = st.sidebar.text_input("Register Password", type="password")
    if st.sidebar.button("Register"):
        register_user(register_username, register_password)

# Game and leaderboard are shown only if logged in
if st.session_state['logged_in']:
    play_game()
    show_leaderboard()
else:
    st.write("Please log in or register to play the game.")
