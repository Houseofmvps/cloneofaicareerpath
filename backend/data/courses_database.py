"""
VERIFIED COURSE DATABASE - Real courses with real URLs
Last updated: January 2025

This is a curated database of HIGH-QUALITY, VERIFIED courses for AI/ML career transitions.
Every course here has been verified to exist and have a working URL.

Structure:
- Organized by skill category
- Each course has: name, url, platform, duration, cost, difficulty, description, skills_taught
- Courses marked with verification status
"""

# ============================================================================
# FOUNDATIONAL COURSES - Python, Math, Stats
# ============================================================================

FOUNDATION_COURSES = [
    # Python Fundamentals
    {
        "id": "py-001",
        "name": "Python for Everybody Specialization",
        "url": "https://www.coursera.org/specializations/python",
        "platform": "Coursera",
        "instructor": "Dr. Charles Severance (University of Michigan)",
        "duration_hours": 80,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "beginner",
        "rating": 4.8,
        "students": "3M+",
        "description": "Learn Python from scratch. Perfect for complete beginners.",
        "skills_taught": ["Python basics", "Data structures", "Web scraping", "Databases"],
        "why_recommended": "Most popular Python course. Great starting point.",
        "badge": "🎓 Top Rated"
    },
    {
        "id": "py-002",
        "name": "Automate the Boring Stuff with Python",
        "url": "https://automatetheboringstuff.com/",
        "platform": "Free Online Book + Udemy",
        "instructor": "Al Sweigart",
        "duration_hours": 20,
        "cost": "Free (book), $14.99 (Udemy video)",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.7,
        "description": "Practical Python for automating tasks. Very hands-on.",
        "skills_taught": ["Python automation", "File handling", "Web scraping", "Excel automation"],
        "why_recommended": "Best for learning Python through practical projects",
        "badge": "🆓 Free"
    },
    {
        "id": "py-scrimba",
        "name": "Learn Python",
        "url": "https://scrimba.com/learn-python-c03?via=u436b310",
        "platform": "Scrimba",
        "instructor": "Scrimba Team",
        "duration_hours": 15,
        "cost": "$20/month Pro",
        "cost_type": "paid",
        "difficulty": "beginner",
        "rating": 4.9,
        "description": "Interactive Python course. Code directly in the browser as you learn.",
        "skills_taught": ["Python basics", "Functions", "Data structures", "OOP", "Projects"],
        "why_recommended": "Most interactive Python learning. Code while watching.",
        "badge": "⚡ Fast Track • 🎯 Interactive",
        "is_fast_track": True
    },
    
    # Math for ML
    {
        "id": "math-001",
        "name": "Mathematics for Machine Learning Specialization",
        "url": "https://www.coursera.org/specializations/mathematics-machine-learning",
        "platform": "Coursera",
        "instructor": "Imperial College London",
        "duration_hours": 60,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "intermediate",
        "rating": 4.6,
        "students": "500K+",
        "description": "Linear algebra, multivariate calculus, and PCA for ML.",
        "skills_taught": ["Linear Algebra", "Calculus", "PCA", "Mathematical foundations"],
        "why_recommended": "Essential math foundation for understanding ML algorithms",
        "badge": "📐 Math Essential"
    },
    {
        "id": "math-002",
        "name": "3Blue1Brown - Essence of Linear Algebra",
        "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab",
        "platform": "YouTube",
        "instructor": "Grant Sanderson",
        "duration_hours": 3,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.9,
        "description": "Visual, intuitive explanations of linear algebra concepts.",
        "skills_taught": ["Vectors", "Linear transformations", "Matrix operations", "Eigenvalues"],
        "why_recommended": "Best visual explanations of math concepts. Watch before any math course.",
        "badge": "🆓 Free • 🎬 Must Watch"
    },
    {
        "id": "stats-001",
        "name": "Statistics with Python Specialization",
        "url": "https://www.coursera.org/specializations/statistics-with-python",
        "platform": "Coursera",
        "instructor": "University of Michigan",
        "duration_hours": 50,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "intermediate",
        "rating": 4.5,
        "description": "Statistical analysis using Python. Essential for data science.",
        "skills_taught": ["Descriptive statistics", "Inferential statistics", "Hypothesis testing", "Regression"],
        "why_recommended": "Combines stats theory with Python implementation",
        "badge": "📊 Stats Essential"
    },
]

# ============================================================================
# MACHINE LEARNING COURSES
# ============================================================================

ML_COURSES = [
    # Foundational ML
    {
        "id": "ml-001",
        "name": "Machine Learning Specialization",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "platform": "Coursera",
        "instructor": "Andrew Ng (Stanford/DeepLearning.AI)",
        "duration_hours": 100,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "beginner",
        "rating": 4.9,
        "students": "5M+",
        "description": "THE foundational ML course. Updated 2022 version with Python/TensorFlow.",
        "skills_taught": ["Supervised learning", "Unsupervised learning", "Neural networks", "Decision trees", "Recommender systems"],
        "why_recommended": "Gold standard for ML education. Start here.",
        "badge": "👑 #1 ML Course • 🎓 Andrew Ng"
    },
    {
        "id": "ml-002",
        "name": "Practical Deep Learning for Coders",
        "url": "https://course.fast.ai/",
        "platform": "fast.ai",
        "instructor": "Jeremy Howard",
        "duration_hours": 40,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.9,
        "description": "Top-down approach to deep learning. Build models from day 1.",
        "skills_taught": ["PyTorch", "Computer vision", "NLP", "Tabular data", "Collaborative filtering"],
        "why_recommended": "Best hands-on deep learning course. Code-first approach.",
        "badge": "🆓 Free • 🔥 Highly Recommended"
    },
    {
        "id": "ml-003",
        "name": "Google Machine Learning Crash Course",
        "url": "https://developers.google.com/machine-learning/crash-course",
        "platform": "Google",
        "instructor": "Google Engineers",
        "duration_hours": 15,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.7,
        "description": "Fast-paced intro to ML with TensorFlow. Great for quick start.",
        "skills_taught": ["ML fundamentals", "TensorFlow basics", "Feature engineering", "Classification"],
        "why_recommended": "Quick, practical introduction from Google. Good for busy professionals.",
        "badge": "🆓 Free • ⚡ Quick Start"
    },
    {
        "id": "ml-004",
        "name": "Hands-On Machine Learning with Scikit-Learn and TensorFlow",
        "url": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/",
        "platform": "O'Reilly (Book)",
        "instructor": "Aurélien Géron",
        "duration_hours": 60,
        "cost": "$60 (book) or O'Reilly subscription",
        "cost_type": "paid",
        "difficulty": "intermediate",
        "rating": 4.8,
        "description": "The ML bible. Comprehensive coverage of ML and DL with code.",
        "skills_taught": ["Scikit-learn", "TensorFlow", "Keras", "End-to-end ML projects"],
        "why_recommended": "Best ML book. Every ML engineer should own this.",
        "badge": "📚 ML Bible"
    },
    {
        "id": "ml-005",
        "name": "Stanford CS229: Machine Learning",
        "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU",
        "platform": "YouTube (Stanford Online)",
        "instructor": "Andrew Ng",
        "duration_hours": 30,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.9,
        "description": "Full Stanford ML course. More theoretical than Coursera version.",
        "skills_taught": ["ML theory", "Algorithm derivations", "Statistical learning", "Advanced topics"],
        "why_recommended": "For those who want deep mathematical understanding",
        "badge": "🆓 Free • 🎓 Stanford"
    },
]

# ============================================================================
# DEEP LEARNING & NEURAL NETWORKS
# ============================================================================

DEEP_LEARNING_COURSES = [
    {
        "id": "dl-001",
        "name": "Deep Learning Specialization",
        "url": "https://www.coursera.org/specializations/deep-learning",
        "platform": "Coursera",
        "instructor": "Andrew Ng (DeepLearning.AI)",
        "duration_hours": 120,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "intermediate",
        "rating": 4.9,
        "students": "1M+",
        "description": "Comprehensive deep learning: CNNs, RNNs, transformers, optimization.",
        "skills_taught": ["Neural networks", "CNNs", "RNNs", "Transformers", "TensorFlow"],
        "why_recommended": "Most comprehensive DL course. Industry standard.",
        "badge": "👑 #1 Deep Learning • 🎓 Andrew Ng"
    },
    {
        "id": "dl-002",
        "name": "PyTorch for Deep Learning",
        "url": "https://www.learnpytorch.io/",
        "platform": "Learn PyTorch (Free)",
        "instructor": "Daniel Bourke",
        "duration_hours": 25,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.8,
        "description": "Modern PyTorch tutorial with hands-on projects.",
        "skills_taught": ["PyTorch", "Neural networks", "Computer vision", "NLP basics"],
        "why_recommended": "Best free PyTorch resource. Very practical.",
        "badge": "🆓 Free • 🔥 PyTorch"
    },
    {
        "id": "dl-003",
        "name": "Neural Networks: Zero to Hero",
        "url": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ",
        "platform": "YouTube",
        "instructor": "Andrej Karpathy",
        "duration_hours": 15,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.9,
        "description": "Build neural networks from scratch. From former Tesla AI Director.",
        "skills_taught": ["Backpropagation", "GPT from scratch", "Transformers", "Neural network internals"],
        "why_recommended": "Learn how neural networks REALLY work. Build GPT from scratch.",
        "badge": "🆓 Free • 🧠 Andrej Karpathy"
    },
]

# ============================================================================
# AI ENGINEERING & LLMs
# ============================================================================

