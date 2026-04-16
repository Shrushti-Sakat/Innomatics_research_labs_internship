"""
AI Resume Screening System - Complete Standalone Runner
Runs the entire pipeline without needing Jupyter
"""

import os
import sys
import json
from datetime import datetime

# Set up environment
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("="*80)
print("AI RESUME SCREENING SYSTEM - COMPLETE RUN")
print("="*80)
print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Import required libraries
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    print("✓ LangChain libraries imported")
except ImportError as e:
    print(f"✗ Error importing LangChain: {e}")
    sys.exit(1)

# =========================================================================
# STEP 1: DEFINE PROMPTS AND DATA
# =========================================================================

# Sample Data
STRONG_CANDIDATE_RESUME = """
JOHN DOE
john.doe@email.com | (123) 456-7890 | LinkedIn: linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Data Scientist with 6 years of experience in machine learning, statistical analysis, and Python development. 
Proven track record of building and deploying predictive models in production environments.

EXPERIENCE

Senior Data Scientist | Tech Company Inc. | Jan 2022 - Present
- Developed and deployed 15+ machine learning models using Python, scikit-learn, and TensorFlow
- Led data pipeline optimization reducing processing time by 40%
- Implemented A/B testing framework using statistical analysis
- Mentored junior data scientists and conducted code reviews
- Used AWS (S3, EC2, SageMaker) for scalable infrastructure

Data Scientist | Analytics Corp | Jun 2020 - Dec 2021
- Built predictive models for customer churn (XGBoost, Random Forest) with 85% accuracy
- Created data visualizations using Tableau and Matplotlib
- Conducted SQL queries from PostgreSQL and MySQL databases
- Collaborated with product teams using Agile/Scrum methodology
- Implemented CI/CD pipelines using Git and Jenkins

Machine Learning Engineer | StartUp AI | Jan 2019 - May 2020
- Developed NLP models for text classification using NLTK and spaCy
- Built REST APIs using Flask for model deployment
- Implemented Docker containerization for application deployment
- Used Jupyter Notebook for exploratory data analysis

EDUCATION
M.S. in Data Science | University of Data | 2019
B.S. in Statistics | College of Science | 2017

TECHNICAL SKILLS
Programming Languages: Python, R, SQL, Java
ML Frameworks: TensorFlow, scikit-learn, PyTorch, XGBoost
Data Tools: Pandas, NumPy, Matplotlib, Seaborn, Plotly
Databases: PostgreSQL, MySQL, MongoDB, Redis
Cloud Platforms: AWS (S3, EC2, SageMaker), Google Cloud Platform
Other Tools: Git, Docker, Jupyter Notebook, Apache Spark, Tableau
Statistical Methods: Regression, Classification, Clustering, Time Series Analysis

CERTIFICATIONS
AWS Certified Machine Learning Specialty (2021)
Google Cloud Professional Data Engineer (2020)

PROJECTS
- Built end-to-end recommendation system using collaborative filtering (Python, Flask, PostgreSQL)
- Developed real-time sentiment analysis system for social media data (NLTK, Spark)
"""

AVERAGE_CANDIDATE_RESUME = """
ALICE SMITH
alice.smith@email.com | (234) 567-8901 | LinkedIn: linkedin.com/in/alicesmith

PROFESSIONAL SUMMARY
Data Analyst with 3 years of experience in data analysis, reporting, and basic statistical analysis. 
Comfortable with Python and SQL for data manipulation and visualization.

EXPERIENCE

Data Analyst | Software Solutions Ltd. | Jul 2022 - Present
- Analyzed business data using SQL queries from a Postgres database
- Created Excel dashboards and Power BI reports for stakeholders
- Performed basic statistical analysis and reporting
- Used Python (Pandas, NumPy) for data cleaning and analysis
- Collaborated with product teams on ad-hoc data requests

Junior Data Analyst | Marketing Agency | Feb 2021 - Jun 2022
- Extracted data from company databases using SQL
- Created charts and visualizations using Excel and Google Sheets
- Assisted in A/B testing analysis and reporting
- Basic Python scripting for data processing

Data Entry Specialist | Retail Corp | Jan 2020 - Jan 2021
- Entered and verified data in company systems
- Created basic reports in Excel

EDUCATION
B.S. in Business Administration | State University | 2020

TECHNICAL SKILLS
Programming: Python (pandas, NumPy basics), SQL
Tools: Excel, Power BI, Google Sheets
Databases: PostgreSQL, MySQL
Other: Git (basic), Jupyter Notebook (basic)
Statistical Knowledge: Descriptive statistics, basic A/B testing

PROJECTS
- Analyzed customer purchase data using pandas (personal project)
- Created sales dashboard in Power BI
"""

