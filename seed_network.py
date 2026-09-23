import sqlite3

connection = sqlite3.connect("data/cybersafe.db")

questions = [
    (
        "Network Security",
        "What is the main purpose of a firewall?",
        "To protect a network by controlling incoming and outgoing traffic",
        "To make the internet faster",
        "To store passwords",
        "To create social media accounts",
        "A"
    ),
    (
        "Network Security",
        "Which connection is generally safer when accessing sensitive information on public Wi-Fi?",
        "An encrypted connection such as HTTPS",
        "Any connection without a password",
        "A random website",
        "An unknown file-sharing service",
        "A"
    ),
    (
        "Network Security",
        "What does HTTPS help provide?",
        "Encryption between the browser and website",
        "Unlimited internet speed",
        "Protection from every type of malware",
        "Automatic password recovery",
        "A"
    ),
    (
        "Network Security",
        "Why should you avoid connecting to unknown public Wi-Fi networks?",
        "They may expose your data to security risks",
        "They always have faster speeds",
        "They automatically install antivirus software",
        "They increase your device storage",
        "A"
    ),
    (
        "Network Security",
        "What is the safest action if your device shows an unexpected network security warning?",
        "Stop and investigate the warning before continuing",
        "Ignore it immediately",
        "Disable all security settings",
        "Share the warning with strangers",
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

print("Network Security questions added:", len(questions))