from data.database import get_connection


QUESTIONS = [
    {
        "category": "Cybersecurity Fundamentals",
        "question_text": "What is the main goal of cybersecurity?",
        "option_a": "To make computers run faster",
        "option_b": "To protect systems, networks, devices, and data from threats",
        "option_c": "To increase internet speed",
        "option_d": "To create computer games",
        "correct_option": "B",
        "explanation": "Cybersecurity focuses on protecting systems, networks, devices, and data from unauthorized access, misuse, damage, and other security threats.",
        "difficulty": "Beginner"
    },
    {
        "category": "Cybersecurity Fundamentals",
        "question_text": "Which of the following is a common cybersecurity threat?",
        "option_a": "Phishing",
        "option_b": "Screen brightness",
        "option_c": "File compression",
        "option_d": "Keyboard shortcuts",
        "correct_option": "A",
        "explanation": "Phishing is a common cybersecurity threat that attempts to trick people into revealing information or taking unsafe actions.",
        "difficulty": "Beginner"
    },
    {
        "category": "Cybersecurity Fundamentals",
        "question_text": "What should you do if you receive a suspicious email asking you to verify your account urgently?",
        "option_a": "Click the link immediately",
        "option_b": "Reply with your password",
        "option_c": "Verify the request through an official trusted channel",
        "option_d": "Forward your password to the sender",
        "correct_option": "C",
        "explanation": "Urgency is commonly used in phishing attempts. Verify unexpected requests through an official website or trusted contact method rather than using links in the suspicious message.",
        "difficulty": "Beginner"
    },
    {
        "category": "Cybersecurity Fundamentals",
        "question_text": "Which password is generally stronger?",
        "option_a": "password123",
        "option_b": "12345678",
        "option_c": "YourName2004",
        "option_d": "A long, unique passphrase that is difficult to guess",
        "correct_option": "D",
        "explanation": "Long, unique passwords or passphrases are generally harder to guess. Reusing passwords across accounts also increases risk.",
        "difficulty": "Beginner"
    },
    {
        "category": "Cybersecurity Fundamentals",
        "question_text": "Why is multi-factor authentication useful?",
        "option_a": "It adds another verification step when signing in",
        "option_b": "It removes the need for any password",
        "option_c": "It makes your computer physically faster",
        "option_d": "It prevents every possible cyberattack",
        "correct_option": "A",
        "explanation": "Multi-factor authentication adds an additional verification factor, making account access harder when a password alone is compromised.",
        "difficulty": "Beginner"
    }
]


def seed_quizzes():
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

    print(f"Quiz seeding complete. Added {inserted} new questions.")


if __name__ == "__main__":
    seed_quizzes()