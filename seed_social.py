import sqlite3

connection = sqlite3.connect("data/cybersafe.db")

questions = [
    (
        "Social Engineering",
        "Someone calls claiming to be from your bank and asks for your OTP. What should you do?",
        "Share the OTP if they know your name",
        "Refuse and contact the bank through an official channel",
        "Give the OTP but change your password later",
        "Ask them to call back later and then share it",
        "B"
    ),
    (
        "Social Engineering",
        "What is the main goal of social engineering?",
        "To physically damage a computer",
        "To manipulate people into revealing information or taking an unsafe action",
        "To increase internet speed",
        "To improve password strength",
        "B"
    ),
    (
        "Social Engineering",
        "You receive a message saying you won a prize and must act immediately. What is the safest response?",
        "Click the link quickly",
        "Share your personal details",
        "Verify the offer through an official source",
        "Forward it to friends",
        "C"
    ),
    (
        "Social Engineering",
        "Which behavior is a common warning sign of a social-engineering attempt?",
        "A request creates unnecessary urgency or pressure",
        "A website uses a normal login page",
        "A friend sends a normal message",
        "A computer receives a software update",
        "A"
    ),
    (
        "Social Engineering",
        "Why should you avoid sharing confidential information with an unexpected caller?",
        "The caller might be trying to manipulate you",
        "Calls always contain malware",
        "Phone numbers cannot be trusted",
        "Confidential information is never useful",
        "A"
    )
]



for question in questions:

    existing = connection.execute("""
        SELECT id
        FROM quiz_questions
        WHERE category = ?
        AND question_text = ?
    """, (
        question[0],
        question[1]
    )).fetchone()

    if existing:
        continue

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

print("Social Engineering questions added:", len(questions))