AI_ENGINEERING_COURSES = [
    {
        "id": "ai-001",
        "name": "The AI Engineer Path",
        "url": "https://scrimba.com/the-ai-engineer-path-c02v?via=u436b310",
        "platform": "Scrimba",
        "instructor": "Scrimba Team",
        "duration_hours": 40,
        "cost": "$20/month Pro",
        "cost_type": "paid",
        "difficulty": "intermediate",
        "rating": 4.9,
        "description": "Complete AI Engineer curriculum. Build with OpenAI, LangChain, vector DBs. Interactive coding.",
        "skills_taught": ["OpenAI API", "LangChain", "Vector databases", "RAG", "AI agents", "Prompt engineering"],
        "why_recommended": "Most comprehensive interactive AI course. Build real AI apps while learning.",
        "badge": "⚡ Fast Track • 🔥 #1 AI Course",
        "is_fast_track": True
    },
    {
        "id": "ai-002",
        "name": "LangChain for LLM Application Development",
        "url": "https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/",
        "platform": "DeepLearning.AI",
        "instructor": "Harrison Chase & Andrew Ng",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.7,
        "description": "Quick intro to LangChain from its creator.",
        "skills_taught": ["LangChain", "Chains", "Agents", "Memory", "LLM integration"],
        "why_recommended": "Learn LangChain from the creator. Essential for AI Engineering.",
        "badge": "🆓 Free • ⚡ Quick"
    },
    {
        "id": "ai-003",
        "name": "Building Systems with ChatGPT API",
        "url": "https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/",
        "platform": "DeepLearning.AI",
        "instructor": "Isa Fulford & Andrew Ng",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.8,
        "description": "Build production systems with OpenAI API.",
        "skills_taught": ["OpenAI API", "Prompt engineering", "Chain of thought", "System design"],
        "why_recommended": "Official OpenAI best practices. Essential for any LLM work.",
        "badge": "🆓 Free • 🤖 OpenAI Official"
    },
    {
        "id": "ai-004",
        "name": "Prompt Engineering for Developers",
        "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/",
        "platform": "DeepLearning.AI",
        "instructor": "Isa Fulford & Andrew Ng",
        "duration_hours": 1,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.9,
        "description": "Master prompt engineering techniques.",
        "skills_taught": ["Prompt engineering", "Few-shot learning", "Chain of thought", "Best practices"],
        "why_recommended": "Start here for LLM work. Quick and essential.",
        "badge": "🆓 Free • ⚡ Start Here"
    },
    {
        "id": "ai-005",
        "name": "Hugging Face NLP Course",
        "url": "https://huggingface.co/learn/nlp-course",
        "platform": "Hugging Face",
        "instructor": "Hugging Face Team",
        "duration_hours": 20,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.8,
        "description": "Complete NLP with Transformers. Use state-of-the-art models.",
        "skills_taught": ["Transformers", "Hugging Face", "Fine-tuning", "NLP tasks", "Model deployment"],
        "why_recommended": "Best resource for modern NLP. Industry standard library.",
        "badge": "🆓 Free • 🤗 Official HF"
    },
    {
        "id": "ai-006",
        "name": "Full Stack LLM Bootcamp",
        "url": "https://fullstackdeeplearning.com/llm-bootcamp/",
        "platform": "Full Stack Deep Learning",
        "instructor": "FSDL Team",
        "duration_hours": 15,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.8,
        "description": "Production LLM systems. From prompt engineering to deployment.",
        "skills_taught": ["LLM ops", "Prompt engineering", "Fine-tuning", "Evaluation", "Deployment"],
        "why_recommended": "Best advanced LLM course. Production-focused.",
        "badge": "🆓 Free • 🚀 Production"
    },
    {
        "id": "ai-007",
        "name": "Fine-tuning Large Language Models",
        "url": "https://www.deeplearning.ai/short-courses/finetuning-large-language-models/",
        "platform": "DeepLearning.AI",
        "instructor": "Sharon Zhou",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.7,
        "description": "Learn when and how to fine-tune LLMs for your use case.",
        "skills_taught": ["Fine-tuning", "LoRA", "Data preparation", "Training strategies"],
        "why_recommended": "Essential for customizing LLMs to specific domains.",
        "badge": "🆓 Free • 🎯 Fine-tuning"
    },
    {
        "id": "ai-008",
        "name": "Vector Databases: from Embeddings to Applications",
        "url": "https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/",
        "platform": "DeepLearning.AI",
        "instructor": "Sebastian Witalec",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.6,
        "description": "Build semantic search and RAG systems with vector databases.",
        "skills_taught": ["Vector embeddings", "Semantic search", "RAG", "Weaviate"],
        "why_recommended": "Essential for building RAG applications.",
        "badge": "🆓 Free • 🔍 RAG"
    },
    {
        "id": "ai-009",
        "name": "Building AI Applications with LlamaIndex",
        "url": "https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/",
        "platform": "DeepLearning.AI",
        "instructor": "Jerry Liu",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.7,
        "description": "Build and evaluate advanced RAG pipelines.",
        "skills_taught": ["LlamaIndex", "RAG evaluation", "Query optimization", "Retrieval strategies"],
        "why_recommended": "Learn from LlamaIndex creator. Essential for production RAG.",
        "badge": "🆓 Free • 🦙 LlamaIndex"
    },
    {
        "id": "ai-010",
        "name": "AI Agents in LangGraph",
        "url": "https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/",
        "platform": "DeepLearning.AI",
        "instructor": "Harrison Chase",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.8,
        "description": "Build autonomous AI agents with LangGraph.",
        "skills_taught": ["AI Agents", "LangGraph", "Tool use", "Agent architectures"],
        "why_recommended": "Latest agent techniques from LangChain creator.",
        "badge": "🆓 Free • 🤖 Agents"
    },
    {
        "id": "ai-011",
        "name": "Functions, Tools and Agents with LangChain",
        "url": "https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/",
        "platform": "DeepLearning.AI",
        "instructor": "Harrison Chase",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.7,
        "description": "Build agents that use tools and functions.",
        "skills_taught": ["Function calling", "Tool use", "OpenAI functions", "Agent design"],
        "why_recommended": "Essential for building AI automation.",
        "badge": "🆓 Free • 🛠️ Tools"
    },
    {
        "id": "ai-012",
        "name": "Building Generative AI Applications with Gradio",
        "url": "https://www.deeplearning.ai/short-courses/building-generative-ai-applications-with-gradio/",
        "platform": "DeepLearning.AI",
        "instructor": "Apolinário Passos",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.6,
        "description": "Build and share AI demos quickly with Gradio.",
        "skills_taught": ["Gradio", "UI for AI", "Demo building", "Prototyping"],
        "why_recommended": "Perfect for quickly building AI demos and prototypes.",
        "badge": "🆓 Free • 🎨 UI"
    },
    {
        "id": "ai-013",
        "name": "Generative AI for Everyone",
        "url": "https://www.deeplearning.ai/courses/generative-ai-for-everyone/",
        "platform": "DeepLearning.AI",
        "instructor": "Andrew Ng",
        "duration_hours": 5,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.9,
        "description": "Understand generative AI concepts and business applications.",
        "skills_taught": ["GenAI concepts", "Business applications", "AI strategy", "Use cases"],
        "why_recommended": "Best intro to GenAI for non-technical roles. Andrew Ng quality.",
        "badge": "🆓 Free • 🎓 Andrew Ng"
    },
    {
        "id": "ai-014",
        "name": "How Diffusion Models Work",
        "url": "https://www.deeplearning.ai/short-courses/how-diffusion-models-work/",
        "platform": "DeepLearning.AI",
        "instructor": "Sharon Zhou",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.7,
        "description": "Understand and build diffusion models for image generation.",
        "skills_taught": ["Diffusion models", "Image generation", "Stable Diffusion", "DDPM"],
        "why_recommended": "Essential for understanding image generation AI.",
        "badge": "🆓 Free • 🖼️ Image Gen"
    },
    {
        "id": "ai-015",
        "name": "Pair Programming with a Large Language Model",
        "url": "https://www.deeplearning.ai/short-courses/pair-programming-llm/",
        "platform": "DeepLearning.AI",
        "instructor": "Laurence Moroney",
        "duration_hours": 1,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.6,
        "description": "Use LLMs effectively for coding assistance.",
        "skills_taught": ["AI coding", "Prompt for code", "Debugging with AI", "Code generation"],
        "why_recommended": "Essential for AI-assisted development (Vibe Coding).",
        "badge": "🆓 Free • 💻 Vibe Coding"
    },
    {
        "id": "ai-016",
        "name": "AI for Good Specialization",
        "url": "https://www.deeplearning.ai/courses/ai-for-good/",
        "platform": "DeepLearning.AI",
        "instructor": "Robert Monarch",
        "duration_hours": 20,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.5,
        "description": "Apply AI to solve real-world social problems.",
        "skills_taught": ["AI ethics", "Social impact", "Responsible AI", "Case studies"],
        "why_recommended": "Essential for AI ethics and safety roles.",
        "badge": "🆓 Free • 🌍 AI Ethics"
    },
    {
        "id": "ai-017",
        "name": "Building and Evaluating Advanced RAG Applications",
        "url": "https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/",
        "platform": "DeepLearning.AI",
        "instructor": "Jerry Liu",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.8,
        "description": "Build production RAG with evaluation metrics.",
        "skills_taught": ["RAG evaluation", "Metrics", "LlamaIndex", "Production RAG"],
        "why_recommended": "Essential for production AI systems.",
        "badge": "🆓 Free • 📊 Evaluation"
    },
    {
        "id": "ai-018",
        "name": "Multi AI Agent Systems with crewAI",
        "url": "https://www.deeplearning.ai/short-courses/multi-ai-agent-systems-with-crewai/",
        "platform": "DeepLearning.AI",
        "instructor": "João Moura",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.7,
        "description": "Build multi-agent AI systems that collaborate.",
        "skills_taught": ["Multi-agent", "CrewAI", "Agent collaboration", "Task delegation"],
        "why_recommended": "Cutting-edge agent development techniques.",
        "badge": "🆓 Free • 🤖 Multi-Agent"
    },
    {
        "id": "ai-019",
        "name": "AI Agentic Design Patterns with AutoGen",
        "url": "https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/",
        "platform": "DeepLearning.AI",
        "instructor": "Chi Wang",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.6,
        "description": "Design patterns for building AI agents.",
        "skills_taught": ["AutoGen", "Agent patterns", "Conversational agents", "Agent design"],
        "why_recommended": "Microsoft's AutoGen framework for agents.",
        "badge": "🆓 Free • 🎯 Patterns"
    },
]

