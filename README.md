
# 🔋 EV Battery Monitoring System

An interactive Electric Vehicle (EV) Battery Monitoring System simulation built with Python, Streamlit, Pandas, and Plotly.

## 📌 About the Project

This project demonstrates how a Battery Management System (BMS) dashboard can display battery parameters and visualize performance trends.

**Important:** This is a software simulation. Sensor values are randomly generated and are not collected from a real battery.

## ✨ Features

- Battery State of Charge (SOC) monitoring
- Simulated voltage and current readings
- Power calculation in kilowatts
- Estimated remaining energy based on SOC
- Battery temperature monitoring and demo alerts
- Illustrative State of Health (SOH) display
- Interactive voltage, temperature, and SOC charts
- Recent readings table
- CSV export
- Reset simulation controls

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly

## 📂 Project Structure

```text
ev-battery-monitor/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd ev-battery-monitor
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
python -m streamlit run app.py
```

The dashboard should open in your browser. If it does not, follow the local URL printed in the terminal.

## 🔬 Electrical Engineering Concepts

- Voltage (V)
- Current (A)
- Electrical power: P = V × I
- State of Charge (SOC)
- Remaining energy estimation
- Battery temperature monitoring

The dashboard calculates power from simulated voltage and current readings. The SOH value is illustrative and is not calculated from actual battery degradation data.

## 🚀 Future Improvements

- Import real sensor datasets
- Add battery charging and discharging profiles
- Use historical data for analysis
- Connect compatible hardware in a controlled lab environment
- Add automated tests
- Estimate SOC from real measurements

## 👨‍💻 Author

Created as an Electrical Engineering and Python learning project.

## 📄 License

This project is available under the MIT License.