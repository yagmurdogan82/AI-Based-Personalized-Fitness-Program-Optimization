import random
import copy

# --- 1. DATA STRUCTURES & CONSTANTS ---

# Exercise Database (Name, Type, Intensity 1-10, Estimated Time mins)
EXERCISE_DB = [
    {"name": "Squat", "type": "strength", "intensity": 8, "time": 10},
    {"name": "Deadlift", "type": "strength", "intensity": 9, "time": 15},
    {"name": "Bench Press", "type": "strength", "intensity": 8, "time": 12},
    {"name": "Push Up", "type": "strength", "intensity": 6, "time": 5},
    {"name": "Pull Up", "type": "strength", "intensity": 8, "time": 5},
    {"name": "Dumbbell Row", "type": "strength", "intensity": 7, "time": 10},
    {"name": "Plank", "type": "core", "intensity": 5, "time": 3},
    {"name": "HIIT Cardio", "type": "cardio", "intensity": 9, "time": 20},
    {"name": "Jogging", "type": "cardio", "intensity": 6, "time": 30},
    {"name": "Yoga Stretch", "type": "flexibility", "intensity": 3, "time": 15},
]

# User Class
class User:
    def __init__(self, name, age, gender, weight, height, goal, weekly_days):
        self.name = name
        self.age = age
        self.gender = gender  # 'male' or 'female'
        self.weight = weight  # kg
        self.height = height  # cm
        self.goal = goal      # 'cut', 'bulk', 'maintain'
        self.weekly_days = weekly_days

# --- 2. NUTRITION OPTIMIZATION (DETERMINISTIC) ---

def calculate_nutrition(user):
    # Mifflin St Jeor Equation for Basal Metabolic Rate (BMR)
    if user.gender == 'male':
        bmr = (10 * user.weight) + (6.25 * user.height) - (5 * user.age) + 5
    else:
        bmr = (10 * user.weight) + (6.25 * user.height) - (5 * user.age) - 161

    # Activity Multiplier (Assuming Moderate Activity for calculation)
    tdee = bmr * 1.55 

    # Adjust calories based on goal
    if user.goal == 'cut':
        target_calories = tdee - 500
        macros = {'protein': 0.40, 'fat': 0.30, 'carb': 0.30} # High protein for cutting
    elif user.goal == 'bulk':
        target_calories = tdee + 500
        macros = {'protein': 0.30, 'fat': 0.20, 'carb': 0.50} # High carb for bulking
    else:
        target_calories = tdee
        macros = {'protein': 0.30, 'fat': 0.30, 'carb': 0.40}

    return {
        "calories": int(target_calories),
        "protein_g": int((target_calories * macros['protein']) / 4),
        "carb_g": int((target_calories * macros['carb']) / 4),
        "fat_g": int((target_calories * macros['fat']) / 9)
    }

# --- 3. GENETIC ALGORITHM (WORKOUT OPTIMIZATION) ---

class WorkoutPlan:
    def __init__(self, days):
        # Genome: Random list of exercises for each day
        self.schedule = []
        for _ in range(days):
            # Randomly select 3 to 6 exercises per day
            daily_workout = random.sample(EXERCISE_DB, k=random.randint(3, 6))
            self.schedule.append(daily_workout)
        self.fitness_score = 0

def fitness_function(plan, user):
    """
    Evaluates how 'fit' (suitable) the plan is for the user.
    Higher score = Better plan.
    """
    score = 100
    
    # Criterion 1: Time Management (Ideal workout: 30-90 mins)
    total_weekly_time = 0
    for day in plan.schedule:
        daily_time = sum(ex['time'] for ex in day)
        total_weekly_time += daily_time
        # Penalty if too short (<30 min) or too long (>90 min)
        if daily_time < 30 or daily_time > 90:
            score -= 10
    
    # Criterion 2: Goal Alignment (Intensity & Type)
    avg_intensity = 0
    total_exercises = 0
    cardio_count = 0
    strength_count = 0
    
    for day in plan.schedule:
        for ex in day:
            avg_intensity += ex['intensity']
            total_exercises += 1
            if ex['type'] == 'cardio': cardio_count += 1
            if ex['type'] == 'strength': strength_count += 1
            
    if total_exercises > 0:
        avg_intensity /= total_exercises

    # Adjust score based on specific user goals
    if user.goal == 'bulk':
        if avg_intensity < 7: score -= 20 # Needs high intensity
        if cardio_count > strength_count: score -= 30 # Too much cardio hurts bulking
    elif user.goal == 'cut':
        if cardio_count < 2: score -= 20 # Needs cardio for fat loss
        
    plan.fitness_score = score
    return score

