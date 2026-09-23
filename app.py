from flask import Flask, render_template, request, redirect, url_for
from data.database import initialize_database, get_connection
import joblib
import pandas as pd

app = Flask(__name__)

initialize_database()


def calculate_level(xp):
    if xp < 250:
        return 1
    elif xp < 600:
        return 2
    elif xp < 1000:
        return 3
    elif xp < 1500:
        return 4
    elif xp < 2200:
        return 5
    elif xp < 3000:
        return 6
    elif xp < 4000:
        return 7
    elif xp < 5500:
        return 8
    elif xp < 7500:
        return 9
    else:
        return 10


def update_user_level(connection, user_id):
    user = connection.execute("""
        SELECT xp
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    if user:
        level = calculate_level(user["xp"])

        connection.execute("""
            UPDATE users
            SET level = ?
            WHERE id = ?
        """, (level, user_id))

def update_security_score(connection, user_id):

    scores = []

    # =========================
    # NORMAL MISSION SCORES
    # =========================

    mission_attempts = connection.execute("""
        SELECT score
        FROM mission_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    scores.extend(
        attempt["score"]
        for attempt in mission_attempts
    )


    # =========================
    # PHISHING SIMULATION SCORES
    # =========================

    phishing_attempts = connection.execute("""
        SELECT score
        FROM phishing_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    scores.extend(
        attempt["score"]
        for attempt in phishing_attempts
    )


    # =========================
    # MALWARE SIMULATION SCORES
    # =========================

    malware_attempts = connection.execute("""
        SELECT score
        FROM malware_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    scores.extend(
        attempt["score"]
        for attempt in malware_attempts
    )


    # =========================
    # SOCIAL ENGINEERING / OTP SCORES
    # =========================

    social_engineering_attempts = connection.execute("""
        SELECT score
        FROM social_engineering_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    scores.extend(
        attempt["score"]
        for attempt in social_engineering_attempts
    )

    # =========================
    # CALCULATE SECURITY SCORE
    # =========================

    if not scores:
        security_score = 0
    else:
        security_score = round(
            sum(scores) / len(scores)
        )


    connection.execute("""
        UPDATE users
        SET security_score = ?
        WHERE id = ?
    """, (
        security_score,
        user_id
    ))
    

def predict_security_risk(connection, user_id):

    user = connection.execute("""
        SELECT
            xp,
            security_score
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    if not user:
        return {
            "risk_level": "Unknown",
            "risk_score": 0,
            "message": "No user data available."
        }

    security_score = user["security_score"] or 0

    quiz_stats = connection.execute("""
        SELECT
            AVG(percentage) AS average_percentage
        FROM quiz_attempts
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    quiz_accuracy = round(
        quiz_stats["average_percentage"] or 0
    )


    # =========================
    # MISSION + SIMULATION ACCURACY
    # =========================

    mission_scores = []

    normal_missions = connection.execute("""
        SELECT score
        FROM mission_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    mission_scores.extend(
        attempt["score"]
        for attempt in normal_missions
    )


    phishing_scores = connection.execute("""
        SELECT score
        FROM phishing_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    mission_scores.extend(
        attempt["score"]
        for attempt in phishing_scores
    )


    malware_scores = connection.execute("""
        SELECT score
        FROM malware_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    mission_scores.extend(
        attempt["score"]
        for attempt in malware_scores
    )

    # =========================
    # SOCIAL ENGINEERING / OTP SCORES
    # =========================

    social_engineering_scores = connection.execute("""
        SELECT score
        FROM social_engineering_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    mission_scores.extend(
        attempt["score"]
        for attempt in social_engineering_scores
    )

    if mission_scores:
        mission_accuracy = round(
            sum(mission_scores) / len(mission_scores)
        )
    else:
        mission_accuracy = 0
    learning_stats = connection.execute("""
        SELECT
            SUM(
                CASE
                    WHEN completed = 1 THEN 1
                    ELSE 0
                END
            ) AS completed_categories
        FROM user_progress
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    completed_categories = learning_stats["completed_categories"] or 0

    total_categories = connection.execute("""
        SELECT COUNT(DISTINCT category)
        FROM quiz_questions
    """).fetchone()[0]

    learning_percentage = 0

    if total_categories > 0:
        learning_percentage = round(
            (completed_categories / total_categories) * 100
        )


    # =========================
    # ML RISK PREDICTION
    # =========================

    model = joblib.load(
        "ml/risk_model.pkl"
    )

    input_data = pd.DataFrame([{
        "security_score": security_score,
        "quiz_accuracy": quiz_accuracy,
        "mission_accuracy": mission_accuracy,
        "learning_percentage": learning_percentage
    }])

    # Get ML prediction
    risk_level = model.predict(
        input_data
    )[0]

    # Get probability for each risk class
    risk_probabilities = model.predict_proba(
        input_data
    )[0]

    class_probabilities = dict(
        zip(
            model.classes_,
            risk_probabilities
        )
    )

    # Convert ML probabilities into a risk score
    risk_score = round(
        class_probabilities.get("Low", 0) * 20
        + class_probabilities.get("Medium", 0) * 55
        + class_probabilities.get("High", 0) * 90
    )

    risk_score = max(
        0,
        min(100, risk_score)
    )

    if risk_level == "High":
        message = "More cybersecurity practice is recommended."

    elif risk_level == "Medium":
        message = "Keep practicing to strengthen your security awareness."

    else:
        message = "Your current security awareness indicators are strong."
    
    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "message": message
    }

def check_and_award_achievements(connection, user_id):
    user = connection.execute("""
        
        SELECT xp
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    if not user:
        return

    completed_missions = connection.execute("""
        SELECT COUNT(DISTINCT mission_id)
        FROM mission_attempts
        WHERE user_id = ?
        AND completed = 1
        AND score = 100
    """, (user_id,)).fetchone()[0]

    achievements = connection.execute("""
        SELECT *
        FROM achievements
    """).fetchall()

    for achievement in achievements:

        earned = connection.execute("""
            SELECT id
            FROM user_achievements
            WHERE user_id = ?
            AND achievement_id = ?
        """, (
            user_id,
            achievement["id"]
        )).fetchone()

        if earned:
            continue

        should_award = False

        if achievement["name"] == "First Mission" and completed_missions >= 1:
            should_award = True

        elif achievement["name"] == "Cyber Beginner" and user["xp"] >= 250:
            should_award = True

        elif achievement["name"] == "Mission Master" and completed_missions >= 3:
            should_award = True

        if should_award:

            connection.execute("""
                INSERT INTO user_achievements
                (
                    user_id,
                    achievement_id
                )
                VALUES (?, ?)
            """, (
                user_id,
                achievement["id"]
            ))

            connection.execute("""
                UPDATE users
                SET xp = xp + ?
                WHERE id = ?
            """, (
                achievement["xp_reward"],
                user_id
            ))


def get_or_create_demo_user(connection):
    user = connection.execute("""
        SELECT *
        FROM users
        WHERE username = ?
    """, ("DemoUser",)).fetchone()

    if user is None:
        connection.execute("""
            INSERT INTO users (username)
            VALUES (?)
        """, ("DemoUser",))

        connection.commit()

        user = connection.execute("""
            SELECT *
            FROM users
            WHERE username = ?
        """, ("DemoUser",)).fetchone()

    return user


@app.route("/")
def home():
    connection = get_connection()

    user = get_or_create_demo_user(connection)

    completed_missions = connection.execute("""
        SELECT COUNT(DISTINCT mission_id)
        FROM mission_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user["id"],)).fetchone()[0]

    total_missions = connection.execute("""
        SELECT COUNT(*)
        FROM missions
    """).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        user=user,
        completed_missions=completed_missions,
        total_missions=total_missions
    )


@app.route("/missions")
def missions():
    connection = get_connection()

    missions_data = connection.execute("""
        SELECT
            id,
            title,
            category,
            difficulty,
            description,
            xp_reward
        FROM missions
        ORDER BY id
    """).fetchall()

    connection.close()

    return render_template(
        "missions.html",
        missions=missions_data
    )

@app.route("/mission/<int:mission_id>")

def mission(mission_id):
    connection = get_connection()

    mission_data = connection.execute("""
        SELECT *
        FROM missions
        WHERE id = ?
    """, (mission_id,)).fetchone()

    if mission_data is None:
        connection.close()
        return "Mission not found", 404

    questions = connection.execute("""
        SELECT *
        FROM mission_questions
        WHERE mission_id = ?
        ORDER BY question_order, id
    """, (mission_id,)).fetchall()

    questions_with_options = []

    for question in questions:
        options = connection.execute("""
            SELECT *
            FROM mission_options
            WHERE question_id = ?
            ORDER BY id
        """, (question["id"],)).fetchall()

        questions_with_options.append({
            "question": question,
            "options": options
        })

    connection.close()

    return render_template(
        "mission.html",
        mission=mission_data,
        questions=questions_with_options
    )

@app.route(
    "/mission/<int:mission_id>/submit",
    methods=["POST"]
)
def submit_mission(mission_id):

    option_id = request.form.get("option_id")

    if not option_id:
        return "No option selected", 400

    connection = get_connection()

    # =========================
    # GET MISSION
    # =========================

    mission_data = connection.execute("""
        SELECT *
        FROM missions
        WHERE id = ?
    """, (mission_id,)).fetchone()

    if mission_data is None:
        connection.close()
        return "Mission not found", 404

    # =========================
    # GET SELECTED OPTION
    # =========================

    selected_option = connection.execute("""
        SELECT
            mission_options.*,
            mission_questions.mission_id
        FROM mission_options
        JOIN mission_questions
            ON mission_options.question_id = mission_questions.id
        WHERE mission_options.id = ?
        AND mission_questions.mission_id = ?
    """, (
        option_id,
        mission_id
    )).fetchone()

    if selected_option is None:
        connection.close()
        return "Invalid option", 400

    # =========================
    # GET USER
    # =========================

    user = get_or_create_demo_user(connection)
    user_id = user["id"]

    # =========================
    # CHECK ANSWER
    # =========================

    if selected_option["is_correct"] == 1:
        score = 100
        result = "correct"
    else:
        score = 0
        result = "wrong"

    # =========================
    # CHECK PREVIOUS COMPLETION
    # =========================

    previous_completion = connection.execute("""
        SELECT id
        FROM mission_attempts
        WHERE user_id = ?
        AND mission_id = ?
        AND completed = 1
        AND score = 100
        LIMIT 1
    """, (
        user_id,
        mission_id
    )).fetchone()

    # =========================
    # SAVE ATTEMPT
    # =========================

    connection.execute("""
        INSERT INTO mission_attempts
        (
            user_id,
            mission_id,
            score,
            completed
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        mission_id,
        score,
        1
    ))

    # =========================
    # AWARD XP
    # =========================

    if result == "correct" and previous_completion is None:

        connection.execute("""
            UPDATE users
            SET xp = xp + ?
            WHERE id = ?
        """, (
            mission_data["xp_reward"],
            user_id
        ))

    # =========================
    # UPDATE LEVEL
    # =========================

    update_user_level(
        connection,
        user_id
    )

    # =========================
    # UPDATE SECURITY SCORE
    # =========================

    update_security_score(
        connection,
        user_id
    )

    # =========================
    # CHECK ACHIEVEMENTS
    # =========================

    check_and_award_achievements(
        connection,
        user_id
    )

    # Achievement XP can change the level
    # so calculate the level again.

    update_user_level(
        connection,
        user_id
    )

    connection.commit()
    connection.close()

    return redirect(
        url_for(
            "mission_result",
            mission_id=mission_id,
            result=result
        )
    )

@app.route(
    "/mission/<int:mission_id>/result"
)
def mission_result(mission_id):
    result = request.args.get("result")

    connection = get_connection()

    mission_data = connection.execute("""
        SELECT *
        FROM missions
        WHERE id = ?
    """, (mission_id,)).fetchone()

    user = get_or_create_demo_user(connection)

    connection.close()

    if mission_data is None:
        return "Mission not found", 404

    return render_template(
        "mission_result.html",
        mission=mission_data,
        user=user,
        result=result
    )

@app.route("/dashboard")
def dashboard():
    connection = get_connection()

    user = get_or_create_demo_user(connection)
    user_id = user["id"]

    # =========================
    # AI RISK PREDICTION
    # =========================

    
    risk_prediction = predict_security_risk(
        connection,
        user_id
    )

    # =========================
    # MISSION ANALYTICS
    # =========================

    completed_missions = connection.execute("""
        SELECT COUNT(DISTINCT mission_id)
        FROM mission_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchone()[0]

    total_missions = connection.execute("""
        SELECT COUNT(*)
        FROM missions
    """).fetchone()[0]

        # =========================
    # MISSION + SIMULATION ANALYTICS
    # =========================

    practical_scores = []

    normal_missions = connection.execute("""
        SELECT score
        FROM mission_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    practical_scores.extend(
        attempt["score"]
        for attempt in normal_missions
    )


    phishing_attempts = connection.execute("""
        SELECT score
        FROM phishing_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    practical_scores.extend(
        attempt["score"]
        for attempt in phishing_attempts
    )


    malware_attempts = connection.execute("""
        SELECT score
        FROM malware_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    practical_scores.extend(
        attempt["score"]
        for attempt in malware_attempts
    )

    # =========================
    # SOCIAL ENGINEERING / OTP SCORES
    # =========================

    social_engineering_attempts = connection.execute("""
        SELECT score
        FROM social_engineering_attempts
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchall()

    practical_scores.extend(
        attempt["score"]
        for attempt in social_engineering_attempts
    )

    if practical_scores:
        mission_accuracy = round(
            sum(practical_scores) / len(practical_scores)
        )
    else:
        mission_accuracy = 0

    # =========================
    # QUIZ ANALYTICS
    # =========================

    quiz_stats = connection.execute("""
        SELECT
            COUNT(*) AS total_quizzes,
            SUM(score) AS correct_answers,
            SUM(total_questions) AS total_questions,
            AVG(percentage) AS average_percentage
        FROM quiz_attempts
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    quiz_accuracy = round(
        quiz_stats["average_percentage"] or 0
    )

    total_quizzes = quiz_stats["total_quizzes"] or 0
    correct_answers = quiz_stats["correct_answers"] or 0
    total_questions = quiz_stats["total_questions"] or 0

    incorrect_answers = max(
        total_questions - correct_answers,
        0
    )

    # =========================
    # LEARNING PROGRESS
    # =========================

    learning_progress = connection.execute("""
        SELECT *
        FROM user_progress
        WHERE user_id = ?
        ORDER BY category
    """, (user_id,)).fetchall()

    completed_categories = connection.execute("""
        SELECT COUNT(*)
        FROM user_progress
        WHERE user_id = ?
        AND completed = 1
    """, (user_id,)).fetchone()[0]

    total_categories = connection.execute("""
        SELECT COUNT(DISTINCT category)
        FROM quiz_questions
    """).fetchone()[0]

    learning_percentage = 0

    if total_categories > 0:
        learning_percentage = round(
            (completed_categories / total_categories) * 100
        )

    # =========================
    # CATEGORY PERFORMANCE
    # =========================

    category_performance = connection.execute("""
        SELECT
            category,
            score,
            completed
        FROM user_progress
        WHERE user_id = ?
        ORDER BY score DESC
    """, (user_id,)).fetchall()

    # =========================
    # ACHIEVEMENTS
    # =========================

    achievements = connection.execute("""
        SELECT achievements.*
        FROM achievements
        JOIN user_achievements
        ON achievements.id = user_achievements.achievement_id
        WHERE user_achievements.user_id = ?
        ORDER BY achievements.id
    """, (user_id,)).fetchall()

    # =========================
    # ANALYTICS SUMMARY
    # =========================

    analytics = {
        "mission_accuracy": mission_accuracy,
        "quiz_accuracy": quiz_accuracy,
        "total_quizzes": total_quizzes,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "completed_categories": completed_categories,
        "total_categories": total_categories,
        "learning_percentage": learning_percentage
    }

    connection.close()


    return render_template(
        "dashboard.html",
        user=user,
        completed_missions=completed_missions,
        total_missions=total_missions,
        achievements=achievements,
        learning_progress=learning_progress,
        category_performance=category_performance,
        analytics=analytics,
        risk_prediction=risk_prediction
    )

@app.route("/learn")
def learn():
    return render_template("learn.html")


# =========================
# PHISHING SIMULATION
# =========================

@app.route("/simulation/phishing")
def phishing_simulation():

    connection = get_connection()

    simulation = connection.execute("""
        SELECT *
        FROM phishing_simulations
        WHERE title = ?
    """, (
        "Suspicious Email Investigation",
    )).fetchone()

    if simulation is None:
        connection.close()
        return "Phishing simulation not found", 404

    clues = connection.execute("""
        SELECT *
        FROM phishing_clues
        WHERE simulation_id = ?
        ORDER BY id
    """, (
        simulation["id"],
    )).fetchall()

    connection.close()

    return render_template(
        "phishing_simulation.html",
        simulation=simulation,
        clues=clues
    )

@app.route(
    "/simulation/phishing/submit",
    methods=["POST"]
)
def submit_phishing_simulation():

    connection = get_connection()

    simulation = connection.execute("""
        SELECT *
        FROM phishing_simulations
        WHERE id = ?
    """, (
        request.form.get("simulation_id"),
    )).fetchone()

    if simulation is None:
        connection.close()
        return "Simulation not found", 404

    clues = connection.execute("""
        SELECT *
        FROM phishing_clues
        WHERE simulation_id = ?
        ORDER BY id
    """, (
        simulation["id"],
    )).fetchall()

    user = get_or_create_demo_user(connection)
    user_id = user["id"]

    correct_answers = 0
    results = []

    for clue in clues:

        selected_answer = request.form.get(
            f"clue_{clue['id']}"
        )

        is_correct = (
            selected_answer == clue["correct_answer"]
        )

        if is_correct:
            correct_answers += 1

        results.append({
            "clue": clue,
            "selected_answer": selected_answer,
            "is_correct": is_correct
        })

    total_clues = len(clues)

    score = 0

    if total_clues > 0:
        score = round(
            (correct_answers / total_clues) * 100
        )

    previous_completion = connection.execute("""
        SELECT id
        FROM phishing_attempts
        WHERE user_id = ?
        AND simulation_id = ?
        AND completed = 1
        AND score = 100
        LIMIT 1
    """, (
        user_id,
        simulation["id"]
    )).fetchone()

    xp_awarded = 0

    if previous_completion is None:

        xp_awarded = round(
            simulation["xp_reward"] * score / 100
        )

        if xp_awarded > 0:

            connection.execute("""
                UPDATE users
                SET xp = xp + ?
                WHERE id = ?
            """, (
                xp_awarded,
                user_id
            ))

    connection.execute("""
        INSERT INTO phishing_attempts
        (
            user_id,
            simulation_id,
            score,
            completed,
            xp_awarded
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        simulation["id"],
        score,
        1,
        xp_awarded
    ))
    update_user_level(
        connection,
        user_id
    )

    update_security_score(
        connection,
        user_id
    )

    connection.commit()
    user = connection.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (
        user_id,
    )).fetchone()

    connection.close()

    return render_template(
        "phishing_result.html",
        simulation=simulation,
        results=results,
        score=score,
        correct_answers=correct_answers,
        total_clues=total_clues,
        xp_awarded=xp_awarded,
        user=user
    )

@app.route("/simulation/malware")
def malware_simulation():
    connection = get_connection()

    simulation = connection.execute("""
        SELECT *
        FROM malware_simulations
        WHERE title = ?
    """, ("Suspicious Download Investigation",)).fetchone()

    if simulation is None:
        connection.close()
        return "Malware simulation not found", 404

    clues = connection.execute("""
        SELECT *
        FROM malware_clues
        WHERE simulation_id = ?
        ORDER BY id
    """, (simulation["id"],)).fetchall()

    connection.close()

    return render_template(
        "malware_simulation.html",
        simulation=simulation,
        clues=clues
    )

@app.route(
    "/simulation/malware/submit",
    methods=["POST"]
)
def submit_malware_simulation():

    connection = get_connection()

    simulation = connection.execute("""
        SELECT *
        FROM malware_simulations
        WHERE id = ?
    """, (
        request.form.get("simulation_id"),
    )).fetchone()

    if simulation is None:
        connection.close()
        return "Simulation not found", 404

    clues = connection.execute("""
        SELECT *
        FROM malware_clues
        WHERE simulation_id = ?
        ORDER BY id
    """, (
        simulation["id"],
    )).fetchall()

    user = get_or_create_demo_user(connection)
    user_id = user["id"]

    correct_answers = 0
    results = []

    for clue in clues:

        selected_answer = request.form.get(
            f"clue_{clue['id']}"
        )

        is_correct = (
            selected_answer == clue["correct_answer"]
        )

        if is_correct:
            correct_answers += 1

        results.append({
            "clue": clue,
            "selected_answer": selected_answer,
            "is_correct": is_correct
        })

    total_clues = len(clues)

    score = 0

    if total_clues > 0:
        score = round(
            (correct_answers / total_clues) * 100
        )

    previous_completion = connection.execute("""
        SELECT id
        FROM malware_attempts
        WHERE user_id = ?
        AND simulation_id = ?
        AND completed = 1
        AND score = 100
        LIMIT 1
    """, (
        user_id,
        simulation["id"]
    )).fetchone()

    xp_awarded = 0

    if previous_completion is None:

        xp_awarded = round(
            simulation["xp_reward"] * score / 100
        )

        if xp_awarded > 0:
            connection.execute("""
                UPDATE users
                SET xp = xp + ?
                WHERE id = ?
            """, (
                xp_awarded,
                user_id
            ))

    connection.execute("""
        INSERT INTO malware_attempts
        (
            user_id,
            simulation_id,
            score,
            completed,
            xp_awarded
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        simulation["id"],
        score,
        1,
        xp_awarded
    ))

    update_user_level(
        connection,
        user_id
    )

    update_security_score(
        connection,
        user_id
    )

    connection.commit()
    user = connection.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (
        user_id,
    )).fetchone()

    connection.close()

    return render_template(
        "malware_result.html",
        simulation=simulation,
        results=results,
        score=score,
        correct_answers=correct_answers,
        total_clues=total_clues,
        xp_awarded=xp_awarded,
        user=user
    )

@app.route("/simulation/social")
def social_engineering_simulation():

    connection = get_connection()

    simulation = connection.execute("""
        SELECT *
        FROM social_engineering_simulations
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if simulation is None:
        connection.close()
        return "Social Engineering simulation not found", 404

    questions = connection.execute("""
        SELECT *
        FROM social_engineering_questions
        WHERE simulation_id = ?
        ORDER BY id
    """, (
        simulation["id"],
    )).fetchall()

    connection.close()

    return render_template(
        "social_engineering_simulation.html",
        simulation=simulation,
        questions=questions
    )


@app.route(
    "/simulation/social/submit",
    methods=["POST"]
)
def submit_social_engineering_simulation():

    connection = get_connection()

    simulation = connection.execute("""
        SELECT *
        FROM social_engineering_simulations
        WHERE id = ?
    """, (
        request.form.get("simulation_id"),
    )).fetchone()

    if simulation is None:
        connection.close()
        return "Simulation not found", 404

    questions = connection.execute("""
        SELECT *
        FROM social_engineering_questions
        WHERE simulation_id = ?
        ORDER BY id
    """, (
        simulation["id"],
    )).fetchall()

    user = get_or_create_demo_user(connection)
    user_id = user["id"]

    correct_answers = 0
    results = []

    for question in questions:

        selected_answer = request.form.get(
            f"question_{question['id']}"
        )

        is_correct = (
            selected_answer == question["correct_answer"]
        )

        if is_correct:
            correct_answers += 1

        results.append({
            "question": question,
            "selected_answer": selected_answer,
            "is_correct": is_correct
        })

    total_questions = len(questions)

    score = 0

    if total_questions > 0:
        score = round(
            (correct_answers / total_questions) * 100
        )

    previous_completion = connection.execute("""
        SELECT id
        FROM social_engineering_attempts
        WHERE user_id = ?
        AND simulation_id = ?
        AND completed = 1
        AND score = 100
        LIMIT 1
    """, (
        user_id,
        simulation["id"]
    )).fetchone()

    xp_awarded = 0

    if previous_completion is None:

        xp_awarded = round(
            simulation["xp_reward"] * score / 100
        )

        if xp_awarded > 0:
            connection.execute("""
                UPDATE users
                SET xp = xp + ?
                WHERE id = ?
            """, (
                xp_awarded,
                user_id
            ))

    connection.execute("""
        INSERT INTO social_engineering_attempts
        (
            user_id,
            simulation_id,
            score,
            completed,
            xp_awarded
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        simulation["id"],
        score,
        1,
        xp_awarded
    ))

    update_user_level(
        connection,
        user_id
    )

    update_security_score(
        connection,
        user_id
    )

    connection.commit()

    user = connection.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (
        user_id,
    )).fetchone()

    connection.close()

    return render_template(
        "social_engineering_result.html",
        simulation=simulation,
        results=results,
        score=score,
        correct_answers=correct_answers,
        total_questions=total_questions,
        xp_awarded=xp_awarded,
        user=user
    )


@app.route("/learn/fundamentals")
def fundamentals():
    return render_template("fundamentals.html")


@app.route("/learn/<category>/quiz", methods=["GET", "POST"])
def category_quiz(category):

    category_map = {
    "fundamentals": "Cybersecurity Fundamentals",
    "phishing": "Phishing Awareness",
    "password": "Password Security",
    "malware": "Malware Awareness",
    "social": "Social Engineering",
    "network": "Network Security",
    "web": "Web Security",
    "encryption": "Encryption & Hashing",
    "otp": "OTP & Account Scams"
}

    quiz_category = category_map.get(category)

    if quiz_category is None:
        return "Quiz category not found", 404

    connection = get_connection()

    questions = connection.execute("""
        SELECT *
        FROM quiz_questions
        WHERE category = ?
        ORDER BY id
    """, (quiz_category,)).fetchall()

    if request.method == "POST":

        score = 0
        total_questions = len(questions)
        answer_records = []

        for question in questions:

            selected_option = request.form.get(
                f"question_{question['id']}"
            )

            is_correct = (
                selected_option == question["correct_option"]
            )

            if is_correct:
                score += 1

            answer_records.append({
                "question_id": question["id"],
                "selected_option": selected_option,
                "is_correct": is_correct
            })

        percentage = 0

        if total_questions > 0:
            percentage = round(
                (score / total_questions) * 100,
                2
            )

        user = connection.execute("""
            SELECT id
            FROM users
            WHERE username = ?
        """, ("DemoUser",)).fetchone()

        if user is None:

            connection.execute("""
                INSERT INTO users (
                    username,
                    xp,
                    level,
                    security_score
                )
                VALUES (?, ?, ?, ?)
            """, ("DemoUser", 0, 1, 0))

            connection.commit()

            user = connection.execute("""
                SELECT id
                FROM users
                WHERE username = ?
            """, ("DemoUser",)).fetchone()

        user_id = user["id"]

        cursor = connection.execute("""
            INSERT INTO quiz_attempts (
                user_id,
                category,
                score,
                total_questions,
                percentage
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            quiz_category,
            score,
            total_questions,
            percentage
        ))

        attempt_id = cursor.lastrowid

        for answer in answer_records:

            connection.execute("""
                INSERT INTO quiz_answers (
                    attempt_id,
                    question_id,
                    selected_option,
                    is_correct
                )
                VALUES (?, ?, ?, ?)
            """, (
                attempt_id,
                answer["question_id"],
                answer["selected_option"],
                answer["is_correct"]
            ))

        connection.execute("""
            INSERT INTO user_progress (
                user_id,
                category,
                completed,
                score
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, category)
            DO UPDATE SET
                completed = excluded.completed,
                score = excluded.score
        """, (
            user_id,
            quiz_category,
            1,
            percentage
        ))

        connection.commit()
        connection.close()

        return render_template(
            "fundamentals_quiz.html",
            questions=questions,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            submitted=True,
            quiz_category=quiz_category,
            category=category
        )

    connection.close()

    return render_template(
        "fundamentals_quiz.html",
        questions=questions,
        submitted=False,
        quiz_category=quiz_category,
        category=category
    )


if __name__ == "__main__":
    app.run()