WEAK_CANDIDATE_RESUME = """
BOB JOHNSON
bob@email.com | (345) 678-9012

PROFESSIONAL SUMMARY
Enthusiastic professional interested in data science and analytics. Strong communication skills.

EXPERIENCE

Data Team Intern | Tech Company | Summer 2023
- Helped organize and sort datasets
- Assisted with Excel spreadsheet creation
- Attended data team meetings

Retail Associate | Store Inc. | 2022 - 2023
- Customer service and sales support

Office Administrator | Small Business | 2021 - 2022
- Administrative tasks and filing

EDUCATION
High School Diploma | Local High School | 2021

SKILLS
- Excel (basic)
- Microsoft Office
- Customer Service
- Strong work ethic
- Quick learner

LANGUAGES
- English (native)
- Spanish (conversational)
"""

JOB_DESCRIPTION = """
Senior Data Scientist - Senior Level

Company: Tech Innovators Inc.
Location: San Francisco, CA (Remote Available)

Position Overview
We are seeking an experienced Senior Data Scientist to join our growing AI/ML team. 
You will design and build machine learning pipelines, lead data-driven projects, 
and mentor junior team members.

Required Qualifications
- 5+ years of professional experience in data science or machine learning
- Master's degree in Data Science, Statistics, Computer Science, or related field
- Expert proficiency in Python for data analysis and modeling
- Strong SQL skills for data extraction and manipulation
- Hands-on experience with at least 2 ML frameworks (scikit-learn, TensorFlow, PyTorch, XGBoost)
- Experience with cloud platforms (AWS, GCP, or Azure)
- Proven ability to deploy models to production
- Strong statistical and mathematical foundation
- Experience with version control (Git)
- Excellent communication and mentoring abilities

Nice to Have
- PhD in a quantitative field
- Experience with big data technologies (Spark, Hadoop)
- NLP or deep learning specialization
- Published research or contributions to open-source ML projects
- Experience with MLOps and model monitoring

Responsibilities
- Develop and optimize machine learning models for various business problems
- Build end-to-end ML pipelines from data ingestion to model deployment
- Conduct exploratory data analysis and statistical testing
- Collaborate with engineers to productionize models
- Lead and mentor junior data scientists
- Present findings and recommendations to stakeholders
"""

print("✓ Sample data loaded (3 resumes, 1 job description)\n")

# =========================================================================
# STEP 2: CREATE PROMPTS AND CHAINS
# =========================================================================

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
json_parser = JsonOutputParser()

# Skill Extraction Prompt
skill_extraction_template = """You are an expert HR recruiter. Extract all skills from this resume.

RULES:
- Only extract EXPLICITLY mentioned skills
- Do NOT hallucinate skills
- Return valid JSON format

Resume:
{resume}

Return JSON:
{{
    "technical_skills": ["skill1", "skill2"],
    "tools_frameworks": ["tool1"],
    "soft_skills": ["skill1"],
    "experience_years": 0,
    "certifications": ["cert1"]
}}"""

skill_extraction_prompt = PromptTemplate(
    input_variables=["resume"],
    template=skill_extraction_template
)

skill_extraction_chain = (
    skill_extraction_prompt 
    | llm 
    | json_parser
)

# Job Requirements Prompt
job_requirement_template = """You are an expert HR recruiter. Extract requirements from this job description.

RULES:
- Only extract EXPLICITLY mentioned requirements
- Return valid JSON format

Job Description:
{job_description}

Return JSON:
{{
    "required_skills": ["skill1"],
    "required_tools": ["tool1"],
    "nice_to_have": ["skill1"],
    "experience_years_required": 0,
    "education_required": "Master's",
    "certifications_required": ["cert1"]
}}"""

job_requirement_prompt = PromptTemplate(
    input_variables=["job_description"],
    template=job_requirement_template
)

job_requirement_chain = (
    job_requirement_prompt 
    | llm 
    | json_parser
)

# Matching Prompt
matching_template = """You are an expert HR recruiter. Compare candidate skills with job requirements.

RULES:
- Only count EXACT matches
- Do NOT assume transferable skills
- Return valid JSON format

Candidate Skills (JSON):
{candidate_skills}

Job Requirements (JSON):
{job_requirements}

Return JSON:
{{
    "matched_required": ["skill1"],
    "missing_required": ["skill1"],
    "matched_nice_to_have": ["skill1"],
    "additional_strengths": [],
    "critical_gaps": ["gap1"]
}}"""

matching_prompt = PromptTemplate(
    input_variables=["candidate_skills", "job_requirements"],
    template=matching_template
)

matching_chain = (
    matching_prompt 
    | llm 
    | json_parser
)

# Scoring Prompt
scoring_template = """You are an expert HR recruiter. Score this candidate (0-100).

Scoring Criteria:
- 90-100: Exceeds all requirements
- 80-89: Meets all requirements
- 70-79: Meets most requirements
- 60-69: Meets some requirements
- 0-59: Does not meet core requirements

Matching Analysis:
{matching_analysis}

Return JSON:
{{
    "fit_score": 0,
    "score_justification": "explanation"
}}"""

scoring_prompt = PromptTemplate(
    input_variables=["matching_analysis"],
    template=scoring_template
)

scoring_chain = (
    scoring_prompt 
    | llm 
    | json_parser
)

