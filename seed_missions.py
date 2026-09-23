from data.database import get_connection

connection = get_connection()

mission = connection.execute("""
    SELECT id
    FROM missions
    WHERE id = 1
""").fetchone()

if mission is None:
    print("Mission 1 not found.")
    connection.close()
    exit()

mission_id = mission["id"]

existing_question = connection.execute("""
    SELECT id
    FROM mission_questions
    WHERE mission_id = ?
""", (mission_id,)).fetchone()

if existing_question:
    print("Mission 1 questions already exist.")
    connection.close()
    exit()

cursor = connection.execute("""
    INSERT INTO mission_questions
    (
        mission_id,
        question_text,
        question_order
    )
    VALUES (?, ?, ?)
""", (
    mission_id,
    "What should you do?",
    1
))

question_id = cursor.lastrowid

options = [
    (
        question_id,
        "Verify the request through the organization's official website instead of using the email.",
        1
    ),
    (
        question_id,
        "Immediately follow the email's instructions because it says the situation is urgent.",
        0
    )
]

connection.executemany("""
    INSERT INTO mission_options
    (
        question_id,
        option_text,
        is_correct
    )
    VALUES (?, ?, ?)
""", options)

connection.commit()
connection.close()

print("Mission 1 question and options added successfully.")