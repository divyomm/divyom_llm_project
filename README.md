# NEXUS - Live Biometric Fitness Dashboard
**Student Name:** Divyom Singh  2210110266   
**Course:** MAT496 Monsoon 2025

## 🔴 Live Demo
https://divyomm-divyom-llm-project-fitness-agent-yiajar.streamlit.app/


## 📖 Project Description
**NEXUS** is a data-driven fitness intelligence agent designed to generate medically accurate workout protocols using live external data.

Unlike standard static workout generators, NEXUS connects to the **API-Ninjas Fitness Database** to fetch real-time exercise metadata. It then applies a custom **"Smart Volume Algorithm"** to inject specific set/rep schemes based on the user's biomechanical goals (Strength vs. Endurance) and safety requirements (BMI-based impact adjustment).

## 🚀 Key Features

### 1. Live Data Stream (External API)
* **Integration:** Connects to the **API-Ninjas** REST API.
* **Function:** Dynamically fetches exercises based on target muscle (e.g., Chest, Quadriceps) and difficulty level.
* **Smart Filtering:** Uses Python logic to filter raw API results by equipment availability (ensuring "Bodyweight" users never see machine exercises).

### 2. Algorithmic Logic Engines
* **Biometric Safety Net:** Automatically calculates BMI and categorizes health risk (Normal vs. Obese).
* **Adaptive Protocol:** If a user is classified as "Obese" (>30 BMI), the system overrides standard hypertrophy protocols with "Low Impact" volume settings to prevent joint injury.
* **Smart Volume Injection:** Assigns specific load vectors (e.g., "5 Sets x 5 Reps" for Strength) to the raw exercise data.

### 3. Visual Data Analytics
* **Vector Analysis:** Uses **Matplotlib** to generate a real-time Radar Chart visualizing the training load distribution (Cardio vs. Strength vs. Mobility).
* **UI Design:** Features a custom "Dark Mode Glassmorphism" interface built with CSS injection.

### 4. Interactive Elements
* **Smart Links:** Auto-generates clickable **YouTube Search Queries** for every exercise.
* **Data Export:** Allows users to download their customized protocol as a `.csv` file for offline tracking.

## 🛠️ Tech Stack
* **Frontend:** Python Streamlit
* **Data Handling:** Pandas (DataFrames & CSV Export)
* **Visualization:** Matplotlib (Radar Charts)
* **Networking:** Requests (API HTTP Calls)

## ⚙️ How to Run Locally

1.  **Clone the Repository:**
    ```bash
    git clone
    cd divyom_llm_project
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application:**
    ```bash
    streamlit run fitness_agent.py
    ```

4.  **API Key Setup:**
    * The app requires a free **API-Ninjas Key** to fetch data.
    * Enter the key in the sidebar when the app launches.

## 🎥 Video Walkthrough
https://drive.google.com/file/d/1i90WM22nurcOXyorpGc6Fi8QAsEmMwIM/view?usp=sharing