def mutate(plan):
    """Introduces random changes to the plan (Mutation)"""
    day_idx = random.randint(0, len(plan.schedule) - 1)
    
    # Type 1: Swap an exercise
    if random.random() < 0.5:
        ex_idx = random.randint(0, len(plan.schedule[day_idx]) - 1)
        plan.schedule[day_idx][ex_idx] = random.choice(EXERCISE_DB)
    # Type 2: Shuffle the order of exercises
    else:
        random.shuffle(plan.schedule[day_idx])

def crossover(parent1, parent2):
    """Creates a new plan by combining two parents"""
    # Single Point Crossover
    child = WorkoutPlan(len(parent1.schedule))
    mid_point = len(parent1.schedule) // 2
    child.schedule = parent1.schedule[:mid_point] + parent2.schedule[mid_point:]
    return child

def run_genetic_algorithm(user):
    POPULATION_SIZE = 20
    GENERATIONS = 50
    
    # 1. Initialize Population
    population = [WorkoutPlan(user.weekly_days) for _ in range(POPULATION_SIZE)]
    
    for generation in range(GENERATIONS):
        # 2. Evaluate Fitness
        for plan in population:
            fitness_function(plan, user)
            
        # Sort by fitness (Best plans first)
        population.sort(key=lambda x: x.fitness_score, reverse=True)
        
        # Selection: Keep top 50%
        survivors = population[:POPULATION_SIZE//2]
        
        next_generation = survivors[:]
        
        # 3. Create Next Generation (Crossover & Mutation)
        while len(next_generation) < POPULATION_SIZE:
            p1 = random.choice(survivors)
            p2 = random.choice(survivors)
            child = crossover(p1, p2)
            
            # 20% Mutation chance
            if random.random() < 0.2:
                mutate(child)
                
            next_generation.append(child)
            
        population = next_generation

    # Return the best solution found
    best_plan = population[0]
    fitness_function(best_plan, user) # Final score update
    return best_plan

# --- 4. MAIN PROGRAM (USER INPUT MODE) ---

def get_user_input():
    print("\n--- ENTER USER DETAILS ---")
    name = input("Enter Name: ")
    
    while True:
        try:
            age = int(input("Enter Age: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number for Age.")

    gender = input("Enter Gender (male/female): ").lower().strip()
    while gender not in ['male', 'female']:
        print("Please enter 'male' or 'female'.")
        gender = input("Enter Gender (male/female): ").lower().strip()

    while True:
        try:
            weight = float(input("Enter Weight (kg): "))
            break
        except ValueError:
            print("Invalid input. Please enter a number for Weight.")

    while True:
        try:
            height = float(input("Enter Height (cm): "))
            break
        except ValueError:
            print("Invalid input. Please enter a number for Height.")

    goal = input("Enter Goal (cut/bulk/maintain): ").lower().strip()
    while goal not in ['cut', 'bulk', 'maintain']:
        print("Please enter 'cut', 'bulk', or 'maintain'.")
        goal = input("Enter Goal (cut/bulk/maintain): ").lower().strip()

    while True:
        try:
            days = int(input("Enter Workout Days per Week (1-7): "))
            if 1 <= days <= 7:
                break
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    return User(name, age, gender, weight, height, goal, days)

def main():
    print("AI-BASED FITNESS OPTIMIZATION SYSTEM STARTING...\n")
    print("-" * 60)

    # Get data manually from terminal
    user = get_user_input()

    print("-" * 60)
    print(f"PROCESSING PROFILE: {user.name} | GOAL: {user.goal.upper()}")
    
    # 1. Calculate Nutrition
    nutrition = calculate_nutrition(user)
    print(f" > Nutrition Target: {nutrition['calories']} kcal")
    print(f" > Macros: Protein: {nutrition['protein_g']}g | Carb: {nutrition['carb_g']}g | Fat: {nutrition['fat_g']}g")
    
    # 2. Optimize Workout (Running Genetic Algorithm)
    print(" > Optimizing Workout Program (Genetic Algorithm Running)...")
    best_workout = run_genetic_algorithm(user)
    
    print(f" > Program Fitness Score: {best_workout.fitness_score}/100")
    print(" > Weekly Plan:")
    
    for i, day in enumerate(best_workout.schedule):
        daily_exercises = [ex['name'] for ex in day]
        print(f"   Day {i+1}: {', '.join(daily_exercises)}")
        
    print("-" * 60)
    print("Optimization Completed Successfully.")

if __name__ == "__main__":
    main()