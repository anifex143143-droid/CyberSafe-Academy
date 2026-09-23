print("================================")
print("     CYBERSAFE ACADEMY")
print("================================")
print("Cybersecurity Learning Platform")
print()

print("1. Learn Cybersecurity")
print("2. Security Awareness")
print("3. Security Quiz")
print("4. Exit")

choice = input("\nEnter your choice: ")

if choice == "1":
    print("\n===== CYBERSECURITY BASICS =====")
    print("1. What is Cybersecurity?")
    print("2. Common Cyber Threats")
    print("3. Password Security")
    print("4. Back")

    lesson = input("\nChoose a lesson: ")

    if lesson == "1":
        print("\n--- What is Cybersecurity? ---")
        print("Cybersecurity protects computers, networks,")
        print("applications and data from unauthorized access.")

    elif lesson == "2":
        print("\n--- Common Cyber Threats ---")
        print("Phishing")
        print("Malware")
        print("Ransomware")
        print("Social Engineering")

    elif lesson == "3":
        print("\n--- Password Security ---")
        print("Use long, unique passwords.")
        print("Avoid using the same password everywhere.")
        print("Use multi-factor authentication when available.")

    elif lesson == "4":
        print("\nReturning to main menu...")

    else:
        print("\nInvalid lesson choice.")

elif choice == "2":
    print("\n===== SECURITY AWARENESS =====")
    print("Security awareness lessons coming next.")

elif choice == "3":
    print("\n===== SECURITY QUIZ =====")

    score = 0

    print("\nQ1. What is phishing?")
    print("1. A type of computer hardware")
    print("2. A fake message designed to trick someone")
    print("3. A programming language")
    print("4. A backup system")

    answer = input("Your answer: ")

    if answer == "2":
        print("Correct! ✅")
        score += 1
    else:
        print("Wrong ❌")

    print("\nQ2. Which is safer?")
    print("1. Using the same password everywhere")
    print("2. Sharing your password with friends")
    print("3. Using long, unique passwords")
    print("4. Writing your password publicly")

    answer = input("Your answer: ")

    if answer == "3":
        print("Correct! ✅")
        score += 1
    else:
        print("Wrong ❌")

    print("\n===== RESULT =====")
    print("Your score:", score, "/ 2")

elif choice == "4":
    print("\nExiting CyberSafe Academy...")

else:
    print("\nInvalid choice.")