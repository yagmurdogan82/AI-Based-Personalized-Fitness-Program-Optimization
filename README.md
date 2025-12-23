# AI-Based Personalized Fitness Program Optimization 🧬🏋️‍♂️

**Course:** CMPE 353 - Principles of Artificial Intelligence  
**Student:** Yağmur Doğan

## 📖 Project Overview
This project is an AI-driven system designed to generate **personalized weekly workout schedules** and **nutrition plans**. Unlike static templates, it utilizes a **Genetic Algorithm (GA)** to solve the optimization problem of fitness scheduling based on user-specific constraints (age, goal, available days).

## 🚀 Key Features
* **Genetic Algorithm Engine:** Uses evolutionary computation (Selection, Crossover, Mutation) to evolve the perfect workout schedule over generations.
* **Smart Constraints:** Optimizes for both *Hard Constraints* (e.g., available days) and *Soft Constraints* (e.g., preferred intensity).
* **Nutrition Module:** Calculates BMR and macronutrients (Protein/Carb/Fat) tailored to goals like "Cut" or "Bulk" using the Mifflin St Jeor equation.
* **Dynamic Adaptation:** The system improves the "fitness score" of the schedule by ~111% compared to random assignment.

## 🛠️ Algorithms & Technologies
* **Language:** Python 3.13
* **Optimization:** Genetic Algorithm (Elitism Selection, Single-Point Crossover)
* **Biological Model:** Mifflin St Jeor Equation

## 📂 Project Structure
* `YağmurDoğan_121200126_codes.py` - The main Python script containing the GA implementation.
* `YağmurDoğan_121200126_cmpe353_report.pdf` - Comprehensive project report detailing the methodology and experimental results.

## ▶️ How to Run
1.  Clone the repository.
2.  Run the Python script:
    ```bash
    python YağmurDoğan_121200126_codes.py
    ```
3.  Follow the terminal prompts to enter your age, weight, and goals.
