import json
import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from config import GROQ_API_KEY, GROQ_MODEL
from search_tools import get_search_tools

os.environ["GROQ_API_KEY"] = GROQ_API_KEY


def build_student_profile_text(profile: dict) -> str:
    """Convert student profile dict to readable text for the agent."""
    level = profile.get("level", "")
    stream = profile.get("stream", "N/A")
    name = profile.get("name", "Student")
    marks = profile.get("marks", "")
    district = profile.get("district", "")
    state = profile.get("state", "")
    caste = profile.get("caste", "")
    income = profile.get("income", "")
    gender = profile.get("gender", "")
    interests = profile.get("interests", [])
    additional = profile.get("additional_info", "")

    interests_text = ", ".join(interests) if interests else "Not specified"

    profile_text = f"""
STUDENT PROFILE:
================
Name: {name}
Education Level: {level}
{"Stream: " + stream if level == "Inter Completed" else ""}
Marks/Percentage: {marks}%
District: {district}
State: {state}
Caste Category: {caste}
Family Annual Income: Rs {income}
Gender: {gender}
Interests and Aptitudes: {interests_text}
Additional Information: {additional if additional else "None provided"}
"""
    return profile_text.strip()


def get_career_guidance(profile: dict, progress_callback=None) -> dict:
    """
    Main function to get AI-powered career guidance for a student.
    Returns a dict with guidance sections.
    """

    def update_progress(message: str):
        if progress_callback:
            progress_callback(message)

    update_progress("Reading and analysing your complete profile...")

    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0.3,
        max_tokens=1200,
    )

    tools = get_search_tools()

    system_prompt = """You are an expert career guidance counsellor with 30+ years of experience 
guiding students in India, especially from Andhra Pradesh and Telangana. You have deep knowledge of:

1. All entrance exams — JEE, NEET, EAMCET, POLYCET, CLAT, NDA, CA Foundation and every other exam
2. All AP and Telangana state government schemes, scholarships, and opportunities
3. Central government jobs — SSC, Railways, Defence, Post Office
4. All professional courses — Engineering, Medical, Law, CA, MBA and all others
5. Current job market trends, salary expectations, and career growth paths
6. Scholarship schemes — AP ePass, TS ePass, NSP, PM YASASVI and all others
7. RGUKT/IIIT Basara eligibility and benefits
8. Vocational, ITI, Polytechnic pathways

Your guidance style:
- Be like a caring, knowledgeable elder who genuinely wants the student to succeed
- Be HONEST — do not give false hope. If marks are low, say so kindly and suggest realistic options
- Be SPECIFIC — mention exact exam names, websites, cutoffs, deadlines
- Be COMPREHENSIVE — do not miss any relevant opportunity for this student
- Prioritise based on the student's actual marks, income, and interests
- Always mention scholarships the student qualifies for — many students miss free money
- Give a clear action plan — what to do this week, this month, in 3 months

IMPORTANT RULES:
- Always search for the latest information before giving advice
- Mention official websites for every exam and scholarship
- Consider the student's financial situation when recommending private vs government colleges
- For low-income students, always highlight free/fully funded options first (RGUKT, ITI govt, PMKVY)
- Be honest about difficulty levels — e.g. "IIT requires top 1% in JEE, which needs serious preparation"
- Always give at least 3 career paths — primary recommendation, alternative, and backup
- Mention both immediate opportunities (can apply now) and future preparation (start now for later)

Respond in well-structured English. Use clear headings and organized sections."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=3,
        handle_parsing_errors=True,
    )

    profile_text = build_student_profile_text(profile)
    level = profile.get("level", "")
    stream = profile.get("stream", "")
    marks = float(profile.get("marks", 0))
    interests = profile.get("interests", [])
    income = profile.get("income", "")
    caste = profile.get("caste", "")
    gender = profile.get("gender", "")
    state = profile.get("state", "AP/Telangana")

    update_progress("Searching latest exam notifications and cutoffs...")

    query = f"""
{profile_text}

Provide complete personalised career guidance for this student.

## SECTION 1: PROFILE ANALYSIS
Analyse strengths, realistic opportunities, honest assessment based on marks and background.

## SECTION 2: TOP 3 RECOMMENDED CAREER PATHS
For each path:
- Why it suits this student
- Entrance exams with websites
- Top colleges in AP/Telangana
- Expected salary
- Next 3 months action steps

## SECTION 3: OTHER VIABLE OPPORTUNITIES
All other realistic options briefly.

## SECTION 4: GOVERNMENT JOB OPPORTUNITIES
APPSC, TSPSC, SSC, Railways, Police, Defence — specific to their qualification.

## SECTION 5: SCHOLARSHIPS
Based on caste ({caste}), income ({income}), state ({state}), gender ({gender}).
List scholarships with amounts and websites.

## SECTION 6: HONEST REALITY CHECK
Challenges and what to do about them.

## SECTION 7: 30-DAY ACTION PLAN
Week 1, Week 2, Week 3-4, Next 3 months.

## SECTION 8: IMPORTANT LINKS
All official websites mentioned.


Search for latest exam dates and notifications before responding. Be thorough, honest, and genuinely helpful.
"""

    update_progress("Analysing eligible scholarships and financial aid...")
    update_progress("Checking government job opportunities...")
    update_progress("Building your personalised roadmap...")

    try:
        result = agent_executor.invoke({
            "input": query,
            "chat_history": [],
        })
        guidance_text = result.get("output", "")
    except Exception as e:
        guidance_text = f"Error generating guidance: {str(e)}\n\nPlease try again."

    update_progress("Guidance generation complete!")

    return {
        "profile": profile,
        "guidance": guidance_text,
        "profile_summary": build_student_profile_text(profile)
    }


def get_quick_summary(profile: dict) -> str:
    """Get a quick 3-line summary for the results page header."""
    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0.2,
        max_tokens=300,
    )

    profile_text = build_student_profile_text(profile)

    response = llm.invoke([
        HumanMessage(content=f"""
{profile_text}

In exactly 3 sentences, give:
1. The single best career recommendation for this student and why.
2. The most important exam they should register for right now.
3. One scholarship they should apply for immediately.

Be specific, honest, and encouraging. No bullet points — 3 plain sentences.
""")
    ])

    return response.content
