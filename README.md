# 🎓 Career Guidance Agent
### Personalised AI Career Counsellor for AP & Telangana Students

---

## What This Does

An intelligent AI career guidance agent exclusively built for students who have completed **10th** or **Intermediate** in Andhra Pradesh and Telangana. It works like a highly experienced counsellor who knows every single opportunity available — and guides the student personally based on their marks, interests, income, and background.

---

## Features

- ✅ Complete list of every opportunity after 10th and Inter — nothing missed
- ✅ Flip/expandable cards with full details — exams, eligibility, official links
- ✅ Personalised AI guidance using Groq LLaMA 3.3 70B
- ✅ Live search via Tavily on official government websites
- ✅ Downloadable professional PDF report
- ✅ Scholarships filtered by caste, income, and state
- ✅ Government jobs — APPSC, TSPSC, SSC, Railways, Police, Defence
- ✅ RGUKT / IIIT Basara eligibility check
- ✅ Works for students from any state — AP/TS focus with national coverage

---

## Project Structure

```
career_agent/
├── .env                          ← Your API keys (fill this first)
├── app.py                        ← Main Streamlit UI — all 5 screens
├── agent.py                      ← LangChain + Groq AI agent logic
├── search_tools.py               ← Tavily live search tools
├── pdf_generator.py              ← ReportLab PDF report generator
├── config.py                     ← Load and validate API keys
├── data/
│   ├── opportunities_10th.json   ← All paths after 10th (complete data)
│   └── opportunities_inter.json  ← All paths after Inter by stream
├── requirements.txt
└── README.md
```

---

## Setup — Step by Step

### Step 1 — Get Free API Keys

**Groq API Key (Free)**
1. Go to https://console.groq.com
2. Sign up for free
3. Click "API Keys" → "Create API Key"
4. Copy the key

**Tavily API Key (Free — 1000 searches/month)**
1. Go to https://app.tavily.com
2. Sign up for free
3. Copy your API key from dashboard

---

### Step 2 — Add API Keys to .env file

Open the `.env` file and replace the placeholders:

```
GROQ_API_KEY=gsk_your_actual_groq_key_here
TAVILY_API_KEY=tvly_your_actual_tavily_key_here
```

---

### Step 3 — Install Python

Make sure Python 3.10 or higher is installed.
Download from: https://www.python.org/downloads/

---

### Step 4 — Install Dependencies

Open terminal/command prompt in the `career_agent` folder and run:

```bash
pip install -r requirements.txt
```

This installs:
- streamlit
- langchain
- langchain-groq
- langchain-community
- tavily-python
- reportlab
- python-dotenv

---

### Step 5 — Run the App

```bash
streamlit run app.py
```

The app will open automatically at: **http://localhost:8501**

---

## How to Use

### Screen 1 — Choose Level
Select **10th Completed** or **Inter Completed**

### Screen 2 — Explore All Opportunities
- If Inter selected → first pick your stream (MPC/BiPC/MEC/CEC/HEC/Vocational)
- All opportunities shown as expandable cards
- Click any card to see full details — exams, colleges, jobs, links
- Explore freely before filling any form

### Screen 3 — Your Profile Form
Fill in:
- Name, gender, marks, district, state
- Caste category, family income
- Interests (checkboxes)
- Any additional info

### Screen 4 — AI Processing
Live progress screen showing the agent working:
- Searching exam notifications
- Finding college cutoffs
- Checking scholarships
- Building roadmap

### Screen 5 — Results
- Complete personalised guidance on screen
- Download full PDF report button

---

## Official Websites Used for Live Search

| Purpose | Website |
|---|---|
| AP EAMCET | sche.ap.gov.in |
| TS EAMCET | tsche.ac.in |
| POLYCET AP | polycetap.nic.in |
| POLYCET TS | polycetts.nic.in |
| RGUKT | rgukt.ac.in |
| AP Scholarships | apepass.apcfss.in |
| TS Scholarships | telanganaepass.cgg.gov.in |
| National Scholarships | scholarships.gov.in |
| APPSC | appsc.gov.in |
| TSPSC | tspsc.gov.in |
| SSC Jobs | ssc.nic.in |
| Railways | rrbapply.gov.in |
| AP Police | slprb.ap.gov.in |
| TS Police | tslprb.in |
| Indian Army | joinindianarmy.nic.in |
| NEET / JEE | nta.ac.in |
| AP ITI | apitiadmissions.nic.in |
| TS ITI | itits.telangana.gov.in |
| APSSDC Skills | apssdc.in |
| TSSDC Skills | tssdc.telangana.gov.in |
| UPSC | upsc.gov.in |
| CLAT | consortiumofnlus.ac.in |
| NALSAR | nalsar.ac.in |

---

## Tech Stack

| Layer | Tool | Cost |
|---|---|---|
| LLM | Groq — LLaMA 3.3 70B | Free |
| Agent Framework | LangChain | Free |
| Live Search | Tavily API | Free (1000/month) |
| PDF Generation | ReportLab | Free |
| UI | Streamlit | Free |
| Language | Python | Free |

**Total cost: ₹0 — Completely Free**

---

## Troubleshooting

**"GROQ_API_KEY not found" error**
→ Make sure you filled the `.env` file correctly. No spaces around `=`.

**"No module named streamlit" error**
→ Run `pip install -r requirements.txt` again

**Agent takes too long**
→ Normal — it is searching live websites. Usually takes 30-60 seconds.

**PDF download not working**
→ Make sure reportlab is installed: `pip install reportlab`

---

## Important Note

This app uses AI-generated guidance based on your profile and live data. Always verify exam dates, eligibility criteria, and application deadlines from official websites before applying. Career guidance is based on current trends and individual outcomes depend on personal effort and preparation.

---

Built with ❤️ for AP and Telangana students
