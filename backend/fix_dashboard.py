#!/usr/bin/env python3
"""
Script to add job_match_analysis back to the improved prompt
"""

def update_prompt_with_match_analysis():
    file_path = 'routes/cover_letter.py'
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the company_research section and add job_match_analysis after it
    old_section = '''    "company_research": {
        "company_name": "Company Name",
        "products_mentioned": ["product1", "product2"],
        "why_compelling": "Brief note on what makes this company interesting"
    }
}'''
    
    new_section = '''    "company_research": {
        "company_name": "Company Name",
        "products_mentioned": ["product1", "product2"],
        "why_compelling": "Brief note on what makes this company interesting"
    },
    "job_match_analysis": {
        "match_score": 85,
        "matching_skills": ["skill1", "skill2", "skill3"],
        "skills_emphasized": ["skill1", "skill2", "skill3"],
        "potential_gaps": ["gap1"]
    }
}'''
    
    if old_section in content:
        content = content.replace(old_section, new_section)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print("✅ Successfully added job_match_analysis to prompt!")
        return True
    else:
        print("❌ Could not find section to replace")
        return False

if __name__ == '__main__':
    update_prompt_with_match_analysis()