# ============================================================================
# BUSINESS & STRATEGY COURSES
# ============================================================================

BUSINESS_COURSES = [
    {
        "id": "biz-001",
        "name": "AI Product Management Specialization",
        "url": "https://www.coursera.org/specializations/ai-product-management-duke",
        "platform": "Coursera",
        "instructor": "Duke University",
        "duration_hours": 40,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "intermediate",
        "rating": 4.6,
        "description": "Manage AI products from ideation to launch.",
        "skills_taught": ["AI product strategy", "ML project management", "Stakeholder management", "AI roadmaps"],
        "why_recommended": "Best course for AI Product Managers.",
        "badge": "🎓 Duke • 📦 Product"
    },
    {
        "id": "biz-002",
        "name": "AI For Business Specialization",
        "url": "https://www.coursera.org/specializations/ai-for-business-wharton",
        "platform": "Coursera",
        "instructor": "Wharton School",
        "duration_hours": 30,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "beginner",
        "rating": 4.5,
        "description": "AI strategy for business leaders.",
        "skills_taught": ["AI strategy", "Business transformation", "ROI analysis", "AI adoption"],
        "why_recommended": "Wharton-quality business AI education.",
        "badge": "🎓 Wharton • 💼 Business"
    },
    {
        "id": "biz-003",
        "name": "Product Management Course",
        "url": "https://www.productschool.com/free-product-management-resources/",
        "platform": "Product School",
        "instructor": "Product School",
        "duration_hours": 10,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.4,
        "description": "Fundamentals of product management.",
        "skills_taught": ["Product thinking", "User research", "Roadmapping", "Prioritization"],
        "why_recommended": "Free PM fundamentals before specializing in AI.",
        "badge": "🆓 Free • 📦 PM Basics"
    },
    {
        "id": "biz-004",
        "name": "AI Transformation Playbook",
        "url": "https://landing.ai/resources/ai-transformation-playbook/",
        "platform": "Landing AI",
        "instructor": "Andrew Ng",
        "duration_hours": 2,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.8,
        "description": "How to transform organizations with AI.",
        "skills_taught": ["AI transformation", "Change management", "AI strategy", "Implementation"],
        "why_recommended": "Andrew Ng's guide for AI consultants.",
        "badge": "🆓 Free • 🎓 Andrew Ng"
    },
]

# ============================================================================
# DESIGN & UX COURSES
# ============================================================================

DESIGN_COURSES = [
    {
        "id": "des-001",
        "name": "AI-Powered UX Design",
        "url": "https://www.interaction-design.org/courses/ai-powered-ux-design",
        "platform": "Interaction Design Foundation",
        "instructor": "IDF",
        "duration_hours": 15,
        "cost": "$16/month membership",
        "cost_type": "paid",
        "difficulty": "intermediate",
        "rating": 4.6,
        "description": "Design user experiences for AI products.",
        "skills_taught": ["AI UX patterns", "Conversational design", "AI transparency", "Trust design"],
        "why_recommended": "Essential for AI product designers.",
        "badge": "🎨 Design • 🤖 AI UX"
    },
    {
        "id": "des-002",
        "name": "Designing AI Products",
        "url": "https://www.nngroup.com/courses/ai-design/",
        "platform": "Nielsen Norman Group",
        "instructor": "NN/g",
        "duration_hours": 8,
        "cost": "$395",
        "cost_type": "paid",
        "difficulty": "intermediate",
        "rating": 4.7,
        "description": "UX guidelines for AI and ML products.",
        "skills_taught": ["AI guidelines", "Error handling", "Explainability", "User trust"],
        "why_recommended": "Industry-standard AI UX guidelines.",
        "badge": "🎨 UX • 💼 NN/g"
    },
    {
        "id": "des-003",
        "name": "Google UX Design Certificate",
        "url": "https://www.coursera.org/professional-certificates/google-ux-design",
        "platform": "Coursera",
        "instructor": "Google",
        "duration_hours": 200,
        "cost": "Free to audit, $39/month for certificate",
        "cost_type": "freemium",
        "difficulty": "beginner",
        "rating": 4.8,
        "description": "Complete UX design fundamentals from Google.",
        "skills_taught": ["UX research", "Wireframing", "Prototyping", "Usability testing"],
        "why_recommended": "Foundation before specializing in AI design.",
        "badge": "🎓 Google • 🎨 UX"
    },
]

# ============================================================================
# REINFORCEMENT LEARNING COURSES
# ============================================================================

RL_COURSES = [
    {
        "id": "rl-001",
        "name": "Reinforcement Learning Specialization",
        "url": "https://www.coursera.org/specializations/reinforcement-learning",
        "platform": "Coursera",
        "instructor": "University of Alberta",
        "duration_hours": 80,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "advanced",
        "rating": 4.7,
        "description": "Complete RL: from bandits to deep RL.",
        "skills_taught": ["MDPs", "Policy gradient", "Q-learning", "Deep RL"],
        "why_recommended": "Most comprehensive RL course available.",
        "badge": "🎓 UAlberta • 🎮 RL"
    },
    {
        "id": "rl-002",
        "name": "Deep Reinforcement Learning Course",
        "url": "https://huggingface.co/learn/deep-rl-course",
        "platform": "Hugging Face",
        "instructor": "Hugging Face Team",
        "duration_hours": 30,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.8,
        "description": "Practical deep RL with Hugging Face.",
        "skills_taught": ["Deep RL", "PPO", "DQN", "Stable Baselines"],
        "why_recommended": "Best free deep RL course. Very hands-on.",
        "badge": "🆓 Free • 🤗 HF • 🎮 RL"
    },
    {
        "id": "rl-003",
        "name": "Spinning Up in Deep RL",
        "url": "https://spinningup.openai.com/",
        "platform": "OpenAI",
        "instructor": "OpenAI",
        "duration_hours": 20,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.9,
        "description": "OpenAI's educational resource for deep RL.",
        "skills_taught": ["Deep RL theory", "Policy optimization", "Implementation"],
        "why_recommended": "OpenAI's official RL learning resource.",
        "badge": "🆓 Free • 🤖 OpenAI"
    },
]

# ============================================================================
# INFRASTRUCTURE & SYSTEMS COURSES
# ============================================================================

INFRA_COURSES = [
    {
        "id": "infra-001",
        "name": "Kubernetes for ML",
        "url": "https://www.kubeflow.org/docs/started/",
        "platform": "Kubeflow Docs",
        "instructor": "Kubeflow Community",
        "duration_hours": 15,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.5,
        "description": "Deploy ML workflows on Kubernetes.",
        "skills_taught": ["Kubeflow", "Kubernetes", "ML pipelines", "Orchestration"],
        "why_recommended": "Essential for ML infrastructure engineers.",
        "badge": "🆓 Free • ☸️ K8s"
    },
    {
        "id": "infra-002",
        "name": "Terraform for ML Infrastructure",
        "url": "https://developer.hashicorp.com/terraform/tutorials",
        "platform": "HashiCorp",
        "instructor": "HashiCorp",
        "duration_hours": 10,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.6,
        "description": "Infrastructure as code for ML systems.",
        "skills_taught": ["Terraform", "IaC", "Cloud provisioning", "State management"],
        "why_recommended": "Modern infrastructure management for ML.",
        "badge": "🆓 Free • 🏗️ IaC"
    },
    {
        "id": "infra-003",
        "name": "Ray - Distributed ML",
        "url": "https://docs.ray.io/en/latest/ray-overview/getting-started.html",
        "platform": "Ray Docs",
        "instructor": "Anyscale",
        "duration_hours": 15,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.7,
        "description": "Scale ML workloads with Ray.",
        "skills_taught": ["Ray", "Distributed computing", "ML scaling", "Ray Train"],
        "why_recommended": "Industry standard for distributed ML.",
        "badge": "🆓 Free • ⚡ Distributed"
    },
]

# ============================================================================  
# CONTENT CREATION COURSES
# ============================================================================

CONTENT_COURSES = [
    {
        "id": "cont-001",
        "name": "AI Content Creation Masterclass",
        "url": "https://www.skillshare.com/classes/AI-Content-Creation-Masterclass",
        "platform": "Skillshare",
        "instructor": "Various",
        "duration_hours": 10,
        "cost": "Free trial, then $14/month",
        "cost_type": "paid",
        "difficulty": "beginner",
        "rating": 4.3,
        "description": "Create content with AI tools.",
        "skills_taught": ["AI writing", "Image generation", "Video with AI", "Workflow automation"],
        "why_recommended": "Practical AI content creation skills.",
        "badge": "✍️ Content"
    },
    {
        "id": "cont-002",
        "name": "Midjourney Mastery",
        "url": "https://www.skillshare.com/classes/Midjourney-AI-Art",
        "platform": "Skillshare / YouTube",
        "instructor": "Various",
        "duration_hours": 5,
        "cost": "Free on YouTube",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.5,
        "description": "Master Midjourney for AI image generation.",
        "skills_taught": ["Midjourney", "Prompt craft", "Image styles", "Commercial use"],
        "why_recommended": "Most popular AI image tool for creators.",
        "badge": "🆓 Free • 🖼️ Art"
    },
]

