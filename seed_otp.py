import sqlite3

connection = sqlite3.connect("data/cybersafe.db")
cursor = connection.cursor()

questions = [
    (
        "OTP & Account Scams",
        "What should you do if someone claiming to be from your bank asks for your OTP?",
        "Give them the OTP if they know your name",
        "Never share the OTP",
        "Send the OTP only if they sound professional",
        "Share the OTP after checking their phone number",
        "B"
    ),
    (
        "OTP & Account Scams",
        "Why should you never share an OTP with another person?",
        "It can be used to authorize actions on your account",
        "It makes your phone slower",
        "It deletes your messages",
        "It changes your SIM card automatically",
        "A"
    ),
    (
        "OTP & Account Scams",
        "You receive an unexpected OTP that you did not request. What should you do?",
        "Share it with someone who asks",
        "Ignore the situation completely",
        "Check your account and contact the official service if necessary",
        "Post the OTP online",
        "C"
    ),
    (
        "OTP & Account Scams",
        "Which is a warning sign of an account scam?",
        "Someone creates urgency and asks for confidential information",
        "A normal account notification",
        "A security update from the official app",
        "Changing your password yourself",
        "A"
    ),
    (
        "OTP & Account Scams",
        "What is the safest way to contact your bank after receiving a suspicious call?",
        "Call the number provided by the caller",
        "Use the official bank app, website, or verified contact number",
        "Ask the caller for another number",
        "Reply to the suspicious message",
        "B"
    )
]

for question in questions:
    cursor.execute("""
        INSERT INTO quiz_questions
        (category, question_text, option_a, option_b, option_c, option_d, correct_option)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, question)

connection.commit()
connection.close()

print("OTP & Account Scams questions added successfully!")