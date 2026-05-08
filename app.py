from flask import Flask, request, jsonify
import sqlite3
import re
import requests
import time
import csv
from datetime import datetime

LOG_FILE = "evaluation_results.csv"

def log_and_return(answer, q, start):
    end = time.time()
    response_time = end - start

    print("Response time:", response_time)

    with open(LOG_FILE, "a", newline="", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(),
            q,
            answer,
            response_time
        ])

    return jsonify({"answer": answer})

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

📄 **Professional Resume Tips**

✔ Keep resume to **1–2 pages**
✔ Use **clear headings and bullet points**
✔ Add **technical skills section**
✔ Mention **projects with outcomes**
✔ Quantify achievements
✔ Avoid grammatical errors
✔ Use simple fonts
✔ Tailor resume for job role
✔ Add **GitHub / LinkedIn links**

📌 **Recommended Resume Sections**

• Career Objective  
• Technical Skills  
• Projects  
• Internships  
• Certifications  
• Education  

---

🌐 **Useful Resume Resources**

1️⃣ GeeksforGeeks Resume Guide  
https://www.geeksforgeeks.org/how-to-build-a-resume/

2️⃣ Harvard Resume Template  
https://hwpi.harvard.edu/files/ocs/files/hes-resume-cover-letter-guide.pdf

3️⃣ Resume Worded Tips  
https://resumeworded.com/resume-tips

4️⃣ LinkedIn Resume Writing Guide  
https://www.linkedin.com/pulse/how-write-good-resume-freshers/

5️⃣ Overleaf Professional Resume Templates  
https://www.overleaf.com/gallery/tagged/cv

---

🎥 **Resume Building Tutorials**

• https://youtu.be/Tt08KmFfIYQ  
• https://youtu.be/u75hUSShvnc

---

💡 **Extra Tip**

Good resumes usually contain:

• 2–3 strong projects  
• GitHub profile  
• Internship experience  
• Certifications  

A strong resume greatly increases **placement chances 🚀**
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

🎤 **Interview Preparation Guide for Freshers**

------------------------------

📌 **Common Interview Questions**

1. Tell me about yourself  
2. Why should we hire you?  
3. What are your strengths and weaknesses?  
4. Explain your final year project  
5. Where do you see yourself in 5 years?  
6. Describe a challenging situation you solved  
7. Why do you want to work in our company?

------------------------------

💻 **Technical Interview Preparation**

Practice these topics:

✔ Data Structures & Algorithms  
✔ OOPS Concepts  
✔ DBMS  
✔ Operating Systems  
✔ SQL  
✔ System Design Basics  

Practice coding on:

• https://leetcode.com  
• https://www.hackerrank.com  
• https://www.geeksforgeeks.org  
• https://www.codechef.com  

------------------------------

🤖 **Free AI Mock Interview Platforms**

1️⃣ Google Interview Warmup  
https://grow.google/certificates/interview-warmup/

2️⃣ Final Round AI (Free trial)  
https://www.finalroundai.com

3️⃣ Interviewing.io  
https://interviewing.io

4️⃣ Pramp (Free Mock Interviews)  
https://www.pramp.com

5️⃣ MyInterviewPractice  
https://myinterviewpractice.com

------------------------------

📄 **Interview Preparation PDFs**

1️⃣ HR Interview Questions PDF  
https://www.geeksforgeeks.org/common-hr-interview-questions/

2️⃣ Technical Interview Guide  
https://www.tutorialspoint.com/interview_questions/index.htm

3️⃣ Placement Interview Questions PDF  
https://www.javatpoint.com/interview-questions

4️⃣ Top 100 Coding Interview Questions  
https://www.geeksforgeeks.org/top-100-data-structure-and-algorithms-dsa-interview-questions/

------------------------------

🎥 **Best YouTube Interview Preparation**

1️⃣ Tech Interview Preparation  
https://youtu.be/1mHjMNZZvFo

2️⃣ HR Interview Questions  
https://youtu.be/9FgfsLa_SmY

3️⃣ Google Interview Tips  
https://youtu.be/kayOhGRcNt4

------------------------------

📅 **Daily Interview Preparation Plan**

Day Plan:

• 2 hrs Coding Practice  
• 1 hr Core Subjects (DBMS/OS/OOPS)  
• 30 mins HR Questions  
• 30 mins Mock Interview  

------------------------------

💡 **Pro Tips**

✔ Know your resume completely  
✔ Explain your projects clearly  
✔ Practice speaking confidently  
✔ Research the company before interview  
✔ Always ask a question to interviewer

Good preparation leads to **great placements 🚀**
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

import re

def extract_company(q):

    stop = [
        "how","many","got","placed","students","student","in","count","of",
        "skills","skill","required","hiring","process","for","company"
    ]

    # remove punctuation like ?,.,!
    q = re.sub(r'[^\w\s]', '', q.lower())

    words = q.split()

    filtered = [w for w in words if w not in stop]

    if len(filtered) > 0:
        return filtered[0]   # return first meaningful word

    return ""

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
    start=time.time()
    data = request.get_json()
    q = data.get("question", "")
    print("Question received:", q)
    ql = q.lower()

    # Greeting
    if ql.strip() in ["hi","hello","hey"]:
        return log_and_return("Hello 👋 I am your Placement Assistant. How may I help you?",q,start)

    # COUNT
    if "how many" in ql or "count" in ql:

        company = extract_company(ql)

        if company.strip()=="":
            return log_and_return(f"Total placed students: {total_students()}.", q, start)

        n = count_students(company)

        if n>0:
            return log_and_return(f"{n} students placed in {company.title()}.", q, start)

        return log_and_return("Company not found in database.", q, start)
    # TECH
    for t in TECH:
        if t in ql:
            return log_and_return(TECH[t], q, start)

    # HIRING PROCESS
    if "hiring" in ql or "process" in ql:

        company = extract_company(ql)

        for c in HIRING:
            if c in company:
                return log_and_return(HIRING[c], q, start)
        return log_and_return("Hiring process not available for this company.", q, start)
    # SKILLS
    # SKILLS / TECHNOLOGIES
    if "skill" in ql or "technologies" in ql or "learn" in ql:

        company = extract_company(ql)

        if company in COMPANY_SKILLS:
            return log_and_return(COMPANY_SKILLS[company], q, start)
        if company:
            ans = ai(f"What skills are required for {company} freshers?")
        else:
            ans = ai("What skills should a student learn for placements?")
        if ans:
            return log_and_return(ans, q, start)
        
    # RESUME TIPS
    if "resume" in ql or "cv" in ql:
        return log_and_return(RESUME_TIPS, q, start)

    # INTERVIEW PREP
    if "interview" in ql:
        return log_and_return(INTERVIEW_PREP, q, start)


    # GENERAL
    ans = ai("You are placement assistant:\n"+q)

    if ans:
        reply = ans
    else:
        reply = "Sorry, could not understand."

    return log_and_return(reply, q, start)  
    
    




# ================= RUN =================

if __name__=="__main__":
    app.run(port=5000, debug=True)