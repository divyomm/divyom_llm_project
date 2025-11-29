import random

def get_user_input():
    print("--- WELCOME TO YOUR PERSONAL FITNESS AGENT ---")
    print("I will design a workout for you based on your needs.\n")
    
    # Question 1: Goal
    print("1. What is your primary goal?")
    print("   (a) Strength")
    print("   (b) Endurance")
    print("   (c) Muscle Growth (Hypertrophy)")
    goal = input("   Enter a, b, or c: ").strip().lower()
    
    # Question 2: Equipment
    print("\n2. What equipment do you have?")
    print("   (a) None (Bodyweight)")
    print("   (b) Dumbbells")
    print("   (c) Full Gym")
    equip = input("   Enter a, b, or c: ").strip().lower()
    
    # Question 3: Experience
    print("\n3. Experience Level?")
    print("   (a) Beginner")
    print("   (b) Intermediate")
    level = input("   Enter a, b, or c: ").strip().lower()
    
    return goal, equip, level

def generate_workout(goal, equip, level):
    workout_plan = []
    
    # WARMUP (Always the same)
    workout_plan.append("\n=== WARMUP (5-10 mins) ===")
    workout_plan.append("- 3 mins jumping jacks or light jog")
    workout_plan.append("- Arm circles, leg swings")
    
    # MAIN WORKOUT LOGIC
    workout_plan.append("\n=== MAIN WORKOUT ===")
    
    # Logic for Bodyweight (Option a)
    if equip == 'a':
        if goal == 'a': # Strength
            workout_plan.append("- Pushups: 5 sets of 5 reps (explosive)")
            workout_plan.append("- Squats: 5 sets of 5 reps (slow tempo)")
        elif goal == 'b': # Endurance
            workout_plan.append("- Burpees: 3 sets of 20 reps")
            workout_plan.append("- Mountain Climbers: 3 sets of 1 min")
        else: # Muscle Growth
            workout_plan.append("- Pushups: 3 sets to failure")
            workout_plan.append("- Lunges: 3 sets of 15 per leg")
            
    # Logic for Dumbbells (Option b)
    elif equip == 'b':
        if goal == 'a': # Strength
            workout_plan.append("- DB Chest Press: 5 sets of 5 reps (Heavy)")
            workout_plan.append("- Goblet Squats: 5 sets of 5 reps (Heavy)")
        else: # General/Hypertrophy
            workout_plan.append("- DB Shoulder Press: 3 sets of 10-12 reps")
            workout_plan.append("- DB Rows: 3 sets of 10-12 reps")
            workout_plan.append("- DB Lunges: 3 sets of 12 reps")

    # Logic for Gym (Option c)
    elif equip == 'c':
         workout_plan.append("- Barbell Squat: 3 sets of 8 reps")
         workout_plan.append("- Bench Press: 3 sets of 8 reps")
         workout_plan.append("- Deadlift: 3 sets of 5 reps")
         
    # COOL DOWN
    workout_plan.append("\n=== COOLDOWN ===")
    workout_plan.append("- 5 mins static stretching (hamstrings, chest, back)")
    
    return workout_plan

def main():
    # 1. Get inputs
    g, e, l = get_user_input()
    
    # 2. Process logic
    plan = generate_workout(g, e, l)
    
    # 3. Output result
    print("\n" + "*"*30)
    print("HERE IS YOUR CUSTOM PLAN:")
    for line in plan:
        print(line)
    print("*"*30)

if __name__ == "__main__":
    main()