import sqlite3

connection = sqlite3.connect("data/cybersafe.db")

questions = [
    (
        "Web Security",
        "What does HTTPS primarily help protect?",
        "Data exchanged between your browser and the website",
        "Your device battery",
        "Your internet speed",
        "Your screen brightness",
        "A"
    ),
    (
        "Web Security",
        "What is phishing on a website commonly designed to do?",
        "Trick users into revealing sensitive information",
        "Increase computer storage",
        "Improve website performance",
        "Update the monitor",
        "A"
    ),
    (
        "Web Security",
        "What should you check before entering sensitive information on a website?",
        "The website address and whether the connection is secure",
        "The number of images on the page",
        "The background color",
        "The number of advertisements",
        "A"
    ),
    (
        "Web Security",
        "Why should you avoid clicking suspicious links?",
        "They may lead to fraudulent or harmful websites",
        "They always improve security",
        "They automatically update your browser",
        "They increase your storage space",
        "A"
    ),
    (
        "Web Security",
        "What is a safer response to an unexpected login or account-reset link?",
        "Open the official website directly instead of using the unexpected link",
        "Click it immediately",
        "Enter your password to check it",
        "Forward it to everyone",
        "A"
    )
]

for question in questions:
    connection.execute("""
        INSERT INTO quiz_questions (
            category,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_option
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, question)

connection.commit()
connection.close()

print("Web Security questions added:", len(questions))