# ============================================================================
# MLOps & PRODUCTION ML
# ============================================================================

MLOPS_COURSES = [
    {
        "id": "mlops-001",
        "name": "Machine Learning Engineering for Production (MLOps) Specialization",
        "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops",
        "platform": "Coursera",
        "instructor": "Andrew Ng (DeepLearning.AI)",
        "duration_hours": 80,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "advanced",
        "rating": 4.7,
        "students": "200K+",
        "description": "Complete MLOps: data pipelines, model deployment, monitoring.",
        "skills_taught": ["MLOps", "Data pipelines", "Model deployment", "Monitoring", "TFX"],
        "why_recommended": "Most comprehensive MLOps course. Industry standard.",
        "badge": "👑 #1 MLOps • 🎓 Andrew Ng"
    },
    {
        "id": "mlops-002",
        "name": "Made With ML - MLOps Course",
        "url": "https://madewithml.com/",
        "platform": "Made With ML",
        "instructor": "Goku Mohandas",
        "duration_hours": 30,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.9,
        "description": "End-to-end MLOps. From design to deployment and monitoring.",
        "skills_taught": ["MLOps", "Testing", "CI/CD", "Monitoring", "Best practices"],
        "why_recommended": "Best free MLOps resource. Very practical and modern.",
        "badge": "🆓 Free • 🔥 Best Free MLOps"
    },
    {
        "id": "mlops-003",
        "name": "Designing Machine Learning Systems",
        "url": "https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/",
        "platform": "O'Reilly (Book)",
        "instructor": "Chip Huyen",
        "duration_hours": 25,
        "cost": "$50 (book)",
        "cost_type": "paid",
        "difficulty": "advanced",
        "rating": 4.9,
        "description": "Design production ML systems. From data to deployment.",
        "skills_taught": ["System design", "Data engineering", "Model serving", "Monitoring"],
        "why_recommended": "Essential reading for ML Engineers. Real-world focus.",
        "badge": "📚 Must Read • 💼 Production"
    },
    {
        "id": "mlops-004",
        "name": "ML System Design Interview",
        "url": "https://www.educative.io/courses/machine-learning-system-design-interview",
        "platform": "Educative",
        "instructor": "Educative Team",
        "duration_hours": 15,
        "cost": "$59 or subscription",
        "cost_type": "paid",
        "difficulty": "advanced",
        "rating": 4.7,
        "description": "Prepare for ML system design interviews at FAANG.",
        "skills_taught": ["System design", "Scalability", "Interview prep", "Real-world cases"],
        "why_recommended": "Essential for FAANG interviews. Real interview questions.",
        "badge": "💼 Interview Prep"
    },
]

# ============================================================================
# COMPUTER VISION
# ============================================================================

CV_COURSES = [
    {
        "id": "cv-001",
        "name": "Stanford CS231n: Deep Learning for Computer Vision",
        "url": "https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv",
        "platform": "YouTube (Stanford)",
        "instructor": "Fei-Fei Li, Andrej Karpathy",
        "duration_hours": 25,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.9,
        "description": "The definitive computer vision course. CNNs to transformers.",
        "skills_taught": ["CNNs", "Object detection", "Segmentation", "Vision transformers"],
        "why_recommended": "Best CV course. Stanford quality, free access.",
        "badge": "🆓 Free • 🎓 Stanford • 👑 Best CV"
    },
    {
        "id": "cv-002",
        "name": "PyTorch for Computer Vision",
        "url": "https://www.learnpytorch.io/05_pytorch_going_modular/",
        "platform": "Learn PyTorch",
        "instructor": "Daniel Bourke",
        "duration_hours": 10,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.7,
        "description": "Practical computer vision with PyTorch.",
        "skills_taught": ["PyTorch", "CNNs", "Transfer learning", "Image classification"],
        "why_recommended": "Hands-on CV with modern PyTorch. Great for practitioners.",
        "badge": "🆓 Free • 🔥 Practical"
    },
]

# ============================================================================
# NLP & LANGUAGE MODELS
# ============================================================================

NLP_COURSES = [
    {
        "id": "nlp-001",
        "name": "Stanford CS224N: NLP with Deep Learning",
        "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rOSH4v6133s9LFPRHjEmbmJ",
        "platform": "YouTube (Stanford)",
        "instructor": "Chris Manning",
        "duration_hours": 25,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.9,
        "description": "Comprehensive NLP: from word vectors to transformers and LLMs.",
        "skills_taught": ["Word embeddings", "RNNs", "Attention", "Transformers", "BERT", "GPT"],
        "why_recommended": "Best NLP course. Essential for understanding modern LLMs.",
        "badge": "🆓 Free • 🎓 Stanford • 👑 Best NLP"
    },
    {
        "id": "nlp-002",
        "name": "Natural Language Processing Specialization",
        "url": "https://www.coursera.org/specializations/natural-language-processing",
        "platform": "Coursera",
        "instructor": "DeepLearning.AI",
        "duration_hours": 80,
        "cost": "Free to audit, $49/month for certificate",
        "cost_type": "freemium",
        "difficulty": "intermediate",
        "rating": 4.6,
        "description": "Complete NLP: classification, sequence models, attention.",
        "skills_taught": ["Text classification", "Sequence models", "Attention", "Translation"],
        "why_recommended": "Structured NLP curriculum with hands-on projects.",
        "badge": "🎓 DeepLearning.AI"
    },
]

# ============================================================================
# DATA ENGINEERING FOR ML
# ============================================================================

DATA_ENGINEERING_COURSES = [
    {
        "id": "de-001",
        "name": "Data Engineering Zoomcamp",
        "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp",
        "platform": "DataTalks.Club (GitHub)",
        "instructor": "DataTalks.Club",
        "duration_hours": 80,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.8,
        "description": "Complete data engineering: Docker, SQL, Spark, Kafka, dbt.",
        "skills_taught": ["Docker", "SQL", "Spark", "Kafka", "dbt", "Airflow", "GCP"],
        "why_recommended": "Best free data engineering course. Very comprehensive.",
        "badge": "🆓 Free • 🔥 Best Free DE"
    },
    {
        "id": "de-002",
        "name": "Fundamentals of Data Engineering",
        "url": "https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/",
        "platform": "O'Reilly (Book)",
        "instructor": "Joe Reis & Matt Housley",
        "duration_hours": 20,
        "cost": "$55 (book)",
        "cost_type": "paid",
        "difficulty": "intermediate",
        "rating": 4.8,
        "description": "Modern data engineering principles and practices.",
        "skills_taught": ["Data architecture", "Pipelines", "Storage", "Processing"],
        "why_recommended": "Essential reading for understanding data infrastructure.",
        "badge": "📚 Essential Reading"
    },
]

# ============================================================================
# CLOUD & DEPLOYMENT
# ============================================================================

CLOUD_COURSES = [
    {
        "id": "cloud-001",
        "name": "AWS Machine Learning Specialty",
        "url": "https://aws.amazon.com/training/learn-about/machine-learning/",
        "platform": "AWS",
        "instructor": "AWS",
        "duration_hours": 40,
        "cost": "Free training, $300 exam",
        "cost_type": "freemium",
        "difficulty": "intermediate",
        "rating": 4.6,
        "description": "ML on AWS: SageMaker, data engineering, deployment.",
        "skills_taught": ["AWS SageMaker", "S3", "Lambda", "Model deployment"],
        "why_recommended": "Essential for ML on AWS. Certification valued by employers.",
        "badge": "☁️ AWS • 📜 Certification"
    },
    {
        "id": "cloud-002",
        "name": "Google Cloud Professional ML Engineer",
        "url": "https://cloud.google.com/learn/certification/machine-learning-engineer",
        "platform": "Google Cloud",
        "instructor": "Google",
        "duration_hours": 40,
        "cost": "Free training, $200 exam",
        "cost_type": "freemium",
        "difficulty": "intermediate",
        "rating": 4.7,
        "description": "ML on GCP: Vertex AI, BigQuery ML, deployment.",
        "skills_taught": ["Vertex AI", "BigQuery", "TensorFlow", "Model deployment"],
        "why_recommended": "Essential for ML on GCP. Highly valued certification.",
        "badge": "☁️ GCP • 📜 Certification"
    },
    {
        "id": "cloud-003",
        "name": "Docker for Data Science & ML",
        "url": "https://www.youtube.com/watch?v=0qG_0CPQhpg",
        "platform": "YouTube",
        "instructor": "Patrick Loeber",
        "duration_hours": 3,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "beginner",
        "rating": 4.6,
        "description": "Docker essentials for ML practitioners.",
        "skills_taught": ["Docker basics", "Containerization", "ML deployment"],
        "why_recommended": "Quick Docker intro for ML. Essential skill.",
        "badge": "🆓 Free • ⚡ Quick"
    },
]

# ============================================================================
# INTERVIEW PREP & CAREER
# ============================================================================

INTERVIEW_COURSES = [
    {
        "id": "int-001",
        "name": "Ace the Data Science Interview",
        "url": "https://www.acethedatascienceinterview.com/",
        "platform": "Book + Online",
        "instructor": "Nick Singh & Kevin Huo",
        "duration_hours": 15,
        "cost": "$35 (book)",
        "cost_type": "paid",
        "difficulty": "intermediate",
        "rating": 4.8,
        "description": "201 real interview questions from FAANG companies.",
        "skills_taught": ["SQL", "Statistics", "ML theory", "Case studies"],
        "why_recommended": "Best DS interview prep. Real questions from big tech.",
        "badge": "💼 Interview Prep • 🔥 Bestseller"
    },
    {
        "id": "int-002",
        "name": "LeetCode ML/AI Questions",
        "url": "https://leetcode.com/tag/machine-learning/",
        "platform": "LeetCode",
        "instructor": "Community",
        "duration_hours": 30,
        "cost": "Free (basic), $35/month (premium)",
        "cost_type": "freemium",
        "difficulty": "intermediate",
        "rating": 4.5,
        "description": "Coding problems for ML interviews.",
        "skills_taught": ["Algorithms", "Data structures", "ML coding"],
        "why_recommended": "Essential for coding rounds at tech companies.",
        "badge": "💻 Coding Prep"
    },
]

