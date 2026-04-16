"""
Main Resume Screening Pipeline Orchestrator
"""

import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from prompts.skill_extraction_prompt import skill_extraction_prompt
from prompts.job_requirement_prompt import job_requirement_prompt
from prompts.matching_prompt import matching_prompt
from prompts.scoring_prompt import scoring_prompt
from prompts.explanation_prompt import explanation_prompt

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# JSON Parser
json_parser = JsonOutputParser()

# Build Chains using LCEL
skill_extraction_chain = skill_extraction_prompt | llm | json_parser
job_requirement_chain = job_requirement_prompt | llm | json_parser
matching_chain = matching_prompt | llm | json_parser
scoring_chain = scoring_prompt | llm | json_parser
explanation_chain = explanation_prompt | llm | json_parser


class ResumeScreeningPipeline:
    """
    Complete Resume Screening Pipeline with LangChain
    """
    
    def __init__(self):
        self.job_requirements = None
        self.results = []
    
    def process_job_description(self, job_description):
        """
        Step 0: Extract job requirements
        """
        print("\n" + "="*80)
        print("STEP 0: EXTRACTING JOB REQUIREMENTS")
        print("="*80)
        
        self.job_requirements = job_requirement_chain.invoke(
            {"job_description": job_description}
        )
        
        print("✓ Job Requirements Extracted Successfully")
        print(json.dumps(self.job_requirements, indent=2))
        
        return self.job_requirements
    
    def screen_resume(self, resume, candidate_name):
        """
        Complete screening pipeline for a single resume
        """
        print("\n" + "="*80)
        print(f"SCREENING CANDIDATE: {candidate_name.upper()}")
        print("="*80)
        
        result = {"candidate_name": candidate_name}
        
        # Step 1: Extract Skills
        print("\n[STEP 1] Extracting Candidate Skills...")
        candidate_skills = skill_extraction_chain.invoke({"resume": resume})
        result["skills_extracted"] = candidate_skills
        print("✓ Skills Extracted")
        print(json.dumps(candidate_skills, indent=2))
        
        # Step 2: Match Skills with Job Requirements
        print("\n[STEP 2] Matching Skills with Job Requirements...")
        matching_analysis = matching_chain.invoke({
            "candidate_skills": json.dumps(candidate_skills),
            "job_requirements": json.dumps(self.job_requirements)
        })
        result["matching_analysis"] = matching_analysis
        print("✓ Matching Analysis Complete")
        print(json.dumps(matching_analysis, indent=2))
        
        # Step 3: Calculate Score
        print("\n[STEP 3] Calculating Fit Score...")
        scoring_result = scoring_chain.invoke({
            "matching_analysis": json.dumps(matching_analysis),
            "job_requirements": json.dumps(self.job_requirements)
        })
        result["scoring"] = scoring_result
        fit_score = scoring_result.get("fit_score", 0)
        print("✓ Score Calculated")
        print(f"FIT SCORE: {fit_score}/100")
        print(f"Justification: {scoring_result.get('score_justification', 'N/A')}")
        
        # Step 4: Generate Explanation
        print("\n[STEP 4] Generating Explanation & Recommendation...")
        explanation_result = explanation_chain.invoke({
            "candidate_skills": json.dumps(candidate_skills),
            "matching_analysis": json.dumps(matching_analysis),
            "fit_score": fit_score,
            "job_requirements": json.dumps(self.job_requirements)
        })
        result["explanation"] = explanation_result
        print("✓ Explanation Generated")
        print(json.dumps(explanation_result, indent=2))
        
        # Final Summary
        print("\n" + "-"*80)
        print("FINAL EVALUATION SUMMARY")
        print("-"*80)
        print(f"Candidate: {candidate_name}")
        print(f"Fit Score: {fit_score}/100")
        print(f"Recommendation: {explanation_result.get('recommendation', 'N/A')}")
        print(f"Summary: {explanation_result.get('summary', 'N/A')}")
        print("-"*80)
        
        self.results.append(result)
        return result
    
    def export_results(self, output_file="screening_results.json"):
        """
        Export all screening results to JSON file
        """
        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✓ Results exported to {output_file}")
        return output_file


def main():
    """
    Main execution function
    """
    print("\n" + "="*80)
    print("AI RESUME SCREENING SYSTEM WITH LANGSMITH TRACING")
    print("="*80)
    
    pipeline = ResumeScreeningPipeline()
    
    return pipeline


if __name__ == "__main__":
    main()
