import sqlite3
from pathlib import Path


# =========================
# DATABASE LOCATION
# =========================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cybersafe.db"


# =========================
# DATABASE CONNECTION
# =========================

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# =========================
# INITIALIZE DATABASE
# =========================

def initialize_database():

    connection = get_connection()

    # =========================
    # USERS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            security_score REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # =========================
    # MISSIONS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            description TEXT NOT NULL,
            xp_reward INTEGER DEFAULT 0
        )
    """)

    # =========================
    # MISSION QUESTIONS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS mission_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mission_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            question_order INTEGER DEFAULT 1,
            FOREIGN KEY (mission_id) REFERENCES missions(id)
        )
    """)

    # =========================
    # MISSION OPTIONS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS mission_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            option_text TEXT NOT NULL,
            is_correct INTEGER DEFAULT 0,
            FOREIGN KEY (question_id) REFERENCES mission_questions(id)
        )
    """)

    # =========================
    # MISSION ATTEMPTS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS mission_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mission_id INTEGER NOT NULL,
            score INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (mission_id) REFERENCES missions(id)
        )
    """)

    # =========================
    # ACHIEVEMENTS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            xp_reward INTEGER DEFAULT 0
        )
    """)

    # =========================
    # USER ACHIEVEMENTS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_id INTEGER NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, achievement_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (achievement_id) REFERENCES achievements(id)
        )
    """)

    # =========================
    # USER LEARNING PROGRESS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            score REAL DEFAULT 0,
            UNIQUE(user_id, category),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # =========================
    # QUIZ QUESTIONS
    # =========================
    #
    # This is the new Question Bank.
    #

    connection.execute("""
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL,
            explanation TEXT,
            difficulty TEXT DEFAULT 'Beginner'
        )
    """)

        # =========================
    # PHISHING SIMULATIONS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS phishing_simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            sender TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            difficulty TEXT DEFAULT 'Beginner',
            xp_reward INTEGER DEFAULT 100
        )
    """)

    # =========================
    # PHISHING CLUES
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS phishing_clues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER NOT NULL,
            clue_text TEXT NOT NULL,
            question_text TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            FOREIGN KEY (simulation_id)
                REFERENCES phishing_simulations(id)
        )
    """)

    # =========================
    # PHISHING ATTEMPTS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS phishing_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            simulation_id INTEGER NOT NULL,
            score INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            xp_awarded INTEGER DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users(id),
            FOREIGN KEY (simulation_id)
                REFERENCES phishing_simulations(id)
        )
    """)

        # =========================
    # MALWARE SIMULATION
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS malware_simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            file_name TEXT NOT NULL,
            source TEXT NOT NULL,
            description TEXT NOT NULL,
            difficulty TEXT DEFAULT 'Intermediate',
            xp_reward INTEGER DEFAULT 150
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS malware_clues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER NOT NULL,
            clue_text TEXT NOT NULL,
            question_text TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            FOREIGN KEY (simulation_id)
                REFERENCES malware_simulations(id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS malware_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            simulation_id INTEGER NOT NULL,
            score INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            xp_awarded INTEGER DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users(id),
            FOREIGN KEY (simulation_id)
                REFERENCES malware_simulations(id)
        )
    """)


    connection.execute("""
        CREATE TABLE IF NOT EXISTS social_engineering_simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            scenario_type TEXT NOT NULL,
            description TEXT NOT NULL,
            difficulty TEXT DEFAULT 'Intermediate',
            xp_reward INTEGER DEFAULT 150
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS social_engineering_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            question_text TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            FOREIGN KEY (simulation_id)
                REFERENCES social_engineering_simulations(id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS social_engineering_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            simulation_id INTEGER NOT NULL,
            score INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            xp_awarded INTEGER DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users(id),
            FOREIGN KEY (simulation_id)
                REFERENCES social_engineering_simulations(id)
        )
    """)


 
    # =========================
    # QUIZ ATTEMPTS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0,
            percentage REAL DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # =========================
    # QUIZ ANSWERS
    # =========================

    connection.execute("""
        CREATE TABLE IF NOT EXISTS quiz_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            selected_option TEXT,
            is_correct INTEGER DEFAULT 0,
            FOREIGN KEY (attempt_id) REFERENCES quiz_attempts(id),
            FOREIGN KEY (question_id) REFERENCES quiz_questions(id)
        )
    """)

        # =========================
    # DEFAULT PHISHING SIMULATION
    # =========================

    phishing_simulation = connection.execute("""
        SELECT id
        FROM phishing_simulations
        WHERE title = ?
    """, (
        "Suspicious Email Investigation",
    )).fetchone()

    if phishing_simulation is None:

        cursor = connection.execute("""
            INSERT INTO phishing_simulations
            (
                title,
                sender,
                subject,
                body,
                difficulty,
                xp_reward
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Suspicious Email Investigation",

            "security-alert@micros0ft-support.com",

            "URGENT: Your account will be suspended",

            """Dear User,

We detected unusual activity on your account.

Your account will be permanently suspended within 24 hours unless you verify your identity immediately.

Click the verification link below and confirm your password:

[ VERIFY MY ACCOUNT ]

Failure to complete verification will result in permanent account suspension.

Microsoft Security Team""",

            "Beginner",

            100
        ))

        simulation_id = cursor.lastrowid

       
        clues = [

    (
        "security-alert@micros0ft-support.com",
        "Sender Check: Does this sender address appear to belong to the real organization?",
        "suspicious",
        "Look closely at the domain name. The word 'micros0ft' uses the number zero instead of the letter 'o'. Small changes like this are commonly used in look-alike phishing domains."
    ),

    (
        "URGENT: Your account will be suspended",
        "Pressure Check: What is the main warning sign created by this subject line?",
        "suspicious",
        "The message creates urgency and fear. Phishing messages often pressure people to act quickly before they stop and verify the request."
    ),

    (
        "[ VERIFY MY ACCOUNT ]",
        "Link Safety Check: What should you do before using a verification link from a suspicious email?",
        "suspicious",
        "Do not blindly follow the email link. Instead, independently open the organization's official website or use another trusted contact method."
    ),

    (
        "Click the verification link and confirm your password.",
        "Credential Check: Is requesting your password through an email verification link a warning sign?",
        "suspicious",
        "Requests for passwords or other sensitive information through unexpected email links should be treated as a major warning sign."
    ),

(
    "Your account will be permanently suspended within 24 hours.",
    "Response Check: What should you do after identifying this message as phishing?",
    "report",
    "Do not click the link or reply to the sender. Report the message as phishing and verify your account through the organization's official website or app if necessary."
)
]

       

        for clue_text, question_text, correct_answer, explanation in clues:

            connection.execute("""
                INSERT INTO phishing_clues
                (
                    simulation_id,
                    clue_text,
                    question_text,
                    correct_answer,
                    explanation
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                simulation_id,
                clue_text,
                question_text,
                correct_answer,
                explanation
            ))

    # =========================
    # DEFAULT ACHIEVEMENTS
    # =========================

    achievements = [
        (
            "First Mission",
            "Complete your first cybersecurity mission.",
            50
        ),
        (
            "Cyber Beginner",
            "Earn 250 XP.",
            75
        ),
        (
            "Mission Master",
            "Complete at least 3 missions with a perfect score.",
            150
        )
    ]

    for name, description, xp_reward in achievements:
        connection.execute("""
            INSERT OR IGNORE INTO achievements
            (name, description, xp_reward)
            VALUES (?, ?, ?)
        """, (name, description, xp_reward))

    # =========================
    # DEFAULT MALWARE SIMULATION
    # =========================

    malware_simulation = connection.execute("""
        SELECT id FROM malware_simulations
        WHERE title = ?
    """, ("Suspicious Download Investigation",)).fetchone()

    if malware_simulation is None:
        cursor = connection.execute("""
            INSERT INTO malware_simulations
            (title, file_name, source, description, difficulty, xp_reward)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Suspicious Download Investigation",
            "Free_Game_Setup.exe",
            "Unknown download website",
            "Investigate a suspicious downloaded file and identify the warning signs of possible malware.",
            "Intermediate",
            150
        ))

        malware_simulation_id = cursor.lastrowid

        malware_clues = [
            (
                "The file is named Free_Game_Setup.exe and came from an unknown download website.",
                "What should you consider first?",
                "suspicious_source",
                "Unknown download sources and unexpected executable files are important warning signs."
            ),
            (
                "The website says: 'Disable Windows Security before installing or the setup will fail.'",
                "What is the safest response?",
                "do_not_disable",
                "Legitimate software should not require you to disable security protections to install."
            ),
            (
                "The downloaded file asks for administrator permission immediately.",
                "What should you do?",
                "verify_first",
                "Unexpected administrator requests should be verified before allowing the program to run."
            ),
            (
                "Your computer becomes unusually slow immediately after running the file.",
                "What is the safest action?",
                "stop_and_report",
                "Unexpected performance changes after running an unknown file can indicate suspicious activity."
            ),
            (
                "A security warning appears saying the file may be unsafe.",
                "What should you do?",
                "do_not_run",
                "A security warning should not be ignored just because the file appears useful."
            )
        ]

        for clue_text, question_text, correct_answer, explanation in malware_clues:
            connection.execute("""
                INSERT INTO malware_clues
                (simulation_id, clue_text, question_text, correct_answer, explanation)
                VALUES (?, ?, ?, ?, ?)
            """, (
                malware_simulation_id,
                clue_text,
                question_text,
                correct_answer,
                explanation
            ))

    social_simulation = connection.execute("""
        SELECT id
        FROM social_engineering_simulations
        WHERE title = ?
    """, ("Fake Bank OTP Scam",)).fetchone()

    if social_simulation is None:
        cursor = connection.execute("""
            INSERT INTO social_engineering_simulations
            (title, scenario_type, description, difficulty, xp_reward)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "Fake Bank OTP Scam",
            "OTP Scam",
            "Investigate a suspicious bank message and decide how to respond safely to an OTP request.",
            "Intermediate",
            150
        ))

        social_simulation_id = cursor.lastrowid

        social_questions = [
            (
                "Your phone receives: 'URGENT: Your bank account will be blocked today. Send the OTP you receive to this number immediately.'",
                "What is the safest response?",
                "do_not_share",
                "Never share an OTP with someone who contacts you unexpectedly. A genuine bank representative should not ask you to reveal your OTP."
            ),
            (
                "The message contains a shortened link and says you must verify your account immediately.",
                "What should you do?",
                "do_not_click",
                "Urgent messages combined with unexpected links are common warning signs. Do not click the link; verify through the bank's official channel instead."
            ),
            (
                "The caller says they are from your bank and already knows your name and some account details.",
                "Does this prove the caller is genuine?",
                "no",
                "Knowing some personal information does not prove someone's identity. Scammers may obtain or already know basic information."
            ),
            (
                "The caller asks for the OTP that just arrived on your phone.",
                "What should you do?",
                "end_call",
                "Do not reveal the OTP. End the suspicious call and contact the bank using an official phone number or app."
            ),
            (
                "You are unsure whether the message is really from your bank.",
                "What is the safest way to verify it?",
                "official_channel",
                "Use the bank's official app, website, or phone number rather than replying to the suspicious message."
            )
        ]

        for message_text, question_text, correct_answer, explanation in social_questions:
            connection.execute("""
                INSERT INTO social_engineering_questions
                (simulation_id, message_text, question_text, correct_answer, explanation)
                VALUES (?, ?, ?, ?, ?)
            """, (
                social_simulation_id,
                message_text,
                question_text,
                correct_answer,
                explanation
            ))



    # =========================
    # SAVE AND CLOSE
    # =========================

    connection.commit()
    connection.close()


# =========================
# RUN DIRECTLY
# =========================

if __name__ == "__main__":
    initialize_database()
    print("CyberSafe Academy database initialized successfully.")