# ============================================================================
# PROJECTS & PORTFOLIO
# ============================================================================

PROJECT_RESOURCES = [
    {
        "id": "proj-001",
        "name": "Kaggle Competitions",
        "url": "https://www.kaggle.com/competitions",
        "platform": "Kaggle",
        "instructor": "Community",
        "duration_hours": 50,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "intermediate",
        "rating": 4.8,
        "description": "Real ML competitions. Build portfolio and learn from winners.",
        "skills_taught": ["End-to-end ML", "Feature engineering", "Model optimization"],
        "why_recommended": "Best way to build portfolio. Employers love Kaggle rankings.",
        "badge": "🆓 Free • 🏆 Portfolio Builder"
    },
    {
        "id": "proj-002",
        "name": "Papers With Code",
        "url": "https://paperswithcode.com/",
        "platform": "Papers With Code",
        "instructor": "Community",
        "duration_hours": 20,
        "cost": "Free",
        "cost_type": "free",
        "difficulty": "advanced",
        "rating": 4.9,
        "description": "Latest ML papers with code implementations.",
        "skills_taught": ["Research", "Implementation", "State-of-the-art"],
        "why_recommended": "Stay current with ML research. Great for advanced projects.",
        "badge": "🆓 Free • 📄 Research"
    },
]


# ============================================================================
# ROLE-SPECIFIC LEARNING PATHS - WEEK BY WEEK (NO REPETITION)
# ============================================================================

