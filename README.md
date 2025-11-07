# 🚒 Emergency Stations Optimization (P-Center Problem)

## 📘 Overview
This project implements a **P-Center optimization model** for planning the placement of **emergency stations** (fire, ambulance, or rescue).  
It determines the best station locations to minimize the **maximum response distance (z\*)** between any neighborhood and its nearest station.

The tool is an **interactive Streamlit web app** where users can enter data, compute results, and visualize station coverage on a map-like plot.

---

## 🧭 Problem Description
City planners must decide where to build a limited number of emergency stations so that every neighborhood can be reached quickly during an emergency.

The **P-Center model** mathematically minimizes the worst-case distance between demand points and facilities:
Minimize:  z = max_j ( min_i d_ij )

where:
I  = candidate station sites
J  = demand points (neighborhoods)
d_ij = distance between station i and neighborhood j
p  = number of stations to build
  

---

## 🧩 Features
✅ User-friendly **Streamlit web interface**  
✅ Manual or JSON data input  
✅ Live visualization (stations, neighborhoods, coverage circles)  
✅ Calculates minimum **maximum response distance (z\*)**  
✅ Assigns each neighborhood to its nearest station  
✅ Input validation & warnings for incorrect data  

---

## ⚙️ Installation

### 1️⃣ Clone or Download
```bash
git clone https://github.com/yourusername/Emergency-Stations-Optimization.git
cd Emergency-Stations-Optimization
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App

```bash
streamlit run pcenter_app.py
```

Then open the link displayed in your terminal (usually [http://localhost:8501](http://localhost:8501)).

---

## 🧮 Example Input (JSON mode)

```json
{
  "coords": {
    "1": [0, 0],
    "2": [0, 10],
    "3": [10, 0],
    "4": [10, 10],
    "5": [20, 4],
    "6": [25, 10],
    "7": [30, 0],
    "8": [35, 8]
  },
  "p": 3
}
```

---

## 📊 Output

| Metric                         | Description                            |
| ------------------------------ | -------------------------------------- |
| **Stations Opened**            | IDs of chosen locations                |
| **Max Response Distance (z*)** | Worst-case service distance (km)       |
| **Assignments**                | Which station covers each neighborhood |
| **Visualization**              | Interactive map with coverage zones    |

---

## 🧠 Methodology

* **Model type:** Discrete P-Center
* **Decision variable:** which `p` sites to open
* **Algorithm:** combinatorial search (`itertools.combinations`)
* **Distance metric:** Euclidean (km)
* **Objective:** minimize the largest service distance (fair response coverage)

---

## 🏙️ Real-Life Applications

| Domain                      | Example                                      |
| --------------------------- | -------------------------------------------- |
| **Emergency Services**      | Fire, ambulance, and rescue station planning |
| **Public Health**           | Clinic or vaccination center locations       |
| **Disaster Management**     | Evacuation and relief center placement       |
| **Infrastructure Planning** | Utility service hubs (energy, water, etc.)   |

---

## 🧾 Folder Structure

```
📁 Emergency-Stations-Optimization
│
├── pcenter_app.py           # Main Streamlit app
├── requirements.txt         # Dependencies list
└── README.md                # Documentation
```

---

## ⚠️ Common Errors

| Issue            | Cause                      | Solution            |
| ---------------- | -------------------------- | ------------------- |
| `p > n`          | Too many stations          | Reduce p            |
| `Invalid JSON`   | Formatting or missing keys | Fix braces/commas   |
| `Too many nodes` | n > 25 (slow)              | Use smaller dataset |
| Large z* value   | Distant coordinates        | Adjust data scale   |

---

## 🧩 Future Enhancements

* Continuous P-Center (stations can be placed anywhere)
* Integration with geographic maps (e.g., OpenStreetMap, Folium)
* Export report as PDF or CSV
* Optimization via solver for larger datasets

---

## 👩‍💻 Author

Maral Abay, Koshanova Aigerim, Kassymkyzy Raikhan
Department of Computer Science / IT-2303
Astana IT University — 2025

---

