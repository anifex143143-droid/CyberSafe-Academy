from data.database import get_connection


questions = [
    {
        "question": "Which password is the strongest?",
        "a": "A long, unique password used only for one account",
        "b": "password123",
        "c": "Your name and birth year",
        "d": "The same password used for every account",
        "correct": "A"
    },
    {
        "question": "Why should you avoid reusing the same password on multiple accounts?",
        "a": "It makes passwords harder to remember",
        "b": "A compromised password could put multiple accounts at risk",
        "c": "Websites reject reused passwords",
        "d": "It makes your internet slower",
        "correct": "B"
    },
    {
        "question": "What is a password manager mainly used for?",
        "a": "Increasing internet speed",
        "b": "Removing malware automatically",
        "c": "Storing and generating passwords securely",
        "d": "Blocking every phishing email",
        "correct": "C"
    },
    {
        "question": "What does multi-factor authentication (MFA) add to account security?",
        "a": "A second username",
        "b": "A faster login process",
        "c": "A stronger internet connection",
        "d": "An additional verification factor",
        "correct": "D"
    },
    {
        "question": "What should you do if you discover that your password has been exposed?",
        "a": "Change the password and avoid reusing it elsewhere",
        "b": "Keep using it until someone accesses the account",
        "c": "Share it with a friend for backup",
        "d": "Post it online to warn others",
        "correct": "A"
    }
]


connection = get_connection()

added = 0

for item in questions:

    existing = connection.execute("""
        SELECT id
        FROM quiz_questions
        WHERE question_text = ?
    """, (item["question"],)).fetchone()

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
    """, (
        "Password Security",
        item["question"],
        item["a"],
        item["b"],
        item["c"],
        item["d"],
        item["correct"]
    ))

    added += 1


connection.commit()
connection.close()

print(f"Password Security questions added: {added}")