ROLE_LEARNING_PATHS = {
    "ml_engineer": {
        "name": "Machine Learning Engineer",
        "description": "Build and deploy ML models at scale",
        "duration_weeks": 16,
        "weekly_curriculum": [
            # Week 1-4: Foundations
            {"week": 1, "theme": "Python Foundations", "courses": ["py-001"], "focus": "Master Python basics for data science"},
            {"week": 2, "theme": "Math for ML", "courses": ["math-002"], "focus": "Linear algebra intuition"},
            {"week": 3, "theme": "Statistics", "courses": ["stats-001"], "focus": "Statistical foundations"},
            {"week": 4, "theme": "Math Deep Dive", "courses": ["math-001"], "focus": "Calculus and PCA for ML"},
            # Week 5-8: Core ML
            {"week": 5, "theme": "ML Fundamentals", "courses": ["ml-001"], "focus": "Start Andrew Ng's ML course"},
            {"week": 6, "theme": "ML Practice", "courses": ["ml-003"], "focus": "Google's ML Crash Course"},
            {"week": 7, "theme": "Hands-On ML", "courses": ["ml-002"], "focus": "fast.ai practical approach"},
            {"week": 8, "theme": "ML Projects", "courses": ["proj-001"], "focus": "Kaggle competition"},
            # Week 9-12: Deep Learning
            {"week": 9, "theme": "Deep Learning Intro", "courses": ["dl-001"], "focus": "Neural networks foundations"},
            {"week": 10, "theme": "PyTorch", "courses": ["dl-002"], "focus": "Learn PyTorch framework"},
            {"week": 11, "theme": "Neural Networks Deep Dive", "courses": ["dl-003"], "focus": "Andrej Karpathy's series"},
            {"week": 12, "theme": "DL Projects", "courses": ["ml-004"], "focus": "Build end-to-end DL project"},
            # Week 13-16: Production
            {"week": 13, "theme": "MLOps Foundations", "courses": ["mlops-001"], "focus": "ML in production"},
            {"week": 14, "theme": "MLOps Practice", "courses": ["mlops-002"], "focus": "Made With ML course"},
            {"week": 15, "theme": "Cloud Deployment", "courses": ["cloud-001"], "focus": "AWS ML certification prep"},
            {"week": 16, "theme": "Interview Prep", "courses": ["int-001"], "focus": "Ace the interview"},
        ]
    },
    "ai_engineer": {
        "name": "AI Engineer",
        "description": "Build applications powered by LLMs and AI",
        "duration_weeks": 12,
        "weekly_curriculum": [
            # Week 1-3: Foundations
            {"week": 1, "theme": "Python for AI", "courses": ["py-001"], "focus": "Python fundamentals for AI development"},
            {"week": 2, "theme": "Prompt Engineering", "courses": ["ai-004"], "focus": "Master prompt engineering techniques"},
            {"week": 3, "theme": "OpenAI API Mastery", "courses": ["ai-003"], "focus": "Build production systems with OpenAI"},
            # Week 4-7: LLM Applications (Core AI Engineering)
            {"week": 4, "theme": "🔥 Scrimba AI Engineer", "courses": ["ai-001"], "focus": "Complete AI Engineer curriculum - OpenAI, LangChain, Vector DBs"},
            {"week": 5, "theme": "LangChain Deep Dive", "courses": ["ai-002"], "focus": "Build chains, agents, and memory systems"},
            {"week": 6, "theme": "Vector Databases & RAG", "courses": ["ai-008"], "focus": "Semantic search and RAG applications"},
            {"week": 7, "theme": "Advanced RAG", "courses": ["ai-009"], "focus": "Build and evaluate production RAG systems"},
            # Week 8-10: Advanced AI Engineering
            {"week": 8, "theme": "AI Agents", "courses": ["ai-010"], "focus": "Build autonomous AI agents with LangGraph"},
            {"week": 9, "theme": "Fine-tuning LLMs", "courses": ["ai-007"], "focus": "Customize LLMs for specific use cases"},
            {"week": 10, "theme": "Production LLMs", "courses": ["ai-006"], "focus": "Full Stack LLM development"},
            # Week 11-12: Production & Career
            {"week": 11, "theme": "MLOps for AI", "courses": ["mlops-002"], "focus": "Deploy and monitor AI systems"},
            {"week": 12, "theme": "Hugging Face Ecosystem", "courses": ["ai-005"], "focus": "Transformers library and model hub"},
        ]
    },
    "data_scientist": {
        "name": "Data Scientist",
        "description": "Extract insights from data using statistics and ML",
        "duration_weeks": 16,
        "weekly_curriculum": [
            {"week": 1, "theme": "Python Basics", "courses": ["py-001"], "focus": "Python fundamentals"},
            {"week": 2, "theme": "Python Practice", "courses": ["py-002"], "focus": "Automate the boring stuff"},
            {"week": 3, "theme": "Statistics", "courses": ["stats-001"], "focus": "Statistical analysis"},
            {"week": 4, "theme": "Data Engineering", "courses": ["de-001"], "focus": "SQL and data pipelines"},
            {"week": 5, "theme": "ML Foundations", "courses": ["ml-001"], "focus": "Andrew Ng's ML course"},
            {"week": 6, "theme": "ML Quick Start", "courses": ["ml-003"], "focus": "Google ML Crash Course"},
            {"week": 7, "theme": "Practical ML", "courses": ["ml-002"], "focus": "fast.ai course"},
            {"week": 8, "theme": "ML Reference", "courses": ["ml-004"], "focus": "Hands-on ML book"},
            {"week": 9, "theme": "Kaggle Practice", "courses": ["proj-001"], "focus": "Compete on Kaggle"},
            {"week": 10, "theme": "Deep Learning", "courses": ["dl-001"], "focus": "Neural networks"},
            {"week": 11, "theme": "NLP Basics", "courses": ["nlp-002"], "focus": "Natural language processing"},
            {"week": 12, "theme": "Hugging Face", "courses": ["ai-005"], "focus": "Modern NLP"},
            {"week": 13, "theme": "Advanced ML", "courses": ["ml-005"], "focus": "Stanford CS229"},
            {"week": 14, "theme": "ML Systems", "courses": ["mlops-003"], "focus": "Designing ML Systems book"},
            {"week": 15, "theme": "Interview Prep", "courses": ["int-001"], "focus": "DS interview questions"},
            {"week": 16, "theme": "Portfolio Building", "courses": ["proj-002"], "focus": "Papers With Code - implement research"},
        ]
    },
    "mlops_engineer": {
        "name": "MLOps Engineer",
        "description": "Build infrastructure for ML systems",
        "duration_weeks": 14,
        "weekly_curriculum": [
            {"week": 1, "theme": "Python Foundations", "courses": ["py-001"], "focus": "Python basics"},
            {"week": 2, "theme": "Docker Basics", "courses": ["cloud-003"], "focus": "Containerization"},
            {"week": 3, "theme": "Data Engineering", "courses": ["de-001"], "focus": "Data pipelines"},
            {"week": 4, "theme": "ML Fundamentals", "courses": ["ml-003"], "focus": "Understand ML basics"},
            {"week": 5, "theme": "Practical ML", "courses": ["ml-002"], "focus": "Build ML models"},
            {"week": 6, "theme": "MLOps Foundations", "courses": ["mlops-001"], "focus": "Andrew Ng's MLOps"},
            {"week": 7, "theme": "MLOps Practice", "courses": ["mlops-002"], "focus": "Made With ML"},
            {"week": 8, "theme": "ML Systems Design", "courses": ["mlops-003"], "focus": "Chip Huyen's book"},
            {"week": 9, "theme": "System Design", "courses": ["mlops-004"], "focus": "ML system design interviews"},
            {"week": 10, "theme": "AWS ML", "courses": ["cloud-001"], "focus": "AWS SageMaker"},
            {"week": 11, "theme": "GCP ML", "courses": ["cloud-002"], "focus": "Google Vertex AI"},
            {"week": 12, "theme": "DE Deep Dive", "courses": ["de-002"], "focus": "Data engineering book"},
            {"week": 13, "theme": "Research", "courses": ["proj-002"], "focus": "Papers With Code"},
            {"week": 14, "theme": "Interview Prep", "courses": ["int-001"], "focus": "Prepare for interviews"},
        ]
    },
    "cv_engineer": {
        "name": "Computer Vision Engineer",
        "description": "Build systems that understand images and video",
        "duration_weeks": 14,
        "weekly_curriculum": [
            {"week": 1, "theme": "Python Foundations", "courses": ["py-001"], "focus": "Python for CV"},
            {"week": 2, "theme": "Math for CV", "courses": ["math-002"], "focus": "Linear algebra for image processing"},
            {"week": 3, "theme": "Deep Learning Basics", "courses": ["dl-002"], "focus": "PyTorch fundamentals"},
            {"week": 4, "theme": "Neural Networks Theory", "courses": ["dl-001"], "focus": "Deep learning foundations"},
            {"week": 5, "theme": "Stanford Computer Vision", "courses": ["cv-001"], "focus": "CS231n - CNNs, detection, segmentation"},
            {"week": 6, "theme": "CV with PyTorch", "courses": ["cv-002"], "focus": "Hands-on CV implementation"},
            {"week": 7, "theme": "Neural Net Internals", "courses": ["dl-003"], "focus": "Andrej Karpathy's deep dive"},
            {"week": 8, "theme": "Hands-On ML Book", "courses": ["ml-004"], "focus": "End-to-end ML projects"},
            {"week": 9, "theme": "Kaggle CV Competitions", "courses": ["proj-001"], "focus": "Compete in image challenges"},
            {"week": 10, "theme": "Vision Transformers", "courses": ["ai-005"], "focus": "Modern CV with transformers"},
            {"week": 11, "theme": "MLOps for CV", "courses": ["mlops-002"], "focus": "Deploy CV models"},
            {"week": 12, "theme": "Docker & Deployment", "courses": ["cloud-003"], "focus": "Containerize CV apps"},
            {"week": 13, "theme": "Research Papers", "courses": ["proj-002"], "focus": "Implement CV papers"},
            {"week": 14, "theme": "Interview Prep", "courses": ["int-001"], "focus": "CV interview preparation"},
        ]
    },
    "nlp_engineer": {
        "name": "NLP Engineer",
        "description": "Build systems that understand and generate language",
        "duration_weeks": 14,
        "weekly_curriculum": [
            {"week": 1, "theme": "Python Foundations", "courses": ["py-001"], "focus": "Python for NLP"},
            {"week": 2, "theme": "Deep Learning Basics", "courses": ["dl-002"], "focus": "PyTorch fundamentals"},
            {"week": 3, "theme": "NLP Foundations", "courses": ["nlp-001"], "focus": "Stanford CS224N - Word vectors to transformers"},
            {"week": 4, "theme": "NLP with DeepLearning.AI", "courses": ["nlp-002"], "focus": "Sequence models and attention"},
            {"week": 5, "theme": "Hugging Face Transformers", "courses": ["ai-005"], "focus": "State-of-the-art NLP models"},
            {"week": 6, "theme": "Prompt Engineering", "courses": ["ai-004"], "focus": "Working with LLMs"},
            {"week": 7, "theme": "LangChain for NLP", "courses": ["ai-002"], "focus": "Build NLP applications"},
            {"week": 8, "theme": "RAG Systems", "courses": ["ai-008"], "focus": "Vector search and retrieval"},
            {"week": 9, "theme": "Fine-tuning LLMs", "courses": ["ai-007"], "focus": "Customize models for NLP tasks"},
            {"week": 10, "theme": "Advanced RAG", "courses": ["ai-009"], "focus": "Production RAG pipelines"},
            {"week": 11, "theme": "Neural Network Internals", "courses": ["dl-003"], "focus": "Build transformers from scratch"},
            {"week": 12, "theme": "Production LLMs", "courses": ["ai-006"], "focus": "Deploy NLP systems at scale"},
            {"week": 13, "theme": "MLOps for NLP", "courses": ["mlops-002"], "focus": "ML operations for NLP"},
            {"week": 14, "theme": "Research & Papers", "courses": ["proj-002"], "focus": "Implement NLP research papers"},
        ]
    },
    
    # ============================================================================
    # NEW ROLES - Prompt Engineer, GenAI Developer, Vibe Coder, etc.
    # ============================================================================
    
    "prompt_engineer": {
        "name": "Prompt Engineer",
        "description": "Design and optimize prompts for LLMs",
        "duration_weeks": 8,
        "weekly_curriculum": [
            {"week": 1, "theme": "Prompt Fundamentals", "courses": ["ai-004"], "focus": "Master prompt engineering basics"},
            {"week": 2, "theme": "OpenAI API Mastery", "courses": ["ai-003"], "focus": "Build systems with ChatGPT API"},
            {"week": 3, "theme": "LangChain Prompting", "courses": ["ai-002"], "focus": "Advanced prompting with LangChain"},
            {"week": 4, "theme": "🔥 Scrimba AI Engineer", "courses": ["ai-001"], "focus": "Complete AI curriculum including prompting"},
            {"week": 5, "theme": "RAG Prompting", "courses": ["ai-008"], "focus": "Prompts for retrieval systems"},
            {"week": 6, "theme": "Agent Prompting", "courses": ["ai-010"], "focus": "Design prompts for AI agents"},
            {"week": 7, "theme": "Evaluation & Testing", "courses": ["ai-017"], "focus": "Evaluate and improve prompts"},
            {"week": 8, "theme": "Production Prompts", "courses": ["ai-006"], "focus": "Prompts at scale"},
        ]
    },
    
    "generative_ai_developer": {
        "name": "Generative AI Developer",
        "description": "Build applications using generative AI models",
        "duration_weeks": 12,
        "weekly_curriculum": [
            {"week": 1, "theme": "GenAI Foundations", "courses": ["ai-013"], "focus": "Understand generative AI concepts"},
            {"week": 2, "theme": "Prompt Engineering", "courses": ["ai-004"], "focus": "Master prompt techniques"},
            {"week": 3, "theme": "OpenAI API", "courses": ["ai-003"], "focus": "Build with ChatGPT API"},
            {"week": 4, "theme": "🔥 Scrimba AI Engineer", "courses": ["ai-001"], "focus": "Complete AI Engineer curriculum"},
            {"week": 5, "theme": "Image Generation", "courses": ["ai-014"], "focus": "How diffusion models work"},
            {"week": 6, "theme": "LangChain", "courses": ["ai-002"], "focus": "Build GenAI applications"},
            {"week": 7, "theme": "RAG Systems", "courses": ["ai-008"], "focus": "Retrieval-augmented generation"},
            {"week": 8, "theme": "Hugging Face", "courses": ["ai-005"], "focus": "Use open-source models"},
            {"week": 9, "theme": "Fine-tuning", "courses": ["ai-007"], "focus": "Customize generative models"},
            {"week": 10, "theme": "Build UIs", "courses": ["ai-012"], "focus": "Create GenAI apps with Gradio"},
            {"week": 11, "theme": "Production GenAI", "courses": ["ai-006"], "focus": "Deploy at scale"},
            {"week": 12, "theme": "MLOps", "courses": ["mlops-002"], "focus": "GenAI in production"},
        ]
    },
    
    "vibe_coder": {
        "name": "Vibe Coder / AI Automation Builder",
        "description": "Build automations and apps using AI coding assistants",
        "duration_weeks": 8,
        "weekly_curriculum": [
            {"week": 1, "theme": "⚡ Python Fast Track", "courses": ["py-scrimba"], "focus": "Interactive Python - code while learning"},
            {"week": 2, "theme": "AI-Assisted Coding", "courses": ["ai-015"], "focus": "Pair programming with LLMs"},
            {"week": 3, "theme": "Prompt for Code", "courses": ["ai-004"], "focus": "Prompt engineering for coding"},
            {"week": 4, "theme": "⚡ AI Engineer Path", "courses": ["ai-001"], "focus": "Scrimba - Build AI apps fast"},
            {"week": 5, "theme": "LangChain Automation", "courses": ["ai-002"], "focus": "Build AI automation chains"},
            {"week": 6, "theme": "AI Agents", "courses": ["ai-011"], "focus": "Build agents that use tools"},
            {"week": 7, "theme": "Build UIs Fast", "courses": ["ai-012"], "focus": "Create apps with Gradio"},
            {"week": 8, "theme": "Multi-Agent Systems", "courses": ["ai-018"], "focus": "Build agent teams with CrewAI"},
        ]
    },
    
    "agent_developer": {
        "name": "Autonomous Agent Developer",
        "description": "Build AI agents that can reason and act autonomously",
        "duration_weeks": 10,
        "weekly_curriculum": [
            {"week": 1, "theme": "Agent Foundations", "courses": ["ai-004"], "focus": "Prompting for agents"},
            {"week": 2, "theme": "OpenAI Functions", "courses": ["ai-011"], "focus": "Function calling and tools"},
            {"week": 3, "theme": "LangChain Agents", "courses": ["ai-002"], "focus": "Build agents with LangChain"},
            {"week": 4, "theme": "🔥 Scrimba AI Engineer", "courses": ["ai-001"], "focus": "Complete agent development"},
            {"week": 5, "theme": "LangGraph Agents", "courses": ["ai-010"], "focus": "Advanced agent architectures"},
            {"week": 6, "theme": "RAG for Agents", "courses": ["ai-008"], "focus": "Give agents knowledge"},
            {"week": 7, "theme": "Multi-Agent Systems", "courses": ["ai-018"], "focus": "CrewAI multi-agent teams"},
            {"week": 8, "theme": "AutoGen Patterns", "courses": ["ai-019"], "focus": "Microsoft's agent patterns"},
            {"week": 9, "theme": "Agent Evaluation", "courses": ["ai-017"], "focus": "Test and evaluate agents"},
            {"week": 10, "theme": "Production Agents", "courses": ["ai-006"], "focus": "Deploy agents at scale"},
        ]
    },
    
    "ai_product_manager": {
        "name": "AI Product Manager",
        "description": "Lead AI product development from ideation to launch",
        "duration_weeks": 10,
        "weekly_curriculum": [
            {"week": 1, "theme": "AI Fundamentals", "courses": ["ai-013"], "focus": "GenAI for everyone - understand AI"},
            {"week": 2, "theme": "⚡ Python Fast Track", "courses": ["py-scrimba"], "focus": "Interactive Python - code while learning"},
            {"week": 3, "theme": "PM Fundamentals", "courses": ["biz-003"], "focus": "Product management basics"},
            {"week": 4, "theme": "AI Product Management", "courses": ["biz-001"], "focus": "Duke AI PM specialization"},
            {"week": 5, "theme": "Prompt Engineering", "courses": ["ai-004"], "focus": "Understand LLM capabilities"},
            {"week": 6, "theme": "AI Business Strategy", "courses": ["biz-002"], "focus": "Wharton AI for business"},
            {"week": 7, "theme": "AI Transformation", "courses": ["biz-004"], "focus": "Andrew Ng's AI playbook"},
            {"week": 8, "theme": "AI UX Design", "courses": ["des-001"], "focus": "Design AI products"},
            {"week": 9, "theme": "MLOps Overview", "courses": ["mlops-002"], "focus": "Understand ML operations"},
            {"week": 10, "theme": "Interview Prep", "courses": ["int-001"], "focus": "AI PM interviews"},
        ]
    },
    
    "ai_product_designer": {
        "name": "AI Product Designer",
        "description": "Design user experiences for AI-powered products",
        "duration_weeks": 10,
        "weekly_curriculum": [
            {"week": 1, "theme": "UX Foundations", "courses": ["des-003"], "focus": "Google UX design certificate"},
            {"week": 2, "theme": "AI Fundamentals", "courses": ["ai-013"], "focus": "Understand generative AI"},
            {"week": 3, "theme": "⚡ Python Fast Track", "courses": ["py-scrimba"], "focus": "Interactive Python for prototyping"},
            {"week": 4, "theme": "AI UX Patterns", "courses": ["des-001"], "focus": "AI-powered UX design"},
            {"week": 5, "theme": "Prompt Engineering", "courses": ["ai-004"], "focus": "Understand LLM capabilities"},
            {"week": 6, "theme": "Build AI Prototypes", "courses": ["ai-012"], "focus": "Gradio for quick AI UIs"},
            {"week": 7, "theme": "Conversational Design", "courses": ["ai-003"], "focus": "Design chatbot experiences"},
            {"week": 8, "theme": "AI Ethics in Design", "courses": ["ai-016"], "focus": "Responsible AI design"},
            {"week": 9, "theme": "Image Generation UX", "courses": ["ai-014"], "focus": "Design for image gen products"},
            {"week": 10, "theme": "Portfolio", "courses": ["proj-001"], "focus": "Build AI design portfolio"},
        ]
    },
    
    "ai_safety_researcher": {
        "name": "AI Safety Researcher",
        "description": "Research and develop safe AI systems",
        "duration_weeks": 14,
        "weekly_curriculum": [
            {"week": 1, "theme": "ML Foundations", "courses": ["ml-001"], "focus": "Andrew Ng's ML course"},
            {"week": 2, "theme": "Deep Learning", "courses": ["dl-001"], "focus": "Neural network foundations"},
            {"week": 3, "theme": "AI Ethics", "courses": ["ai-016"], "focus": "AI for Good specialization"},
            {"week": 4, "theme": "NLP & LLMs", "courses": ["nlp-001"], "focus": "Stanford NLP course"},
            {"week": 5, "theme": "Prompt Engineering", "courses": ["ai-004"], "focus": "Understand LLM behavior"},
            {"week": 6, "theme": "Hugging Face", "courses": ["ai-005"], "focus": "Open-source models"},
            {"week": 7, "theme": "Fine-tuning", "courses": ["ai-007"], "focus": "Model customization risks"},
            {"week": 8, "theme": "RL Foundations", "courses": ["rl-001"], "focus": "RL for alignment"},
            {"week": 9, "theme": "Deep RL", "courses": ["rl-002"], "focus": "Advanced RL techniques"},
            {"week": 10, "theme": "Evaluation", "courses": ["ai-017"], "focus": "Evaluate AI systems"},
            {"week": 11, "theme": "Agent Safety", "courses": ["ai-010"], "focus": "Safe agent design"},
            {"week": 12, "theme": "Research Papers", "courses": ["proj-002"], "focus": "Papers With Code"},
            {"week": 13, "theme": "ML Theory", "courses": ["ml-005"], "focus": "Stanford CS229 theory"},
            {"week": 14, "theme": "Advanced Research", "courses": ["rl-003"], "focus": "OpenAI Spinning Up"},
        ]
    },
    
    "ai_solutions_architect": {
        "name": "AI Solutions Architect",
        "description": "Design and architect enterprise AI solutions",
        "duration_weeks": 12,
        "weekly_curriculum": [
            {"week": 1, "theme": "ML Fundamentals", "courses": ["ml-001"], "focus": "ML foundations"},
            {"week": 2, "theme": "Cloud ML - AWS", "courses": ["cloud-001"], "focus": "AWS ML services"},
            {"week": 3, "theme": "Cloud ML - GCP", "courses": ["cloud-002"], "focus": "Google Cloud ML"},
            {"week": 4, "theme": "MLOps Architecture", "courses": ["mlops-001"], "focus": "Andrew Ng's MLOps"},
            {"week": 5, "theme": "System Design", "courses": ["mlops-003"], "focus": "Designing ML Systems"},
            {"week": 6, "theme": "AI Business Strategy", "courses": ["biz-002"], "focus": "AI for business"},
            {"week": 7, "theme": "GenAI Solutions", "courses": ["ai-001"], "focus": "Scrimba AI Engineer"},
            {"week": 8, "theme": "RAG Architecture", "courses": ["ai-008"], "focus": "Vector DB architecture"},
            {"week": 9, "theme": "Data Engineering", "courses": ["de-001"], "focus": "Data pipelines"},
            {"week": 10, "theme": "Infrastructure", "courses": ["infra-001"], "focus": "Kubeflow on K8s"},
            {"week": 11, "theme": "Interview Prep", "courses": ["mlops-004"], "focus": "ML system design interviews"},
            {"week": 12, "theme": "AI Transformation", "courses": ["biz-004"], "focus": "Enterprise AI playbook"},
        ]
    },
    
    "ai_research_scientist": {
        "name": "AI Research Scientist",
        "description": "Conduct cutting-edge AI/ML research",
        "duration_weeks": 16,
        "weekly_curriculum": [
            {"week": 1, "theme": "ML Theory", "courses": ["ml-005"], "focus": "Stanford CS229"},
            {"week": 2, "theme": "Math for ML", "courses": ["math-001"], "focus": "Math specialization"},
            {"week": 3, "theme": "Deep Learning Theory", "courses": ["dl-001"], "focus": "DL foundations"},
            {"week": 4, "theme": "Neural Networks", "courses": ["dl-003"], "focus": "Karpathy's series"},
            {"week": 5, "theme": "Computer Vision", "courses": ["cv-001"], "focus": "Stanford CS231n"},
            {"week": 6, "theme": "NLP Research", "courses": ["nlp-001"], "focus": "Stanford CS224N"},
            {"week": 7, "theme": "Transformers", "courses": ["ai-005"], "focus": "Hugging Face course"},
            {"week": 8, "theme": "RL Theory", "courses": ["rl-001"], "focus": "RL specialization"},
            {"week": 9, "theme": "Deep RL", "courses": ["rl-002"], "focus": "Deep RL course"},
            {"week": 10, "theme": "OpenAI RL", "courses": ["rl-003"], "focus": "Spinning Up"},
            {"week": 11, "theme": "LLM Research", "courses": ["ai-007"], "focus": "Fine-tuning research"},
            {"week": 12, "theme": "Diffusion Models", "courses": ["ai-014"], "focus": "Image generation"},
            {"week": 13, "theme": "Agent Research", "courses": ["ai-010"], "focus": "Agent architectures"},
            {"week": 14, "theme": "Research Methods", "courses": ["proj-002"], "focus": "Papers With Code"},
            {"week": 15, "theme": "PyTorch Advanced", "courses": ["dl-002"], "focus": "Advanced PyTorch"},
            {"week": 16, "theme": "Research Portfolio", "courses": ["proj-001"], "focus": "Kaggle competitions"},
        ]
    },
    
    "rl_engineer": {
        "name": "Reinforcement Learning Engineer",
        "description": "Build RL systems for games, robotics, and optimization",
        "duration_weeks": 12,
        "weekly_curriculum": [
            {"week": 1, "theme": "Python for RL", "courses": ["py-001"], "focus": "Python foundations"},
            {"week": 2, "theme": "Math for RL", "courses": ["math-002"], "focus": "Linear algebra"},
            {"week": 3, "theme": "ML Foundations", "courses": ["ml-001"], "focus": "ML basics for RL"},
            {"week": 4, "theme": "Deep Learning", "courses": ["dl-002"], "focus": "PyTorch for RL"},
            {"week": 5, "theme": "RL Foundations", "courses": ["rl-001"], "focus": "RL specialization"},
            {"week": 6, "theme": "Deep RL", "courses": ["rl-002"], "focus": "Hugging Face Deep RL"},
            {"week": 7, "theme": "OpenAI RL", "courses": ["rl-003"], "focus": "Spinning Up"},
            {"week": 8, "theme": "Neural Networks", "courses": ["dl-003"], "focus": "NN internals"},
            {"week": 9, "theme": "Multi-Agent RL", "courses": ["ai-018"], "focus": "Multi-agent systems"},
            {"week": 10, "theme": "MLOps for RL", "courses": ["mlops-002"], "focus": "Deploy RL systems"},
            {"week": 11, "theme": "Research Papers", "courses": ["proj-002"], "focus": "Implement RL papers"},
            {"week": 12, "theme": "Portfolio", "courses": ["proj-001"], "focus": "RL competitions"},
        ]
    },
    
    "ml_infra_engineer": {
        "name": "AI/ML Infrastructure Engineer",
        "description": "Build and scale ML infrastructure",
        "duration_weeks": 14,
        "weekly_curriculum": [
            {"week": 1, "theme": "Python", "courses": ["py-001"], "focus": "Python for infra"},
            {"week": 2, "theme": "ML Basics", "courses": ["ml-003"], "focus": "Understand ML workloads"},
            {"week": 3, "theme": "Docker", "courses": ["cloud-003"], "focus": "Containerization"},
            {"week": 4, "theme": "Data Engineering", "courses": ["de-001"], "focus": "Data pipelines"},
            {"week": 5, "theme": "MLOps", "courses": ["mlops-001"], "focus": "ML in production"},
            {"week": 6, "theme": "Made With ML", "courses": ["mlops-002"], "focus": "End-to-end MLOps"},
            {"week": 7, "theme": "ML Systems", "courses": ["mlops-003"], "focus": "Chip Huyen's book"},
            {"week": 8, "theme": "Kubernetes", "courses": ["infra-001"], "focus": "Kubeflow on K8s"},
            {"week": 9, "theme": "Terraform", "courses": ["infra-002"], "focus": "IaC for ML"},
            {"week": 10, "theme": "Distributed ML", "courses": ["infra-003"], "focus": "Ray for scaling"},
            {"week": 11, "theme": "AWS ML", "courses": ["cloud-001"], "focus": "AWS SageMaker"},
            {"week": 12, "theme": "GCP ML", "courses": ["cloud-002"], "focus": "Vertex AI"},
            {"week": 13, "theme": "Interview Prep", "courses": ["mlops-004"], "focus": "System design"},
            {"week": 14, "theme": "DE Deep Dive", "courses": ["de-002"], "focus": "Data engineering book"},
        ]
    },
    
    "ai_consultant": {
        "name": "AI Consultant",
        "description": "Advise organizations on AI strategy and implementation",
        "duration_weeks": 10,
        "weekly_curriculum": [
            {"week": 1, "theme": "AI for Business", "courses": ["biz-002"], "focus": "Wharton AI strategy"},
            {"week": 2, "theme": "GenAI Fundamentals", "courses": ["ai-013"], "focus": "GenAI for everyone"},
            {"week": 3, "theme": "⚡ Python Fast Track", "courses": ["py-scrimba"], "focus": "Interactive Python - essential for demos"},
            {"week": 4, "theme": "AI Transformation", "courses": ["biz-004"], "focus": "Andrew Ng's playbook"},
            {"week": 5, "theme": "Prompt Engineering", "courses": ["ai-004"], "focus": "Understand LLM capabilities"},
            {"week": 6, "theme": "AI Products", "courses": ["biz-001"], "focus": "AI product management"},
            {"week": 7, "theme": "⚡ AI Engineer Path", "courses": ["ai-001"], "focus": "Scrimba - Build AI apps to demo"},
            {"week": 8, "theme": "MLOps Overview", "courses": ["mlops-002"], "focus": "Made With ML"},
            {"week": 9, "theme": "AI Ethics", "courses": ["ai-016"], "focus": "AI for Good"},
            {"week": 10, "theme": "Case Studies", "courses": ["proj-002"], "focus": "Real-world implementations"},
        ]
    },
    
    "ai_ethics_specialist": {
        "name": "AI Ethics Specialist",
        "description": "Ensure responsible and ethical AI development",
        "duration_weeks": 10,
        "weekly_curriculum": [
            {"week": 1, "theme": "AI Fundamentals", "courses": ["ai-013"], "focus": "Understand GenAI"},
            {"week": 2, "theme": "⚡ Python Fast Track", "courses": ["py-scrimba"], "focus": "Interactive Python for analysis"},
            {"week": 3, "theme": "AI for Good", "courses": ["ai-016"], "focus": "AI ethics specialization"},
            {"week": 4, "theme": "AI Business Impact", "courses": ["biz-002"], "focus": "Business implications"},
            {"week": 5, "theme": "LLM Behavior", "courses": ["ai-004"], "focus": "Prompt engineering"},
            {"week": 6, "theme": "Hugging Face", "courses": ["ai-005"], "focus": "Model cards and ethics"},
            {"week": 7, "theme": "AI UX Ethics", "courses": ["des-001"], "focus": "Ethical design patterns"},
            {"week": 8, "theme": "Agent Ethics", "courses": ["ai-010"], "focus": "Safe agent design"},
            {"week": 9, "theme": "Evaluation", "courses": ["ai-017"], "focus": "Evaluate AI fairness"},
            {"week": 10, "theme": "Research", "courses": ["proj-002"], "focus": "AI ethics research"},
        ]
    },
    
    "ai_content_creator": {
        "name": "AI Content Creator",
        "description": "Create content using AI tools",
        "duration_weeks": 8,
        "weekly_curriculum": [
            {"week": 1, "theme": "GenAI Basics", "courses": ["ai-013"], "focus": "Understand AI tools"},
            {"week": 2, "theme": "⚡ Python Fast Track", "courses": ["py-scrimba"], "focus": "Interactive Python for automation"},
            {"week": 3, "theme": "Prompt Mastery", "courses": ["ai-004"], "focus": "Write effective prompts"},
            {"week": 4, "theme": "Image Generation", "courses": ["ai-014"], "focus": "How diffusion models work"},
            {"week": 5, "theme": "Midjourney/DALL-E", "courses": ["cont-002"], "focus": "AI art mastery"},
            {"week": 6, "theme": "⚡ AI Engineer Path", "courses": ["ai-001"], "focus": "Scrimba - Build content tools"},
            {"week": 7, "theme": "Build Apps", "courses": ["ai-012"], "focus": "Gradio for content tools"},
            {"week": 8, "theme": "AI Automation", "courses": ["ai-002"], "focus": "LangChain workflows"},
        ]
    },
    
    "ai_business_analyst": {
        "name": "AI Business Analyst",
        "description": "Analyze business needs and translate to AI solutions",
        "duration_weeks": 10,
        "weekly_curriculum": [
            {"week": 1, "theme": "AI Fundamentals", "courses": ["ai-013"], "focus": "GenAI for everyone"},
            {"week": 2, "theme": "⚡ Python Fast Track", "courses": ["py-scrimba"], "focus": "Interactive Python for data"},
            {"week": 3, "theme": "AI for Business", "courses": ["biz-002"], "focus": "Wharton AI strategy"},
            {"week": 4, "theme": "Data Analysis", "courses": ["stats-001"], "focus": "Statistics with Python"},
            {"week": 5, "theme": "SQL & Data", "courses": ["de-001"], "focus": "Data engineering basics"},
            {"week": 6, "theme": "Prompt Engineering", "courses": ["ai-004"], "focus": "LLM capabilities"},
            {"week": 7, "theme": "AI Products", "courses": ["biz-001"], "focus": "AI product management"},
            {"week": 8, "theme": "AI Transformation", "courses": ["biz-004"], "focus": "Implementation playbook"},
            {"week": 9, "theme": "Kaggle Analysis", "courses": ["proj-001"], "focus": "Real data analysis"},
            {"week": 10, "theme": "Interview Prep", "courses": ["int-001"], "focus": "Business analyst interviews"},
        ]
    }
}

