from data.database import get_connection


MISSIONS = [
    {
        "title": "The Suspicious Email",
        "category": "Phishing Awareness",
        "difficulty": "Beginner",
        "description": "You receive an unexpected email asking you to urgently verify your account. Investigate the message and identify the warning signs.",
        "xp_reward": 100
    },
    {
        "title": "The Fake Support Call",
        "category": "Social Engineering",
        "difficulty": "Beginner",
        "description": "Someone claiming to be technical support asks for information about your account. Decide how you should respond.",
        "xp_reward": 120
    },
    {
        "title": "The Suspicious Download",
        "category": "Malware Awareness",
        "difficulty": "Intermediate",
        "description": "A file arrives from an unfamiliar source. Investigate the situation and decide the safest action.",
        "xp_reward": 150
    }
]


def seed_missions():
    connection = get_connection()

    for mission in MISSIONS:
        existing = connection.execute(
            "SELECT id FROM missions WHERE title = ?",
            (mission["title"],)
        ).fetchone()

        if not existing:
            connection.execute("""
                INSERT INTO missions
                (title, category, difficulty, description, xp_reward)
                VALUES (?, ?, ?, ?, ?)
            """, (
                mission["title"],
                mission["category"],
                mission["difficulty"],
                mission["description"],
                mission["xp_reward"]
            ))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    seed_missions()
    print("Missions added successfully.")