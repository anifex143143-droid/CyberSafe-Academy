from data.database import get_connection

connection = get_connection()

questions = [
    (
        "Encryption & Hashing",
        "What is the main purpose of encryption?",
        "To protect data by converting it into an unreadable form",
        "To delete data permanently",
        "To make a computer faster",
        "To create stronger passwords automatically",
        "A"
    ),
    (
        "Encryption & Hashing",
        "Which key is used to decrypt data in symmetric encryption?",
        "A completely different public key",
        "The same secret key used for encryption",
        "The user's password only",
        "No key is required",
        "B"
    ),
    (
        "Encryption & Hashing",
        "What is hashing mainly used for?",
        "Reversibly hiding data",
        "Compressing videos",
        "Creating a fixed-length representation of data",
        "Increasing internet speed",
        "C"
    ),
    (
        "Encryption & Hashing",
        "Which of these is commonly used as a secure password-hashing algorithm?",
        "SHA-1",
        "MD5",
        "bcrypt",
        "Base64",
        "C"
    ),
    (
        "Encryption & Hashing",
        "What is an important difference between encryption and hashing?",
        "Encryption can be reversed with the correct key, while hashing is designed to be one-way",
        "Hashing always uses two keys",
        "Encryption can only be used for passwords",
        "They are exactly the same",
        "A"
    )
]

for question in questions:
    connection.execute(
        """
        INSERT INTO quiz_questions
        (category, question_text, option_a, option_b, option_c, option_d, correct_option)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        question
    )

connection.commit()
connection.close()

print("Encryption & Hashing questions added: 5")