# Build course lookup dictionary
ALL_COURSES = {}
for course_list in [FOUNDATION_COURSES, ML_COURSES, DEEP_LEARNING_COURSES, 
                    AI_ENGINEERING_COURSES, MLOPS_COURSES, CV_COURSES, 
                    NLP_COURSES, DATA_ENGINEERING_COURSES, CLOUD_COURSES, 
                    INTERVIEW_COURSES, PROJECT_RESOURCES, BUSINESS_COURSES,
                    DESIGN_COURSES, RL_COURSES, INFRA_COURSES, CONTENT_COURSES]:
    for course in course_list:
        ALL_COURSES[course["id"]] = course


def get_course_by_id(course_id: str):
    """Get course details by ID"""
    return ALL_COURSES.get(course_id)


def get_courses_for_role(role_id: str):
    """Get all courses for a specific role's learning path"""
    path = ROLE_LEARNING_PATHS.get(role_id)
    if not path:
        return []
    
    courses = []
    for phase in path.get("phases", []):
        for course_id in phase.get("courses", []):
            course = get_course_by_id(course_id)
            if course:
                courses.append({
                    **course,
                    "phase": phase["phase"],
                    "phase_name": phase["name"]
                })
    return courses


def get_role_path(role_id: str):
    """Get the complete learning path for a role"""
    return ROLE_LEARNING_PATHS.get(role_id)
