# FinAI
An intelligent, agent-based portfolio analysis system built using **CrewAI** and **Google Gemini**.   The system analyzes equity holdings, interprets market signals, evaluates portfolio risk, and generates structured investment reports.

# 📊 AI Portfolio Intelligence System

An intelligent, agent-based portfolio analysis system built using **CrewAI** and **Google Gemini**.  
The system analyzes equity holdings, interprets market signals, evaluates portfolio risk, and generates structured investment reports.

> ⚠️ For educational and research purposes only. Not investment advice.

---

## ✨ Key Features

- 📈 Market Signal Interpretation  
  - Trend analysis  
  - Moving average alignment  
  - RSI & volatility interpretation  
  - Price position vs 52-week range  

- 🧠 LLM-powered Decision Making  
  - Conservative, long-term analysis  
  - BUY / HOLD / REDUCE recommendations  
  - Confidence scoring  
  - Risk-aware reasoning  

- 🧮 Portfolio-Level Intelligence  
  - Concentration & allocation risk detection  
  - Portfolio Health Score (0–100)  
  - Identification of the single most important action  

- 📝 Professional Investment Reports  
  - Clean, structured summaries  
  - Stock-wise recommendations  
  - Portfolio risk overview  

- 🔐 Secure Configuration  
  - API keys managed via `.env`  
  - Secrets excluded via `.gitignore`  

---


Each agent has a **single responsibility**, making the system modular, explainable, and extensible.

---

## 🛠️ Tech Stack

- Python 3.10+
- CrewAI
- Google Gemini (`gemini-1.5-flash`)
- pandas / numpy
- python-dotenv

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd crew_finance

### setup 
python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt


GOOGLE_API_KEY=your_gemini_api_key_here

python main.py --file path/to/holdings.xlsx --broker groww




