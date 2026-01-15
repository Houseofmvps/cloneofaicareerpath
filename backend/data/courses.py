"""
Course Database Module
Contains comprehensive course data for AI/ML learning paths.
"""

# Comprehensive Course Database with real links and metadata
COURSE_DATABASE = {
    # Python Fundamentals
    "python_everybody": {
        "name": "Python for Everybody Specialization",
        "platform": "Coursera",
        "url": "https://www.coursera.org/specializations/python",
        "duration_hours": 80,
        "cost": "Free (Audit) / $49/month",
        "difficulty": "Beginner",
        "rating": 4.8,
        "skills": ["Python", "Data Structures", "Web Scraping"],
        "for_roles": ["all"]
    },
    "python_bootcamp": {
        "name": "Complete Python Bootcamp",
        "platform": "Udemy",
        "url": "https://www.udemy.com/course/complete-python-bootcamp/",
        "duration_hours": 22,
        "cost": "$15-20",
        "difficulty": "Beginner",
        "rating": 4.6,
        "skills": ["Python", "OOP", "Projects"],
        "for_roles": ["all"]
    },
    "cs50_python": {
        "name": "CS50's Introduction to Programming with Python",
        "platform": "Harvard/edX",
        "url": "https://cs50.harvard.edu/python/",
        "duration_hours": 40,
        "cost": "Free",
        "difficulty": "Beginner",
        "rating": 4.9,
        "skills": ["Python", "Problem Solving", "Testing"],
        "for_roles": ["all"]
    },
    
    # Machine Learning
    "andrew_ng_ml": {
        "name": "Machine Learning Specialization",
        "platform": "Coursera (DeepLearning.AI)",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "duration_hours": 100,
        "cost": "$49/month",
        "difficulty": "Intermediate",
        "rating": 4.9,
        "skills": ["Machine Learning", "Supervised Learning", "Neural Networks"],
        "for_roles": ["ml_engineer", "data_scientist", "ai_researcher"]
    },
    "fastai_ml": {
        "name": "Practical Deep Learning for Coders",
        "platform": "Fast.ai",
        "url": "https://course.fast.ai/",
        "duration_hours": 50,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.9,
        "skills": ["Deep Learning", "PyTorch", "Computer Vision", "NLP"],
        "for_roles": ["ml_engineer", "ai_researcher", "cv_engineer", "nlp_engineer"]
    },
    "stanford_cs229": {
        "name": "CS229: Machine Learning",
        "platform": "Stanford Online",
        "url": "https://cs229.stanford.edu/",
        "duration_hours": 60,
        "cost": "Free",
        "difficulty": "Advanced",
        "rating": 4.8,
        "skills": ["ML Theory", "Statistics", "Optimization"],
        "for_roles": ["ai_researcher", "ml_engineer"]
    },
    
    # Deep Learning
    "deeplearning_ai_dl": {
        "name": "Deep Learning Specialization",
        "platform": "Coursera (DeepLearning.AI)",
        "url": "https://www.coursera.org/specializations/deep-learning",
        "duration_hours": 120,
        "cost": "$49/month",
        "difficulty": "Intermediate",
        "rating": 4.9,
        "skills": ["Neural Networks", "CNN", "RNN", "Transformers"],
        "for_roles": ["ml_engineer", "ai_researcher", "cv_engineer"]
    },
    "pytorch_udacity": {
        "name": "Intro to Deep Learning with PyTorch",
        "platform": "Udacity",
        "url": "https://www.udacity.com/course/deep-learning-pytorch--ud188",
        "duration_hours": 40,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["PyTorch", "Neural Networks", "CNN"],
        "for_roles": ["ml_engineer", "ai_researcher"]
    },
    "fastai_part2": {
        "name": "Deep Learning from the Foundations",
        "platform": "Fast.ai",
        "url": "https://course.fast.ai/Lessons/part2.html",
        "duration_hours": 40,
        "cost": "Free",
        "difficulty": "Advanced",
        "rating": 4.9,
        "skills": ["Deep Learning", "From Scratch Implementation"],
        "for_roles": ["ai_researcher", "ml_engineer"]
    },
    
    # LLMs & Generative AI
    "deeplearning_llm": {
        "name": "Generative AI with Large Language Models",
        "platform": "Coursera (DeepLearning.AI)",
        "url": "https://www.coursera.org/learn/generative-ai-with-llms",
        "duration_hours": 20,
        "cost": "$49/month",
        "difficulty": "Intermediate",
        "rating": 4.8,
        "skills": ["LLMs", "Fine-tuning", "RLHF", "Prompt Engineering"],
        "for_roles": ["genai_developer", "prompt_engineer", "ml_engineer"]
    },
    "langchain_course": {
        "name": "LangChain for LLM Application Development",
        "platform": "DeepLearning.AI",
        "url": "https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/",
        "duration_hours": 4,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["LangChain", "RAG", "LLM Applications"],
        "for_roles": ["genai_developer", "prompt_engineer"]
    },
    "huggingface_nlp": {
        "name": "NLP Course",
        "platform": "Hugging Face",
        "url": "https://huggingface.co/learn/nlp-course",
        "duration_hours": 30,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.8,
        "skills": ["Transformers", "NLP", "Hugging Face"],
        "for_roles": ["nlp_engineer", "genai_developer", "ml_engineer"]
    },
    "prompt_engineering": {
        "name": "ChatGPT Prompt Engineering for Developers",
        "platform": "DeepLearning.AI",
        "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/",
        "duration_hours": 2,
        "cost": "Free",
        "difficulty": "Beginner",
        "rating": 4.9,
        "skills": ["Prompt Engineering", "GPT API", "LLM Applications"],
        "for_roles": ["prompt_engineer", "genai_developer", "all"]
    },
    "building_rag": {
        "name": "Building RAG Agents with LLMs",
        "platform": "DeepLearning.AI",
        "url": "https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex/",
        "duration_hours": 3,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["RAG", "Vector Databases", "LlamaIndex"],
        "for_roles": ["genai_developer", "prompt_engineer"]
    },
    
    # Data Science
    "ibm_data_science": {
        "name": "IBM Data Science Professional Certificate",
        "platform": "Coursera",
        "url": "https://www.coursera.org/professional-certificates/ibm-data-science",
        "duration_hours": 200,
        "cost": "$49/month",
        "difficulty": "Beginner",
        "rating": 4.6,
        "skills": ["Python", "SQL", "Data Visualization", "ML"],
        "for_roles": ["data_scientist", "data_analyst"]
    },
    "kaggle_courses": {
        "name": "Kaggle Learn (All Courses)",
        "platform": "Kaggle",
        "url": "https://www.kaggle.com/learn",
        "duration_hours": 40,
        "cost": "Free",
        "difficulty": "Beginner-Intermediate",
        "rating": 4.7,
        "skills": ["Python", "Pandas", "ML", "Feature Engineering"],
        "for_roles": ["data_scientist", "ml_engineer", "data_analyst"]
    },
    "statistics_khan": {
        "name": "Statistics and Probability",
        "platform": "Khan Academy",
        "url": "https://www.khanacademy.org/math/statistics-probability",
        "duration_hours": 30,
        "cost": "Free",
        "difficulty": "Beginner",
        "rating": 4.8,
        "skills": ["Statistics", "Probability", "Hypothesis Testing"],
        "for_roles": ["data_scientist", "data_analyst", "ml_engineer"]
    },
    
    # Computer Vision
    "stanford_cs231n": {
        "name": "CS231n: Deep Learning for Computer Vision",
        "platform": "Stanford Online",
        "url": "https://cs231n.stanford.edu/",
        "duration_hours": 60,
        "cost": "Free",
        "difficulty": "Advanced",
        "rating": 4.9,
        "skills": ["CNN", "Object Detection", "Image Segmentation"],
        "for_roles": ["cv_engineer", "ai_researcher"]
    },
    "opencv_course": {
        "name": "OpenCV Python Course",
        "platform": "FreeCodeCamp/YouTube",
        "url": "https://www.youtube.com/watch?v=oXlwWbU8l2o",
        "duration_hours": 4,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.6,
        "skills": ["OpenCV", "Image Processing", "Computer Vision"],
        "for_roles": ["cv_engineer", "ml_engineer"]
    },
    
    # MLOps
    "mlops_specialization": {
        "name": "Machine Learning Engineering for Production (MLOps)",
        "platform": "Coursera (DeepLearning.AI)",
        "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops",
        "duration_hours": 80,
        "cost": "$49/month",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["MLOps", "Model Deployment", "Data Pipelines", "Monitoring"],
        "for_roles": ["mlops_engineer", "ml_engineer"]
    },
    "docker_beginners": {
        "name": "Docker for Beginners",
        "platform": "YouTube/TechWorld with Nana",
        "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
        "duration_hours": 3,
        "cost": "Free",
        "difficulty": "Beginner",
        "rating": 4.8,
        "skills": ["Docker", "Containers", "DevOps"],
        "for_roles": ["mlops_engineer", "ml_engineer", "genai_developer"]
    },
    "kubernetes_course": {
        "name": "Kubernetes Course",
        "platform": "YouTube/TechWorld with Nana",
        "url": "https://www.youtube.com/watch?v=X48VuDVv0do",
        "duration_hours": 4,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["Kubernetes", "Container Orchestration"],
        "for_roles": ["mlops_engineer"]
    },
    
    # Cloud & Tools
    "aws_ml": {
        "name": "AWS Machine Learning Specialty",
        "platform": "AWS Training",
        "url": "https://aws.amazon.com/training/learn-about/machine-learning/",
        "duration_hours": 40,
        "cost": "Free (Training) / $300 (Cert)",
        "difficulty": "Intermediate",
        "rating": 4.6,
        "skills": ["AWS", "SageMaker", "Cloud ML"],
        "for_roles": ["mlops_engineer", "ml_engineer"]
    },
    "gcp_ml": {
        "name": "Google Cloud ML Engineer Path",
        "platform": "Google Cloud",
        "url": "https://cloud.google.com/learn/training/machinelearning-ai",
        "duration_hours": 60,
        "cost": "Free (Training)",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["GCP", "Vertex AI", "BigQuery ML"],
        "for_roles": ["mlops_engineer", "ml_engineer"]
    },
    
    # Practice & Projects
    "leetcode_premium": {
        "name": "LeetCode (Data Structures & Algorithms)",
        "platform": "LeetCode",
        "url": "https://leetcode.com/",
        "duration_hours": 100,
        "cost": "Free / $35/month Premium",
        "difficulty": "All Levels",
        "rating": 4.8,
        "skills": ["Algorithms", "Data Structures", "Problem Solving"],
        "for_roles": ["all"]
    },
    "kaggle_competitions": {
        "name": "Kaggle Competitions",
        "platform": "Kaggle",
        "url": "https://www.kaggle.com/competitions",
        "duration_hours": 50,
        "cost": "Free",
        "difficulty": "All Levels",
        "rating": 4.9,
        "skills": ["ML", "Data Science", "Competition"],
        "for_roles": ["data_scientist", "ml_engineer"]
    },
    
    # Soft Skills & Career
    "ai_product_management": {
        "name": "AI Product Management",
        "platform": "Udacity",
        "url": "https://www.udacity.com/course/ai-product-manager-nanodegree--nd088",
        "duration_hours": 60,
        "cost": "$399/month",
        "difficulty": "Intermediate",
        "rating": 4.5,
        "skills": ["Product Management", "AI Strategy", "Roadmapping"],
        "for_roles": ["ai_pm"]
    },
    "technical_writing": {
        "name": "Technical Writing Courses",
        "platform": "Google",
        "url": "https://developers.google.com/tech-writing",
        "duration_hours": 10,
        "cost": "Free",
        "difficulty": "Beginner",
        "rating": 4.7,
        "skills": ["Technical Writing", "Documentation"],
        "for_roles": ["all"]
    },
    
    # ============================================
    # SCRIMBA AI COURSES (Recommended Partner)
    # ============================================
    
    # The flagship AI Engineer Path - Comprehensive
    "scrimba_ai_engineer_path": {
        "name": "The AI Engineer Path",
        "platform": "Scrimba",
        "url": "https://scrimba.com/the-ai-engineer-path-c02v?via=u436b310",
        "duration_hours": 11.2,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.9,
        "skills": ["AI Agents", "RAG", "MCP", "Embeddings", "Vector Databases", "Vercel AI SDK", "Multimodality", "Context Engineering"],
        "for_roles": ["ai_engineer", "prompt_engineer", "genai_developer", "fullstack_ai"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # Free Intro Course
    "scrimba_intro_ai_engineering": {
        "name": "Intro to AI Engineering",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/introtoaiengineering?via=u436b310",
        "duration_hours": 1.5,
        "cost": "Free",
        "difficulty": "Beginner",
        "rating": 4.8,
        "skills": ["LLMs", "OpenAI API", "AI Applications", "Web Development"],
        "for_roles": ["ai_engineer", "prompt_engineer", "genai_developer", "ml_engineer", "data_scientist"],
        "recommended": True,
        "badge": "🆓 Free"
    },
    
    # AI Agents Course
    "scrimba_ai_agents": {
        "name": "Learn AI Agents",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/aiagents?via=u436b310",
        "duration_hours": 2,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.9,
        "skills": ["AI Agents", "Multi-step Reasoning", "Function Calling", "APIs"],
        "for_roles": ["ai_engineer", "mlops_engineer", "ai_pm", "genai_developer"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # RAG Course
    "scrimba_rag": {
        "name": "Learn RAG (Retrieval-Augmented Generation)",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/rag?via=u436b310",
        "duration_hours": 1.5,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.8,
        "skills": ["RAG", "Embeddings", "Vector Databases", "LLM Applications"],
        "for_roles": ["ai_engineer", "nlp_engineer", "data_scientist", "genai_developer"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # Context Engineering
    "scrimba_context_engineering": {
        "name": "Learn Context Engineering",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/contextengineering?via=u436b310",
        "duration_hours": 1,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.8,
        "skills": ["Context Windows", "Token Optimization", "System Prompts", "Vercel AI SDK"],
        "for_roles": ["ai_engineer", "prompt_engineer", "genai_developer"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # Claude AI Course - Free
    "scrimba_claude_ai": {
        "name": "Intro to Claude AI",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/introtoclaudeai?via=u436b310",
        "duration_hours": 0.8,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["Claude API", "Anthropic", "AI Applications"],
        "for_roles": ["ai_engineer", "prompt_engineer", "genai_developer", "ml_engineer"],
        "recommended": True,
        "badge": "🆓 Free"
    },
    
    # Mistral AI Course - Free
    "scrimba_mistral_ai": {
        "name": "Intro to Mistral AI",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/introtomistral?via=u436b310",
        "duration_hours": 1.4,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["Mistral API", "Open-source LLMs", "RAG", "Function Calling"],
        "for_roles": ["ai_engineer", "ml_engineer", "genai_developer"],
        "recommended": True,
        "badge": "🆓 Free"
    },
    
    # LangChain.js - Free
    "scrimba_langchain": {
        "name": "Learn LangChain.js",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/langchain?via=u436b310",
        "duration_hours": 1.5,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.8,
        "skills": ["LangChain", "Document QA", "Chatbots", "RAG"],
        "for_roles": ["ai_engineer", "genai_developer", "fullstack_ai"],
        "recommended": True,
        "badge": "🆓 Free"
    },
    
    # Open-source AI Models
    "scrimba_opensource_models": {
        "name": "Open-source AI Models (with Hugging Face)",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/opensourceai?via=u436b310",
        "duration_hours": 0.6,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["Hugging Face", "Open-source LLMs", "Ollama", "Local AI"],
        "for_roles": ["ml_engineer", "ai_researcher", "ai_engineer"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # Build Support Agent
    "scrimba_support_agent": {
        "name": "Build a Support Agent with Vercel AI SDK",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/buildsupportagent?via=u436b310",
        "duration_hours": 2,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.8,
        "skills": ["Vercel AI SDK", "Support Chatbots", "Autonomous Agents", "Web Search"],
        "for_roles": ["ai_engineer", "ai_pm", "genai_developer"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # Model Context Protocol (MCP)
    "scrimba_mcp": {
        "name": "Intro to Model Context Protocol (MCP)",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/mcp?via=u436b310",
        "duration_hours": 0.6,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["MCP", "AI Tools", "Real-world Data Integration"],
        "for_roles": ["ai_engineer", "genai_developer"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # DALL-E & GPT Vision
    "scrimba_dalle_vision": {
        "name": "Intro to DALL-E and GPT Vision",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/introtodalle?via=u436b310",
        "duration_hours": 1,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["DALL-E", "GPT-4 Vision", "Image Generation", "Multimodal AI"],
        "for_roles": ["cv_engineer", "ai_engineer", "genai_developer"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # Deploy AI Apps - Free
    "scrimba_deploy_cloudflare": {
        "name": "Deploy AI Apps with Cloudflare",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/deployaiapps?via=u436b310",
        "duration_hours": 0.8,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.6,
        "skills": ["Cloudflare", "Edge Computing", "AI Deployment", "Low Latency"],
        "for_roles": ["mlops_engineer", "ai_engineer", "genai_developer"],
        "recommended": True,
        "badge": "🆓 Free"
    },
    
    # Prompt Engineering for Web Devs
    "scrimba_prompt_engineering": {
        "name": "Prompt Engineering for Web Developers",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/promptengineering?via=u436b310",
        "duration_hours": 3.1,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.8,
        "skills": ["Prompt Engineering", "AI-Assisted Coding", "Workflow Optimization"],
        "for_roles": ["prompt_engineer", "ai_pm", "genai_developer", "ai_engineer"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # OpenAI Assistants API
    "scrimba_openai_assistants": {
        "name": "Learn OpenAI's Assistants API",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/openaiassistants?via=u436b310",
        "duration_hours": 0.5,
        "cost": "Pro Subscription",
        "difficulty": "Intermediate",
        "rating": 4.7,
        "skills": ["OpenAI Assistants", "Knowledge Retrieval", "Agent Capabilities"],
        "for_roles": ["ai_engineer", "genai_developer", "fullstack_ai"],
        "recommended": True,
        "badge": "⭐ Recommended"
    },
    
    # Serverless AI Agents - Free
    "scrimba_serverless_agents": {
        "name": "Build Serverless AI Agents with Langbase",
        "platform": "Scrimba",
        "url": "https://scrimba.com/learn/langbase?via=u436b310",
        "duration_hours": 0.8,
        "cost": "Free",
        "difficulty": "Intermediate",
        "rating": 4.6,
        "skills": ["Langbase", "Serverless AI", "AI Agents"],
        "for_roles": ["ai_engineer", "mlops_engineer", "genai_developer"],
        "recommended": True,
        "badge": "🆓 Free"
    }
}


def get_courses_for_role(role_id: str, difficulty: str = None) -> list:
    """Get relevant courses for a specific role"""
    courses = []
    for course_id, course in COURSE_DATABASE.items():
        if "all" in course.get("for_roles", []) or role_id in course.get("for_roles", []):
            if difficulty is None or course.get("difficulty", "").lower().startswith(difficulty.lower()):
                courses.append({
                    "id": course_id,
                    **course
                })
    return courses


def get_scrimba_courses() -> list:
    """Get all Scrimba courses (recommended partner)"""
    return [
        {"id": course_id, **course}
        for course_id, course in COURSE_DATABASE.items()
        if course.get("platform") == "Scrimba"
    ]


def get_free_courses() -> list:
    """Get all free courses"""
    return [
        {"id": course_id, **course}
        for course_id, course in COURSE_DATABASE.items()
        if "free" in course.get("cost", "").lower()
    ]
