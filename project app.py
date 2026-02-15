from flask import Flask, request, jsonify
import sqlite3
import re
import requests

# ================= OPENROUTER =================

OPENROUTER_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct:free"
app = Flask(__name__)

# ================= DATABASE =================

def db():
    return sqlite3.connect("placements.db")

def normalize(s):
    return re.sub(r'\s+', '', s.lower())

def total_students():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM placements")
    r = cur.fetchone()[0]
    con.close()
    return r

def count_students(company):

    con = db()
    cur = con.cursor()
    cur.execute("SELECT Company FROM placements")
    rows = cur.fetchall()

    count = 0
    for r in rows:
        if normalize(company) in normalize(r[0]):
            count += 1

    con.close()
    return count

# ================= TECH =================

TECH = {

    "python": """Python Topics:
• Basics & Syntax
• OOPS Concepts
• Lists, Tuples, Sets, Dictionaries
• File Handling
• Exception Handling
• Pandas & NumPy
• APIs & Requests
• Mini Projects
• Real Time Projects
• Interview Questions""",

    "java": """Java Topics:
• Core Java
• OOPS Concepts
• Collections Framework
• Multithreading
• Exception Handling
• JDBC
• Mini Projects""",

    "oops": """OOPS Concepts:
• Class & Object
• Encapsulation
• Inheritance
• Polymorphism
• Abstraction
• Interfaces
• Method Overloading & Overriding""",

    "dsa": """DSA Topics:
• Arrays
• Strings
• Linked Lists
• Stack & Queue
• Trees
• Graphs
• Sorting Algorithms
• Searching Algorithms
• Recursion
• Time & Space Complexity""",

    "sql": """SQL Topics:
• Joins
• Subqueries
• Indexes
• Normalization
• Stored Procedures
• Views
• Constraints""",

    "dbms": """DBMS Topics:
• Normalization
• ER Diagrams
• Transactions
• ACID Properties
• Indexing
• Deadlocks""",

    "os": """Operating Systems:
• Process Scheduling
• Deadlocks
• Memory Management
• Paging
• Multithreading""",

    "aptitude": """Quantitative Aptitude:
• Percentages
• Profit & Loss
• Time & Work
• Time & Distance
• Ratio & Proportion
• Probability
• Permutation & Combination

Logical Reasoning:
• Coding-Decoding
• Blood Relations
• Directions
• Seating Arrangements
• Puzzles

Verbal Ability:
• Reading Comprehension
• Synonyms & Antonyms
• Sentence Correction
• Error Spotting
• Vocabulary""",

    "communication": """Communication Skills:
• Self Introduction
• HR Interview Questions
• Group Discussion
• Email Writing
• Presentation Skills""",

    "cloud": """Cloud Basics:
• AWS / Azure Basics
• Virtual Machines
• Storage
• Networking
• Deployment"""

}
# ================= COMPANY SKILLS =================

COMPANY_SKILLS = {

    "wipro": """Wipro Skills:
• Python / Java
• DSA
• SQL
• Cloud Basics
• Aptitude
• Communication""",

    "tcs": """TCS Skills:
• C / Java
• DBMS
• Operating Systems
• Aptitude
• Verbal Ability""",

    "infosys": """Infosys Skills:
• Java / Python
• OOPS
• SQL
• Software Engineering
• Communication""",

    "cognizant": """Cognizant Skills:
• Python
• DSA
• OOPS
• SQL
• Web Basics
• Aptitude""",

    "accenture": """Accenture Skills:
• Python / Java
• Cloud
• Web Development
• Aptitude
• Communication"""
}
# ================= RESUME TIPS =================

RESUME_TIPS = """Professional Resume Tips:

• Keep resume to 1–2 pages  
• Use clear headings and bullet points  
• Add technical skills section  
• Mention projects with outcomes  
• Quantify achievements  
• Avoid grammatical errors  
• Use simple fonts  
• Tailor resume for job role  
• Add GitHub / LinkedIn links  
• Avoid unnecessary personal details  

Recommended Sections:
✔ Career Objective  
✔ Technical Skills  
✔ Projects  
✔ Internships  
✔ Certifications  
✔ Education  
"""