# Explanation Prompt
explanation_template = """You are an expert HR recruiter. Explain this candidate's evaluation.

Candidate Skills (JSON):
{candidate_skills}

Matching Analysis (JSON):
{matching_analysis}

Fit Score: {fit_score}/100

Return JSON:
{{
    "summary": "brief summary",
    "strengths": "key strengths",
    "weaknesses": "main gaps",
    "recommendation": "STRONG PASS/PASS/CONSIDER/REJECT",
    "next_steps": "action"
}}"""

explanation_prompt = PromptTemplate(
    input_variables=["candidate_skills", "matching_analysis", "fit_score"],
    template=explanation_template
)

explanation_chain = (
    explanation_prompt 
    | llm 
    | json_parser
)

print("✓ LangChain prompts and chains created\n")

# =========================================================================
# STEP 3: PROCESS JOB DESCRIPTION
# =========================================================================

print("="*80)
print("PROCESSING JOB DESCRIPTION")
print("="*80)

job_requirements = job_requirement_chain.invoke(
    {"job_description": JOB_DESCRIPTION}
)

print(f"✓ Job requirements extracted")
print(f"  Required skills: {len(job_requirements.get('required_skills', []))} skills")
print(f"  Experience required: {job_requirements.get('experience_years_required', 0)}+ years\n")

# =========================================================================
# STEP 4: SCREEN ALL CANDIDATES
# =========================================================================

candidates = [
    {"name": "John Doe", "type": "STRONG", "resume": STRONG_CANDIDATE_RESUME},
    {"name": "Alice Smith", "type": "AVERAGE", "resume": AVERAGE_CANDIDATE_RESUME},
    {"name": "Bob Johnson", "type": "WEAK", "resume": WEAK_CANDIDATE_RESUME},
]

results = []

for idx, candidate in enumerate(candidates, 1):
    print("="*80)
    print(f"RUN {idx}: {candidate['type']} CANDIDATE - {candidate['name']}")
    print("="*80)
    
    result = {"candidate_name": candidate["name"], "candidate_type": candidate["type"]}
    
    try:
        # Step 1: Extract Skills
        print(f"[STEP 1/4] Extracting Skills...")
        candidate_skills = skill_extraction_chain.invoke({"resume": candidate["resume"]})
        result["skills_extracted"] = candidate_skills
        print(f"✓ Extracted: {len(candidate_skills.get('technical_skills', []))} technical skills")
        
        # Step 2: Match Skills
        print(f"[STEP 2/4] Matching with Job Requirements...")
        matching_analysis = matching_chain.invoke({
            "candidate_skills": json.dumps(candidate_skills),
            "job_requirements": json.dumps(job_requirements)
        })
        result["matching_analysis"] = matching_analysis
        matched = len(matching_analysis.get('matched_required', []))
        missing = len(matching_analysis.get('missing_required', []))
        print(f"✓ Matched: {matched}/{matched+missing} required skills")
        
        # Step 3: Calculate Score
        print(f"[STEP 3/4] Calculating Fit Score...")
        scoring_result = scoring_chain.invoke({
            "matching_analysis": json.dumps(matching_analysis)
        })
        result["scoring"] = scoring_result
        fit_score = scoring_result.get("fit_score", 0)
        print(f"✓ FIT SCORE: {fit_score}/100")
        
        # Step 4: Generate Explanation
        print(f"[STEP 4/4] Generating Explanation...")
        explanation_result = explanation_chain.invoke({
            "candidate_skills": json.dumps(candidate_skills),
            "matching_analysis": json.dumps(matching_analysis),
            "fit_score": fit_score
        })
        result["explanation"] = explanation_result
        print(f"✓ Recommendation: {explanation_result.get('recommendation', 'N/A')}\n")
        
        results.append(result)
        
    except Exception as e:
        print(f"✗ Error: {str(e)}\n")
        result["error"] = str(e)
        results.append(result)

# =========================================================================
# STEP 5: DISPLAY RESULTS
# =========================================================================

print("="*80)
print("FINAL RESULTS SUMMARY")
print("="*80 + "\n")

print(f"{'Candidate':<20} {'Type':<10} {'Score':<10} {'Recommendation':<15}")
print("-"*80)

for result in results:
    score = result.get('scoring', {}).get('fit_score', 'N/A')
    recommendation = result.get('explanation', {}).get('recommendation', 'N/A')
    print(f"{result['candidate_name']:<20} {result['candidate_type']:<10} {score:<10} {recommendation:<15}")

print("\n" + "="*80)

# =========================================================================
# STEP 6: SAVE RESULTS
# =========================================================================

# Save to JSON
output_file = "screening_results.json"
with open(output_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"✓ Results saved to: {output_file}\n")

# =========================================================================
# COMPLETION
# =========================================================================

print("="*80)
print("✅ RESUME SCREENING COMPLETE")
print("="*80)
print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nNext Steps:")
print("1. Check LangSmith traces at: https://smith.langchain.com")
print("2. Look for project: 'Resume_Screening_System'")
print("3. You should see 3 runs with all pipeline steps")
print("4. Push to GitHub and create LinkedIn post")
print("5. Submit Google Form before April 16, 2026\n")
