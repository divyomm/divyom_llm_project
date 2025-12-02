# NEXUS - Live Biometric Fitness Dashboard
**Student Name:** Divyom Singh  2210110266   
**Course:** MAT496 Monsoon 2025

## Overview
NEXUS PRO is an intelligent fitness agent designed to solve the problem of generic, non-personalized workout advice. It acts as a biomechanical consultant that accepts specific user constraints (biometrics, equipment access, experience level) and outputs a medically accurate, data-driven action plan.

My project processes user inputs through a custom logic engine, fetches real-time data from an external source (API-Ninjas), and presents the information in a highly structured format (Pandas DataFrames, Radar Charts, and CSV reports). It calculates metabolic baselines, visualizes training load vectors, and generates a complete weekly split protocol.

## Reason for picking up this project
I chose this project to demonstrate how an "Intelligent Agent" can act as a bridge between raw data and human decision-making. This aligns with the MAT496 course content in several key ways:

1.  **Structured Output:** A core theme of the course was formatting unstructured data. My agent takes raw API JSON responses and restructures them into clean, human-readable Pandas DataFrames and visual Charts.
2.  **Tool Calling:** Similar to how LLMs call tools, my agent uses Python `requests` to call an external tool (The API-Ninjas Fitness Database) to retrieve information it does not possess internally.
3.  **Agentic Workflow:** The system follows a State-Node logic flow: Input -> Biometric Processing -> API Data Retrieval -> Volume Injection -> Final Visualization.
4.  **Creativity:** I moved beyond simple text generation to build a "Multimodal Output" dashboard (Text + Data Tables + Visual Graphs + Downloadable Files), solving a real-world problem with high reliability.

## Video Summary Link:
https://drive.google.com/file/d/1i90WM22nurcOXyorpGc6Fi8QAsEmMwIM/view?usp=sharing

*(Note: The video demonstrates the agent taking inputs (Weight, Goal), executing the logic, and producing the output (Charts/Tables) as per submission requirements.)*

## Live Demo Link:
https://divyomm-divyom-llm-project-fitness-agent-yiajar.streamlit.app/

## Plan
I planned to execute these steps to complete my project. All steps have been executed and committed to the repository history.

- [DONE] **Step 1: Setup & Core Logic:** Forked repository, initialized Streamlit app, and built the basic Python functions to handle user inputs (Weight, Goal, Equipment).
- [DONE] **Step 2: Biometric Engine:** Implemented the mathematical logic to calculate BMI, Caloric Burn, and Safety Protocols (e.g., detecting obesity and adjusting intensity).
- [DONE] **Step 3: User Interface Overhaul:** Injected custom CSS to create a "Dark Mode Glassmorphism" UI for a professional, modern aesthetic.
- [DONE] **Step 4: External Tool Integration:** Connected the agent to the **API-Ninjas Fitness API** to replace hardcoded data with live, real-time exercise databases.
- [DONE] **Step 5: Smart Volume Logic:** Built an algorithm to inject specific "Sets & Reps" into the raw API data based on the user's specific training focus (Strength vs. Endurance).
- [DONE] **Step 6: Visualization:** Integrated Matplotlib to generate dynamic Radar Charts (Load Balance) and Donut Charts (Nutrition) that update in real-time.
- [DONE] **Step 7: Final Polish & Documentation:** Cleaned up code, verified `requirements.txt` for cloud deployment, recorded demo video, and finalized the README.

## Conclusion:
I had planned to achieve a fully functional, crash-proof fitness agent that provides more than just text output. I think I have **achieved the conclusion satisfactorily**.

**Reason for satisfaction:**
The final application successfully integrates multiple technologies (Streamlit, Pandas, Matplotlib, Requests) into a cohesive dashboard. It handles edge cases (like high BMI) with safety logic, fetches real data from the internet without errors, and provides a level of visual polish that exceeds a standard script. The "Smart Volume" algorithm successfully bridges the gap between raw data and actionable advice.