"""
AI Roles and Global Hiring Data Module
This module contains the core data structures for AI roles and global hiring patterns.
Separated to avoid circular imports and centralize data definitions.
"""

# 21 AI Roles Database with Global Salary Data
AI_ROLES = [
    {
        "id": "ml_engineer",
        "name": "Machine Learning Engineer",
        "description": "Build and deploy ML models, create training pipelines, optimize model performance, work with traditional ML algorithms and deep learning",
        "salary": {
            "us": "$140K - $230K",
            "india": "₹25-65 LPA ($30K-$75K)",
            "europe": "€75K - €170K",
            "brazil": "R$110K - R$280K",
            "se_asia": "$35K - $95K"
        },
        "salary_range": "$140K - $230K",
        "top_skills": ["Python", "PyTorch/TensorFlow", "Scikit-learn", "MLOps", "Feature Engineering", "Model Optimization", "Statistical Learning"],
        "companies": ["Google", "Meta", "Netflix", "Spotify", "Airbnb", "Uber", "LinkedIn"],
        "transition_weeks": 14,
        "from_background": {
            "software_engineer": {"fit": "EXCELLENT", "weeks": 10},
            "data_engineer": {"fit": "EXCELLENT", "weeks": 12},
            "data_scientist": {"fit": "EXCELLENT", "weeks": 6},
            "product_manager": {"fit": "CHALLENGING", "weeks": 32}
        },
        "courses": ["Andrew Ng ML Specialization", "Fast.ai Practical Deep Learning", "Stanford CS229", "Hands-On ML with Scikit-Learn"],
        "focus_areas": ["Classical ML algorithms", "Neural networks", "Model training & evaluation", "Feature engineering", "ML system design"]
    },
    {
        "id": "ai_engineer",
        "name": "AI Engineer",
        "description": "Build AI-powered applications using LLMs, integrate AI APIs, develop RAG systems, create AI agents and automation workflows",
        "salary": {
            "us": "$150K - $260K",
            "india": "₹28-75 LPA ($35K-$90K)",
            "europe": "€80K - €190K",
            "brazil": "R$120K - R$320K",
            "se_asia": "$40K - $110K"
        },
        "salary_range": "$150K - $260K",
        "top_skills": ["LLM APIs (OpenAI, Anthropic)", "LangChain/LlamaIndex", "RAG Systems", "Vector Databases", "Prompt Engineering", "AI Agents", "Full-Stack Development"],
        "companies": ["OpenAI", "Anthropic", "Cohere", "Replit", "Vercel", "AI Startups", "Tech Companies"],
        "transition_weeks": 10,
        "from_background": {
            "software_engineer": {"fit": "EXCELLENT", "weeks": 8},
            "full_stack_developer": {"fit": "EXCELLENT", "weeks": 8},
            "data_engineer": {"fit": "GOOD", "weeks": 12},
            "product_manager": {"fit": "GOOD", "weeks": 20}
        },
        "courses": ["Deeplearning.AI LLM Courses", "LangChain Documentation", "OpenAI Cookbook", "Building AI Applications"],
        "focus_areas": ["LLM integration", "RAG architectures", "AI agents", "Prompt optimization", "Production AI systems"]
    },
    {
        "id": "prompt_engineer",
        "name": "Prompt Engineer",
        "description": "LLM applications, RAG systems, prompt optimization",
        "salary": {
            "us": "$100K - $180K",
            "india": "₹20-50 LPA ($25K-$60K)",
            "europe": "€60K - €150K",
            "brazil": "R$100K - R$250K",
            "se_asia": "$30K - $80K"
        },
        "salary_range": "$100K - $180K",
        "top_skills": ["LLM APIs", "Prompt Design", "RAG", "API Integration", "Creativity"],
        "companies": ["OpenAI", "Anthropic", "Cohere", "Scale AI", "Replit"],
        "transition_weeks": 8,
        "from_background": {
            "product_manager": {"fit": "EXCELLENT", "weeks": 8},
            "content_writer": {"fit": "EXCELLENT", "weeks": 8},
            "software_engineer": {"fit": "EXCELLENT", "weeks": 6}
        },
        "courses": ["Deeplearning.AI Short Courses", "OpenAI Cookbook", "LangChain Tutorials"]
    },
    {
        "id": "ai_product_manager",
        "name": "AI Product Manager",
        "description": "AI product strategy, market fit, stakeholder management",
        "salary": {
            "us": "$160K - $280K",
            "india": "₹30-85 LPA ($35K-$100K)",
            "europe": "€90K - €200K",
            "brazil": "R$130K - R$350K",
            "se_asia": "$50K - $120K"
        },
        "salary_range": "$160K - $280K",
        "top_skills": ["Product Strategy", "AI/ML Understanding", "Business Acumen", "Stakeholder Management"],
        "companies": ["Google", "Microsoft", "Anthropic", "OpenAI", "Amazon"],
        "transition_weeks": 10,
        "from_background": {
            "product_manager": {"fit": "EXCELLENT", "weeks": 8},
            "software_engineer": {"fit": "GOOD", "weeks": 16}
        },
        "courses": ["Reforge AI/ML for PMs", "Y Combinator Startup School", "AI Product Management"]
    },
    {
        "id": "data_scientist",
        "name": "Data Scientist",
        "description": "ML pipelines, statistical modeling, data analysis",
        "salary": {
            "us": "$120K - $200K",
            "india": "₹20-60 LPA ($25K-$70K)",
            "europe": "€70K - €160K",
            "brazil": "R$100K - R$280K",
            "se_asia": "$35K - $90K"
        },
        "salary_range": "$120K - $200K",
        "top_skills": ["Python", "Statistics", "SQL", "ML Algorithms", "Data Visualization"],
        "companies": ["Google", "Netflix", "Airbnb", "Spotify", "Amazon"],
        "transition_weeks": 14,
        "from_background": {
            "data_analyst": {"fit": "EXCELLENT", "weeks": 12},
            "software_engineer": {"fit": "GOOD", "weeks": 16}
        },
        "courses": ["Andrew Ng ML Specialization", "Fast.ai", "Kaggle Competitions"]
    },
    {
        "id": "mlops_engineer",
        "name": "ML Operations Engineer",
        "description": "MLOps, model monitoring, deployment pipelines",
        "salary": {
            "us": "$140K - $220K",
            "india": "₹25-70 LPA ($30K-$80K)",
            "europe": "€75K - €170K",
            "brazil": "R$110K - R$300K",
            "se_asia": "$40K - $100K"
        },
        "salary_range": "$140K - $220K",
        "top_skills": ["Python", "Docker", "Kubernetes", "CI/CD", "Cloud Platforms"],
        "companies": ["Google Cloud", "AWS", "Azure", "Databricks", "DVC"],
        "transition_weeks": 8,
        "from_background": {
            "devops_engineer": {"fit": "EXCELLENT", "weeks": 6},
            "software_engineer": {"fit": "GOOD", "weeks": 12}
        },
        "courses": ["Deeplearning.AI MLOps", "Kubernetes for ML", "AWS ML Specialty"]
    },
    {
        "id": "ai_safety_researcher",
        "name": "AI Safety Researcher",
        "description": "AI alignment, safety research, responsible AI",
        "salary": {
            "us": "$150K - $250K",
            "india": "₹35-85 LPA ($40K-$100K)",
            "europe": "€80K - €180K",
            "brazil": "R$130K - R$350K",
            "se_asia": "$50K - $120K"
        },
        "salary_range": "$150K - $250K",
        "top_skills": ["Research Methodology", "Mathematics", "Deep Learning Theory", "Policy"],
        "companies": ["Anthropic", "OpenAI Safety", "DeepMind", "Center for AI Safety"],
        "transition_weeks": 28,
        "from_background": {
            "ml_engineer": {"fit": "GOOD", "weeks": 28},
            "academic_researcher": {"fit": "GOOD", "weeks": 20}
        },
        "courses": ["Alignment Research Course", "AI Safety Fundamentals", "Academic Papers"]
    },
    {
        "id": "ai_solutions_architect",
        "name": "AI Solutions Architect",
        "description": "Enterprise AI solutions, implementation, architecture",
        "salary": {
            "us": "$170K - $280K",
            "india": "₹35-100 LPA ($40K-$120K)",
            "europe": "€95K - €210K",
            "brazil": "R$140K - R$380K",
            "se_asia": "$55K - $140K"
        },
        "salary_range": "$170K - $280K",
        "top_skills": ["Enterprise Systems", "AI Integration", "Cloud Platforms", "Communication"],
        "companies": ["Microsoft", "Google Cloud", "AWS", "IBM", "Salesforce"],
        "transition_weeks": 12,
        "from_background": {
            "solutions_architect": {"fit": "EXCELLENT", "weeks": 10},
            "product_manager": {"fit": "GOOD", "weeks": 16}
        },
        "courses": ["Google Cloud AI Architect", "AWS ML Solutions Architect", "Azure AI"]
    },
    {
        "id": "generative_ai_developer",
        "name": "Generative AI Developer",
        "description": "RAG, LLM applications, automation with AI",
        "salary": {
            "us": "$130K - $220K",
            "india": "₹25-70 LPA ($30K-$80K)",
            "europe": "€75K - €170K",
            "brazil": "R$110K - R$300K",
            "se_asia": "$40K - $100K"
        },
        "salary_range": "$130K - $220K",
        "top_skills": ["LLMs", "RAG", "Prompt Engineering", "Full-Stack Dev", "API Integration"],
        "companies": ["Anthropic", "OpenAI", "Replit", "Hugging Face", "Google"],
        "transition_weeks": 10,
        "from_background": {
            "full_stack_developer": {"fit": "EXCELLENT", "weeks": 10},
            "ml_engineer": {"fit": "GOOD", "weeks": 12}
        },
        "courses": ["LangChain Tutorials", "Deeplearning.AI", "LlamaIndex", "RAG Fundamentals"]
    },
    {
        "id": "ai_research_scientist",
        "name": "AI Research Scientist",
        "description": "Cutting-edge AI research, publications, novel algorithms",
        "salary": {
            "us": "$160K - $300K",
            "india": "₹50-120 LPA ($50K-$120K)",
            "europe": "€90K - €220K",
            "brazil": "R$150K - R$400K",
            "se_asia": "$60K - $150K"
        },
        "salary_range": "$160K - $300K",
        "top_skills": ["Research Methodology", "Advanced Mathematics", "Deep Learning", "Publications"],
        "companies": ["DeepMind", "OpenAI", "Meta FAIR", "Google Research", "Academic Labs"],
        "transition_weeks": 40,
        "from_background": {
            "academic_phd": {"fit": "GOOD", "weeks": 24},
            "ml_engineer": {"fit": "GOOD", "weeks": 40}
        },
        "courses": ["University-level AI Courses", "Research Guidance", "PhD Programs"]
    },
    {
        "id": "cv_engineer",
        "name": "Computer Vision Engineer",
        "description": "Image processing, object detection, CV models",
        "salary": {
            "us": "$140K - $240K",
            "india": "₹35-90 LPA ($35K-$90K)",
            "europe": "€80K - €180K",
            "brazil": "R$120K - R$320K",
            "se_asia": "$45K - $110K"
        },
        "salary_range": "$140K - $240K",
        "top_skills": ["CNN", "Image Processing", "OpenCV", "PyTorch", "Computer Vision Theory"],
        "companies": ["Tesla Autopilot", "Google", "Meta", "Apple", "Robotics Companies"],
        "transition_weeks": 20,
        "from_background": {
            "ml_engineer": {"fit": "GOOD", "weeks": 16},
            "software_engineer": {"fit": "CHALLENGING", "weeks": 28}
        },
        "courses": ["Stanford CV Course", "Fast.ai Part 2", "PyTorch CV"]
    },
    {
        "id": "nlp_engineer",
        "name": "NLP Engineer",
        "description": "Text processing, language models, NLU systems",
        "salary": {
            "us": "$140K - $240K",
            "india": "₹35-90 LPA ($35K-$90K)",
            "europe": "€80K - €180K",
            "brazil": "R$120K - R$320K",
            "se_asia": "$45K - $110K"
        },
        "salary_range": "$140K - $240K",
        "top_skills": ["Transformers", "BERT/GPT", "NLP Theory", "Text Processing", "Linguistics"],
        "companies": ["Google", "OpenAI", "Anthropic", "Meta", "HuggingFace"],
        "transition_weeks": 20,
        "from_background": {
            "ml_engineer": {"fit": "GOOD", "weeks": 16},
            "linguist": {"fit": "CHALLENGING", "weeks": 24}
        },
        "courses": ["Stanford NLP", "HuggingFace Course", "Fast.ai NLP"]
    },
    {
        "id": "rl_engineer",
        "name": "Reinforcement Learning Engineer",
        "description": "RL algorithms, game AI, robotics applications",
        "salary": {
            "us": "$150K - $260K",
            "india": "₹40-100 LPA ($40K-$100K)",
            "europe": "€85K - €190K",
            "brazil": "R$130K - R$350K",
            "se_asia": "$50K - $120K"
        },
        "salary_range": "$150K - $260K",
        "top_skills": ["RL Algorithms", "Markov Processes", "Policy Optimization", "Game AI"],
        "companies": ["DeepMind", "Tesla Robotics", "OpenAI", "Game Companies"],
        "transition_weeks": 32,
        "from_background": {
            "ml_engineer": {"fit": "GOOD", "weeks": 28},
            "game_developer": {"fit": "CHALLENGING", "weeks": 40}
        },
        "courses": ["David Silver RL Course", "Spinning Up in DRL", "Sutton & Barto Book"]
    },
    {
        "id": "ml_infra_engineer",
        "name": "AI/ML Infrastructure Engineer",
        "description": "Scalable ML systems, cloud ML, distributed training",
        "salary": {
            "us": "$160K - $260K",
            "india": "₹40-110 LPA ($40K-$110K)",
            "europe": "€90K - €200K",
            "brazil": "R$140K - R$380K",
            "se_asia": "$50K - $130K"
        },
        "salary_range": "$160K - $260K",
        "top_skills": ["Distributed Systems", "Kubernetes", "Cloud ML", "Data Pipelines", "Scalability"],
        "companies": ["Google Cloud", "AWS", "Meta", "Databricks"],
        "transition_weeks": 16,
        "from_background": {
            "backend_engineer": {"fit": "EXCELLENT", "weeks": 14},
            "devops_engineer": {"fit": "EXCELLENT", "weeks": 14}
        },
        "courses": ["Deeplearning.AI MLOps", "Kubernetes", "Cloud Platform Certifications"]
    },
    {
        "id": "ai_product_designer",
        "name": "AI Product Designer",
        "description": "AI-first UX, designing with ML, human-AI interaction",
        "salary": {
            "us": "$120K - $200K",
            "india": "₹30-80 LPA ($30K-$80K)",
            "europe": "€70K - €160K",
            "brazil": "R$100K - R$280K",
            "se_asia": "$35K - $90K"
        },
        "salary_range": "$120K - $200K",
        "top_skills": ["AI UX Patterns", "User Research", "Design Thinking", "Prototyping"],
        "companies": ["Google", "Apple", "Microsoft", "Figma", "Design Startups"],
        "transition_weeks": 16,
        "from_background": {
            "product_designer": {"fit": "EXCELLENT", "weeks": 14},
            "product_manager": {"fit": "GOOD", "weeks": 20}
        },
        "courses": ["AI UX Design Courses", "Product Design Fundamentals", "Human-AI Interaction"]
    },
    {
        "id": "ai_consultant",
        "name": "AI Consultant",
        "description": "Helping enterprises adopt AI, strategy consulting",
        "salary": {
            "us": "$150K - $300K",
            "india": "₹50-150 LPA ($50K-$150K)",
            "europe": "€90K - €220K",
            "brazil": "R$150K - R$450K",
            "se_asia": "$60K - $180K"
        },
        "salary_range": "$150K - $300K",
        "top_skills": ["Business Strategy", "AI Strategy", "Client Communication", "Industry Knowledge"],
        "companies": ["McKinsey", "Bain", "BCG", "Tech Consultants", "Boutique AI Firms"],
        "transition_weeks": 14,
        "from_background": {
            "management_consultant": {"fit": "EXCELLENT", "weeks": 12},
            "product_manager": {"fit": "GOOD", "weeks": 16}
        },
        "courses": ["Business Strategy + AI Fundamentals", "Consulting Frameworks", "AI Case Studies"]
    },
    {
        "id": "ai_ethics_specialist",
        "name": "AI Ethics Specialist",
        "description": "Responsible AI, bias detection, governance",
        "salary": {
            "us": "$130K - $220K",
            "india": "₹35-90 LPA ($35K-$90K)",
            "europe": "€75K - €170K",
            "brazil": "R$110K - R$300K",
            "se_asia": "$40K - $100K"
        },
        "salary_range": "$130K - $220K",
        "top_skills": ["AI Ethics", "Bias Detection", "Policy", "Responsible AI", "Fairness"],
        "companies": ["Google", "OpenAI", "Regulatory Bodies", "Ethics-Focused Orgs"],
        "transition_weeks": 20,
        "from_background": {
            "policy_analyst": {"fit": "GOOD", "weeks": 18},
            "philosopher": {"fit": "CHALLENGING", "weeks": 24}
        },
        "courses": ["AI Ethics Courses", "Policy Fundamentals", "Fairness in ML"]
    },
    {
        "id": "vibe_coder",
        "name": "Vibe Coder / AI Automation Builder",
        "description": "Using Cursor, Emergent, no-code AI tools for rapid development - FASTEST PATH TO AI",
        "salary": {
            "us": "$80K - $150K",
            "india": "₹15-50 LPA ($20K-$50K)",
            "europe": "€60K - €140K",
            "brazil": "R$80K - R$250K",
            "se_asia": "$25K - $70K"
        },
        "salary_range": "$80K - $150K",
        "top_skills": ["Cursor.sh", "Emergent.sh", "Make.com", "No-Code AI", "Rapid Prototyping"],
        "companies": ["Indie Hackers", "Startups", "Automation Agencies", "Emerging Tech"],
        "transition_weeks": 3,
        "from_background": {
            "any_tech": {"fit": "EXCELLENT", "weeks": 3},
            "no_code": {"fit": "EXCELLENT", "weeks": 2}
        },
        "courses": ["Cursor Tutorials", "Emergent.sh Docs", "Make.com", "YouTube Builders"],
        "fastest_path": True
    },
    {
        "id": "ai_content_creator",
        "name": "AI Content Creator",
        "description": "AI-generated content, prompt mastery for content",
        "salary": {
            "us": "$40K - $150K (highly variable)",
            "india": "₹10-60 LPA ($15K-$60K)",
            "europe": "€40K - €140K",
            "brazil": "R$50K - R$250K",
            "se_asia": "$15K - $60K"
        },
        "salary_range": "$40K - $150K",
        "top_skills": ["Prompt Engineering", "Content Strategy", "LLM Mastery", "Personal Brand"],
        "companies": ["YouTube", "TikTok", "Substack", "Twitter", "Personal Brands"],
        "transition_weeks": 6,
        "from_background": {
            "content_writer": {"fit": "EXCELLENT", "weeks": 5},
            "content_creator": {"fit": "EXCELLENT", "weeks": 3}
        },
        "courses": ["ChatGPT Mastery", "Midjourney", "Content Strategy", "AI Tools Tutorials"]
    },
    {
        "id": "agent_developer",
        "name": "Autonomous Agent Developer",
        "description": "Building AI agents, multi-agent systems, agentic workflows",
        "salary": {
            "us": "$140K - $250K",
            "india": "₹35-90 LPA ($35K-$90K)",
            "europe": "€80K - €190K",
            "brazil": "R$120K - R$330K",
            "se_asia": "$45K - $110K"
        },
        "salary_range": "$140K - $250K",
        "top_skills": ["Multi-Agent Systems", "Orchestration", "LLMs", "Autonomous Reasoning"],
        "companies": ["Anthropic", "OpenAI", "Replit", "AI Agent Startups"],
        "transition_weeks": 18,
        "from_background": {
            "full_stack_developer": {"fit": "GOOD", "weeks": 16},
            "ml_engineer": {"fit": "GOOD", "weeks": 18}
        },
        "courses": ["AutoGPT", "LangChain Advanced", "Agent Patterns", "CrewAI"]
    },
    {
        "id": "ai_business_analyst",
        "name": "AI Business Analyst",
        "description": "AI ROI, analytics, business intelligence with AI",
        "salary": {
            "us": "$100K - $180K",
            "india": "₹25-70 LPA ($25K-$70K)",
            "europe": "€70K - €160K",
            "brazil": "R$90K - R$280K",
            "se_asia": "$30K - $80K"
        },
        "salary_range": "$100K - $180K",
        "top_skills": ["AI Metrics", "Business Analysis", "ROI Calculation", "Data Storytelling"],
        "companies": ["Google Analytics", "Mixpanel", "Data Analytics", "Business Intelligence"],
        "transition_weeks": 10,
        "from_background": {
            "business_analyst": {"fit": "EXCELLENT", "weeks": 10},
            "data_analyst": {"fit": "EXCELLENT", "weeks": 12}
        },
        "courses": ["Analytics Fundamentals", "AI Concepts", "Business Intelligence"]
    }
]

