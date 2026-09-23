from data.database import get_connection


QUESTIONS = [
    {
        "category": "Phishing Awareness",
        "question_text": "Which is a common warning sign of a phishing email?",
        "option_a": "A message that creates urgency and asks you to verify an account",
        "option_b": "A routine message you expected from a known service",
        "option_c": "A notification you received through the official app",
        "option_d": "A message with information you already confirmed",
        "correct_option": "A",
        "explanation": "Phishing messages often use urgency or fear to pressure people into taking unsafe actions.",
        "difficulty": "Beginner"
    },
    {
        "category": "Phishing Awareness",
        "question_text": "You receive an unexpected email containing a link asking you to log in. What is the safest first step?",
        "option_a": "Click the link and check whether the page looks real",
        "option_b": "Forward the email to friends to ask what they think",
        "option_c": "Open the service through its official website or app instead",
        "option_d": "Enter your password but not your username",
        "correct_option": "C",
        "explanation": "Using the official website or app avoids relying on an unexpected link in a message.",
        "difficulty": "Beginner"
    },
    {
        "category": "Phishing Awareness",
        "question_text": "An email says your account will be suspended within 10 minutes unless you act immediately. What should make you cautious?",
        "option_a": "The message contains normal information",
        "option_b": "The message uses strong urgency to pressure you",
        "option_c": "The message has a greeting",
        "option_d": "The message contains a date",
        "correct_option": "B",
        "explanation": "Strong urgency is commonly used in phishing attempts to pressure people into acting before they verify the request.",
        "difficulty": "Beginner"
    },
    {
        "category": "Phishing Awareness",
        "question_text": "What should you check when evaluating an unexpected message claiming to come from a company?",
        "option_a": "Whether the sender and request are consistent with the official service",
        "option_b": "Whether the message uses colorful formatting",
        "option_c": "Whether the message contains many words",
        "option_d": "Whether the message has a large logo",
        "correct_option": "A",
        "explanation": "Checking the sender and independently verifying the request can help identify suspicious messages.",
        "difficulty": "Beginner"
    },
    {
        "category": "Phishing Awareness",
        "question_text": "You suspect that an unexpected email is phishing. What is the safest response?",
        "option_a": "Reply and provide the requested information",
        "option_b": "Click the link to investigate the sender",
        "option_c": "Ignore the warning and continue normally",
        "option_d": "Avoid interacting with the message and verify the request through an official channel",
        "correct_option": "D",
        "explanation": "Avoid interacting with suspicious messages and independently verify important requests through trusted official channels.",
        "difficulty": "Beginner"
    }
]


connection = get_connection()

inserted = 0

for question in QUESTIONS:

    existing = connection.execute("""
        SELECT id
        FROM quiz_questions
        WHERE category = ?
        AND question_text = ?
    """, (
        question["category"],
        question["question_text"]
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
            correct_option,
            explanation,
            difficulty
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        question["category"],
        question["question_text"],
        question["option_a"],
        question["option_b"],
        question["option_c"],
        question["option_d"],
        question["correct_option"],
        question["explanation"],
        question["difficulty"]
    ))

    inserted += 1


connection.commit()
connection.close()

print(f"Phishing Awareness questions added: {inserted}")