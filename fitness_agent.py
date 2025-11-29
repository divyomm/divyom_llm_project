import random
import datetime

def get_user_input():
    print("--- WELCOME TO YOUR ADVANCED FITNESS AGENT ---")
    print("I will design a unique workout for you based on your needs.\n")
    
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

def select_exercise(options):
    """Helper function to pick a random exercise from a list"""
    return random.choice(options)

def generate_workout(goal, equip, level):
    workout_plan = []
    
    # Get current date for the file header
    date_today = datetime.datetime.now().strftime("%Y-%m-%d")
    workout_plan.append(f"=== CUSTOM WORKOUT PLAN ({date_today}) ===")
    
    # WARMUP
    workout_plan.append("\n=== WARMUP (5-10 mins) ===")
    warmups = ["Jumping Jacks", "High Knees", "Light Jog", "Skipping Rope"]
    workout_plan.append(f"- 3 mins of {select_exercise(warmups)}")
    workout_plan.append("- Arm circles, leg swings, torso twists")
    
    # MAIN WORKOUT LOGIC
    workout_plan.append("\n=== MAIN WORKOUT ===")
    
    # --- BODYWEIGHT LOGIC ---
    if equip == 'a':
        if goal == 'a': # Strength
            push_variation = select_exercise(["Standard Pushups", "Diamond Pushups", "Wide Pushups"])
            leg_variation = select_exercise(["Squats", "Lunges", "Step-ups"])
            workout_plan.append(f"- {push_variation}: 5 sets of 5 reps (Explosive)")
            workout_plan.append(f"- {leg_variation}: 5 sets of 5 reps (Slow tempo)")
            workout_plan.append("- Plank: 3 sets of 45 seconds")
            
        elif goal == 'b': # Endurance
            cardio_move = select_exercise(["Burpees", "Mountain Climbers", "Jump Squats"])
            workout_plan.append(f"- {cardio_move}: 3 sets of 20 reps")
            workout_plan.append("- High Knees: 3 sets of 1 min")
            workout_plan.append("- Bicycle Crunches: 3 sets of 30 reps")
            
        else: # Hypertrophy
            workout_plan.append("- Pushups: 3 sets to failure")
            workout_plan.append("- Glute Bridges: 3 sets of 15 reps")
            workout_plan.append("- Dips (using chair): 3 sets of 12 reps")

    # --- DUMBBELL LOGIC ---
    elif equip == 'b':
        if goal == 'a': # Strength
            press = select_exercise(["DB Chest Press", "DB Shoulder Press"])
            workout_plan.append(f"- {press}: 5 sets of 5 reps (Heavy weight)")
            workout_plan.append("- Goblet Squats: 5 sets of 5 reps")
            
        else: # General/Hypertrophy
            row_type = select_exercise(["One-arm Row", "Bent-over Row"])
            workout_plan.append(f"- {row_type}: 3 sets of 10-12 reps")
            workout_plan.append("- DB Lunges: 3 sets of 12 reps per leg")
            workout_plan.append("- Bicep Curls: 3 sets of 12 reps")

    # --- GYM LOGIC ---
    elif equip == 'c':
         compound_lift = select_exercise(["Barbell Squat", "Deadlift"])
         workout_plan.append(f"- {compound_lift}: 3 sets of 5 reps (Heavy)")
         workout_plan.append("- Bench Press: 3 sets of 8 reps")
         workout_plan.append("- Lat Pulldowns: 3 sets of 10 reps")
         
    # COOL DOWN
    workout_plan.append("\n=== COOLDOWN ===")
    workout_plan.append("- 5 mins static stretching (hamstrings, chest, back)")
    
    return workout_plan

def save_to_file(plan):
    filename = "my_workout_plan.txt"
    with open(filename, "w") as f:
        for line in plan:
            f.write(line + "\n")
    print(f"\n[SUCCESS] Your workout has been saved to '{filename}'")

def main():
    # 1. Get inputs
    g, e, l = get_user_input()
    
    # 2. Process logic
    plan = generate_workout(g, e, l)
    
    # 3. Output result to screen
    print("\n" + "*"*30)
    for line in plan:
        print(line)
    print("*"*30)
    
    # 4. Save to file (The "Pro" Feature)
    save_to_file(plan)

if __name__ == "__main__":
    main()