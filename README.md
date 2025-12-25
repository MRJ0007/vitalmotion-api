🫀 VitalMotion

Real‑Time Health Monitoring & AI‑Assisted Alert System

VitalMotion is an end‑to‑end, real‑time health monitoring platform that collects vital sign data from IoT sensors, detects abnormal conditions, and provides explainable, AI‑assisted alerts to support early intervention.

The system is designed to work beyond hospitals — in homes, remote areas, workplaces, and emergency scenarios — where continuous monitoring and timely alerts are critical.


---

🚨 Problem Statement

Many health emergencies occur because abnormal vital signs go unnoticed or are detected too late, especially outside hospital environments such as homes, rural areas, industrial workplaces, or during patient transport.

Existing solutions often:

Focus only on raw data collection

Require manual monitoring

Lack clear, explainable alerts

Are tightly coupled to specific hardware



---

💡 Solution: VitalMotion

VitalMotion provides a complete monitoring pipeline that converts real‑time sensor data into actionable insights.

It:

Continuously ingests vital sign data

Automatically detects abnormal conditions

Triggers real‑time alerts

Uses AI to explain why an alert occurred

Visualizes trends on a live dashboard


The system is hardware‑agnostic, modular, and designed for scalability.


---

🩺 What We Monitor

Currently supported vital signs:

❤️ Heart Rate (BPM)

🫁 Blood Oxygen Saturation (SpO₂)

🌡️ Body Temperature


These parameters provide early indicators of abnormal physiological conditions that may require attention.


---

⚙️ System Architecture

[ IoT / Wearable Sensors ]
            ↓
      FastAPI Backend
            ↓
   Rule‑Based Alert Engine
            ↓
 GPT‑Powered Explanation Layer
            ↓
   Azure Cosmos DB (MongoDB API)
            ↓
   React Live Dashboard
            ↓
     Alerts & AI Insights


---

🧠 Explainable AI‑Assisted Analysis

VitalMotion integrates a GPT‑based explanation layer using Azure OpenAI.

The AI does not perform diagnosis or prediction.

Instead, it:

Converts alerts into human‑readable explanations

Summarizes recent vital‑sign trends

Classifies system status (Normal / Warning / Critical)

Suggests responsible next steps (monitoring or medical consultation)


All clinical decisions remain rule‑based and transparent, ensuring trust and explainability.


---

🧪 Demo Flow

1. Sensor (or simulated device) sends vital data


2. Backend processes and stores the data


3. Alerts are generated if thresholds are crossed


4. Dashboard updates live


5. AI explains the patient condition



> A simulation mode is available to ensure reliable demonstrations even if physical sensors are unavailable.




---

🚑 Use Cases (Beyond Hospitals)

Home healthcare & elderly monitoring

Rural and remote healthcare access

Ambulances and emergency transport

Industrial safety (mines, factories)

Sports & fitness monitoring

Quarantine and isolation scenarios



---

🛡️ Responsible Use

VitalMotion is a prototype and decision‑support system.

It is not a medical diagnostic device and does not replace healthcare professionals. Real‑world deployment would require medical certification and regulatory approvals.


---

🛠️ Tech Stack

Backend

FastAPI (Python)

Azure Cosmos DB (MongoDB API)

Azure OpenAI (GPT‑based explanations)


Frontend

React

Vite

Recharts


Tools & Platforms

GitHub

GitHub Student Developer Pack

Azure for Students



---

🚀 Future Scope

Additional vitals (ECG, blood pressure, respiration rate)

Wearable‑ready hardware design

Doctor / caregiver role‑based dashboards

Offline buffering for low‑connectivity regions

Regulatory‑ready deployment



---

👤 Author

Maniraj (MRJ0007)
Student Developer | Full‑Stack & IoT Enthusiast

Project built as part of GitHub Education × Microsoft Imagine Cup