# Global Hiring Patterns by Region
GLOBAL_HIRING = {
    "india": {
        "companies": ["Flipkart", "Amazon India", "Google India", "Microsoft India", "TCS", "Infosys", "AI Startups"],
        "preference": "GitHub portfolio, competitive coding, startup hustle",
        "vibe_coder_opportunity": "HIGHEST"
    },
    "us": {
        "companies": ["OpenAI", "Google", "Meta", "DeepMind", "Tesla", "Anthropic", "Y Combinator"],
        "preference": "Publications, open-source, unique projects",
        "vibe_coder_opportunity": "VERY HIGH"
    },
    "europe": {
        "companies": ["Google Switzerland", "DeepMind London", "HuggingFace", "CERN"],
        "preference": "Academic background, publications, structured education",
        "vibe_coder_opportunity": "HIGH"
    },
    "brazil": {
        "companies": ["Nubank", "Mercado Libre", "Local AI Startups", "Fintech"],
        "preference": "Bilingual (Portuguese + English), practical skills",
        "vibe_coder_opportunity": "HIGH"
    },
    "se_asia": {
        "companies": ["Grab", "Gojek", "ByteDance", "Local Startups"],
        "preference": "Practical skills, immediate contribution, rapid growth",
        "vibe_coder_opportunity": "HIGHEST"
    }
}


def get_role_by_id(role_id: str):
    """Get a role by its ID"""
    return next((r for r in AI_ROLES if r["id"] == role_id), None)


def get_all_role_ids():
    """Get list of all role IDs"""
    return [r["id"] for r in AI_ROLES]