# ================= INTERVIEW PREP =================

INTERVIEW_PREP = """Interview Preparation Guide:

Technical:
• Revise core subjects (DSA, OOPS, DBMS, OS)
• Practice coding problems
• Explain projects confidently

HR Round:
• Tell me about yourself
• Strengths & weaknesses
• Why should we hire you?
• Career goals

Behavioral:
• Teamwork examples
• Leadership situations
• Problem solving

Before Interview:
✔ Research company  
✔ Practice mock interviews  
✔ Prepare resume explanation  
✔ Dress professionally  
✔ Be confident  

Daily Preparation:
• 2 hrs coding
• 1 hr aptitude
• 1 hr revision
• 30 mins communication
"""

# ================= HIRING PROCESS =================

HIRING = {

    "wipro": """Wipro Hiring Process:
1. Online Aptitude Test
2. Technical Assessment
3. Technical Interview
4. HR Interview""",

    "tcs": """TCS Hiring Process:
1. NQT Exam
2. Technical Interview
3. Managerial Interview
4. HR Round""",

    "infosys": """Infosys Hiring Process:
1. Online Test
2. Technical Interview
3. HR Interview""",

    "cognizant": """Cognizant Hiring Process:
1. Aptitude Test
2. Technical Interview
3. HR Interview""",

    "accenture": """Accenture Hiring Process:
1. Cognitive Test
2. Coding Round
3. Communication Round
4. HR Discussion"""
}
# ================= COMPANY EXTRACT =================

def extract_company(q):

    stop = ["how","many","got","placed","students","student","in","count","of",
            "skills","skill","required","hiring","process","for"]

    words = q.lower().split()
    filtered = [w for w in words if w not in stop]

    return " ".join(filtered)

# ================= AI =================

def ai(prompt):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role":"user","content":prompt}]
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return None
    

# ================= API =================

@app.route("/ask",methods=["POST"])
def ask():

    q = request.json["question"]
    ql = q.lower()

    # Greeting
    if ql.strip() in ["hi","hello","hey"]:
        return jsonify({"answer":"Hello 👋 I am your Placement Assistant. How may I help you?"})

    # COUNT
    if "how many" in ql or "count" in ql:

        company = extract_company(ql)

        if company.strip()=="":
            return jsonify({"answer":f"Total placed students: {total_students()}."})

        n = count_students(company)

        if n>0:
            return jsonify({"answer":f"{n} students placed in {company.title()}."})

        return jsonify({"answer":"Company not found in database."})

    # TECH
    for t in TECH:
        if t in ql:
            return jsonify({"answer":TECH[t]})

    # HIRING PROCESS
    if "hiring" in ql or "process" in ql:

        company = extract_company(ql)

        for c in HIRING:
            if c in company:
                return jsonify({"answer":HIRING[c]})

        return jsonify({"answer":"Hiring process not available for this company."})

    # SKILLS
    # SKILLS / TECHNOLOGIES
    if "skill" in ql or "technologies" or "learn" in ql:

        company = extract_company(ql)

        if company in COMPANY_SKILLS:
            return jsonify({"answer":COMPANY_SKILLS[company]})

        ans = ai(f"What skills are required for {company} freshers?")
        if ans:
            return jsonify({"answer":ans})
        
    # RESUME TIPS
    if "resume" in ql or "cv" in ql:
        return jsonify({"answer": RESUME_TIPS})

    # INTERVIEW PREP
    if "interview" in ql:
        return jsonify({"answer": INTERVIEW_PREP})


    # GENERAL
    ans = ai("You are placement assistant:\n"+q)
    if ans:
        return jsonify({"answer":ans})

    return jsonify({"answer":"Sorry, could not understand."})   
    
    




# ================= RUN =================

if __name__=="__main__":
    app.run(port=5000)
