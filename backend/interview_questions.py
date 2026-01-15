"""
Comprehensive Interview Question Bank for AI Roles - EXPANDED VERSION
500+ Interview Questions from top AI companies and role-specific preparation.
"""

# ============================================
# ROLE-SPECIFIC QUESTION BANKS (21 ROLES)
# ============================================

ROLE_QUESTIONS = {
    # ============================================
    # MACHINE LEARNING ENGINEER - 60+ Questions
    # ============================================
    "ml_engineer": {
        "technical": [
            {"question": "Explain the bias-variance tradeoff. How do you diagnose and address each?", "difficulty": "medium", "hint": "High bias = underfitting, high variance = overfitting. Use learning curves.", "frequency": "very_high"},
            {"question": "What's the difference between L1 and L2 regularization? When would you use each?", "difficulty": "medium", "hint": "L1 creates sparsity (feature selection), L2 shrinks weights uniformly.", "frequency": "very_high"},
            {"question": "How would you handle class imbalance in a classification problem?", "difficulty": "medium", "hint": "SMOTE, class weights, threshold tuning, stratified sampling, focal loss.", "frequency": "very_high"},
            {"question": "Explain gradient descent and its variants (batch, SGD, mini-batch, Adam).", "difficulty": "easy", "hint": "Trade-offs: convergence speed, memory, noise for escaping local minima.", "frequency": "very_high"},
            {"question": "What's the curse of dimensionality and how do you address it?", "difficulty": "hard", "hint": "Data becomes sparse in high dimensions. Use PCA, feature selection, embeddings.", "frequency": "high"},
            {"question": "Explain backpropagation step by step.", "difficulty": "medium", "hint": "Chain rule to compute gradients, propagate error from output to input.", "frequency": "very_high"},
            {"question": "What are the differences between bagging and boosting?", "difficulty": "medium", "hint": "Bagging reduces variance (Random Forest), boosting reduces bias (XGBoost).", "frequency": "high"},
            {"question": "How do you prevent overfitting? Name at least 5 techniques.", "difficulty": "medium", "hint": "Regularization, dropout, early stopping, data augmentation, cross-validation.", "frequency": "very_high"},
            {"question": "Explain the ROC curve and AUC. When is accuracy not a good metric?", "difficulty": "medium", "hint": "ROC plots TPR vs FPR. Accuracy fails with imbalanced data.", "frequency": "high"},
            {"question": "What's the difference between generative and discriminative models?", "difficulty": "medium", "hint": "Generative learns P(X,Y), discriminative learns P(Y|X) directly.", "frequency": "high"},
            {"question": "Explain how Random Forest works. What are its hyperparameters?", "difficulty": "easy", "hint": "Ensemble of decision trees with bagging. Key params: n_estimators, max_depth.", "frequency": "high"},
            {"question": "What is XGBoost and why is it so effective?", "difficulty": "medium", "hint": "Gradient boosting with regularization, parallel processing, handling missing values.", "frequency": "high"},
            {"question": "Explain cross-validation. Why use k-fold over train-test split?", "difficulty": "easy", "hint": "K-fold gives more robust estimate, uses all data for both train and validation.", "frequency": "very_high"},
            {"question": "What's the difference between precision and recall? When do you optimize for each?", "difficulty": "easy", "hint": "Precision: of predicted positives, how many correct. Recall: of actual positives, how many found.", "frequency": "very_high"},
            {"question": "Explain feature engineering. What techniques do you use?", "difficulty": "medium", "hint": "Binning, one-hot encoding, feature crossing, polynomial features, embeddings.", "frequency": "high"},
            {"question": "How does dropout work and why does it help prevent overfitting?", "difficulty": "medium", "hint": "Randomly zeros neurons during training, creates ensemble effect.", "frequency": "high"},
            {"question": "Explain the difference between batch normalization and layer normalization.", "difficulty": "hard", "hint": "BatchNorm: across batch. LayerNorm: across features. Different use cases.", "frequency": "high"},
            {"question": "What is the kernel trick in SVM?", "difficulty": "hard", "hint": "Maps data to higher dimension without explicit computation.", "frequency": "medium"},
            {"question": "How do you handle missing values in your dataset?", "difficulty": "easy", "hint": "Deletion, imputation (mean/median/mode), indicator variable, model-based.", "frequency": "very_high"},
            {"question": "Explain the difference between Type I and Type II errors.", "difficulty": "easy", "hint": "Type I: false positive. Type II: false negative.", "frequency": "high"},
            {"question": "What is the central limit theorem and why is it important for ML?", "difficulty": "medium", "hint": "Sample means are normally distributed. Enables statistical inference.", "frequency": "medium"},
            {"question": "How do you choose the right evaluation metric for your problem?", "difficulty": "medium", "hint": "Depends on business goal, class balance, cost of errors.", "frequency": "high"},
            {"question": "Explain ensemble methods. Why do they often outperform single models?", "difficulty": "medium", "hint": "Combine multiple models to reduce variance/bias, improve robustness.", "frequency": "high"},
            {"question": "What is feature importance and how do you calculate it?", "difficulty": "medium", "hint": "Permutation importance, Gini importance, SHAP values.", "frequency": "high"},
            {"question": "Explain the difference between parametric and non-parametric models.", "difficulty": "medium", "hint": "Parametric: fixed params. Non-parametric: complexity grows with data.", "frequency": "medium"},
        ],
        "behavioral": [
            {"question": "Tell me about a time when your ML model didn't perform as expected in production. How did you debug it?", "difficulty": "medium", "hint": "Use STAR format. Mention data drift, feature changes, or distribution shift.", "frequency": "very_high"},
            {"question": "Describe a situation where you had to explain complex ML concepts to non-technical stakeholders.", "difficulty": "easy", "hint": "Focus on analogies and business impact, not technical details.", "frequency": "high"},
            {"question": "How do you prioritize which ML projects to work on?", "difficulty": "medium", "hint": "Consider business impact, feasibility, data availability, time to value.", "frequency": "high"},
            {"question": "Tell me about a time you disagreed with your team's approach. How did you handle it?", "difficulty": "medium", "hint": "Show data-driven decision making and collaborative problem solving.", "frequency": "high"},
            {"question": "What's the most challenging ML problem you've solved?", "difficulty": "medium", "hint": "Focus on the approach, iterations, and quantified impact.", "frequency": "very_high"},
            {"question": "How do you stay updated with the latest ML research?", "difficulty": "easy", "hint": "Mention papers, conferences (NeurIPS, ICML), blogs, communities.", "frequency": "high"},
            {"question": "Describe a project where you had to work with messy or incomplete data.", "difficulty": "medium", "hint": "Data cleaning process, assumptions made, impact on analysis.", "frequency": "high"},
            {"question": "Tell me about a time you had to make a decision with incomplete information.", "difficulty": "medium", "hint": "Show structured thinking and risk assessment.", "frequency": "high"},
            {"question": "How do you handle tight deadlines on ML projects?", "difficulty": "medium", "hint": "Prioritization, MVP approach, communication.", "frequency": "high"},
            {"question": "Describe a time when you had to learn a new technology quickly.", "difficulty": "easy", "hint": "Show learning agility and resourcefulness.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design a recommendation system for an e-commerce platform.", "difficulty": "hard", "hint": "Collaborative filtering, content-based, embeddings, real-time ranking.", "frequency": "very_high"},
            {"question": "How would you design an ML pipeline for real-time fraud detection?", "difficulty": "hard", "hint": "Feature store, low-latency serving, streaming data, model monitoring.", "frequency": "very_high"},
            {"question": "Design a system to train and serve 1000 different ML models.", "difficulty": "hard", "hint": "MLOps, model registry, orchestration (Airflow), feature store, A/B testing.", "frequency": "high"},
            {"question": "Design a feature store for a large-scale ML platform.", "difficulty": "hard", "hint": "Offline/online stores, point-in-time correctness, low-latency retrieval.", "frequency": "high"},
            {"question": "How would you design YouTube's video recommendation system?", "difficulty": "hard", "hint": "Two-tower model, candidate generation + ranking, user/item embeddings.", "frequency": "very_high"},
            {"question": "Design an ML system to detect spam/offensive content at scale.", "difficulty": "hard", "hint": "Multimodal (text+image), ensemble models, human-in-the-loop, appeal system.", "frequency": "high"},
            {"question": "Design a real-time bidding system for online advertising.", "difficulty": "hard", "hint": "Low-latency prediction, CTR models, budget pacing.", "frequency": "high"},
            {"question": "How would you design a search ranking system?", "difficulty": "hard", "hint": "Query understanding, retrieval, learning to rank, personalization.", "frequency": "high"},
            {"question": "Design an ML-powered pricing optimization system.", "difficulty": "hard", "hint": "Demand forecasting, price elasticity, A/B testing, constraints.", "frequency": "medium"},
            {"question": "Design a customer churn prediction system.", "difficulty": "medium", "hint": "Feature engineering, model selection, actionable predictions.", "frequency": "high"},
        ],
        "coding": [
            {"question": "Implement a function to calculate precision, recall, and F1 score from scratch.", "difficulty": "medium", "hint": "Need TP, FP, FN counts. F1 = 2 * (P * R) / (P + R).", "frequency": "high"},
            {"question": "Write code to implement K-means clustering from scratch.", "difficulty": "hard", "hint": "Initialize centroids, assign points, update centroids, repeat until convergence.", "frequency": "high"},
            {"question": "Implement gradient descent for linear regression.", "difficulty": "medium", "hint": "Update weights: w = w - lr * gradient. Gradient = (1/n) * X.T @ (X@w - y).", "frequency": "high"},
            {"question": "Implement a decision tree classifier from scratch.", "difficulty": "hard", "hint": "Information gain or Gini impurity for splits. Recursive tree building.", "frequency": "medium"},
            {"question": "Write code to implement cross-validation.", "difficulty": "medium", "hint": "Split data into K folds, train on K-1, validate on 1, rotate.", "frequency": "high"},
            {"question": "Implement logistic regression from scratch.", "difficulty": "medium", "hint": "Sigmoid function, binary cross-entropy loss, gradient descent.", "frequency": "high"},
            {"question": "Write a function to compute AUC-ROC.", "difficulty": "hard", "hint": "Sort by prediction, compute TPR/FPR at each threshold, integrate.", "frequency": "medium"},
            {"question": "Implement softmax function and cross-entropy loss.", "difficulty": "medium", "hint": "Softmax: exp(x)/sum(exp(x)). CE: -sum(y*log(p)).", "frequency": "high"},
        ],
        "ml_concepts": [
            {"question": "Explain how attention mechanisms work in transformers.", "difficulty": "hard", "hint": "Q, K, V matrices. Attention(Q,K,V) = softmax(QK^T/√d)V.", "frequency": "very_high"},
            {"question": "What's the difference between supervised, unsupervised, and reinforcement learning?", "difficulty": "easy", "hint": "Supervised: labeled data. Unsupervised: find patterns. RL: reward signal.", "frequency": "very_high"},
            {"question": "Explain batch normalization and why it helps training.", "difficulty": "medium", "hint": "Normalizes layer inputs, reduces internal covariate shift, allows higher LR.", "frequency": "high"},
            {"question": "What's the vanishing gradient problem and how do you solve it?", "difficulty": "medium", "hint": "Gradients shrink in deep networks. Solutions: ReLU, residual connections, LSTM.", "frequency": "very_high"},
            {"question": "Explain the difference between CNN and RNN architectures.", "difficulty": "medium", "hint": "CNN: spatial patterns (images). RNN: sequential data (text, time series).", "frequency": "high"},
            {"question": "What is transfer learning and when should you use it?", "difficulty": "medium", "hint": "Use pretrained model, fine-tune for new task. When: limited data, similar domain.", "frequency": "very_high"},
            {"question": "Explain the LSTM architecture and why it helps with long sequences.", "difficulty": "hard", "hint": "Gates (forget, input, output) control information flow, prevent vanishing gradients.", "frequency": "high"},
            {"question": "What's the difference between word2vec and BERT embeddings?", "difficulty": "hard", "hint": "Word2vec: static. BERT: contextual, captures word meaning in context.", "frequency": "high"},
            {"question": "Explain how GANs work.", "difficulty": "hard", "hint": "Generator creates fake data, discriminator distinguishes real/fake. Adversarial training.", "frequency": "high"},
            {"question": "What is the reparameterization trick in VAEs?", "difficulty": "hard", "hint": "Sample z = μ + σ*ε where ε ~ N(0,1). Allows backprop through sampling.", "frequency": "medium"},
        ],
    },
    
    # ============================================
    # AI ENGINEER - 55+ Questions
    # ============================================
    "ai_engineer": {
        "technical": [
            {"question": "Explain how RAG (Retrieval Augmented Generation) works. What are its limitations?", "difficulty": "medium", "hint": "Embed query, retrieve relevant docs, augment prompt, generate. Limitations: retrieval quality, context length.", "frequency": "very_high"},
            {"question": "What's the difference between fine-tuning and prompt engineering? When would you use each?", "difficulty": "medium", "hint": "Fine-tuning: change weights for specific task. Prompt eng: guide behavior without training.", "frequency": "very_high"},
            {"question": "How do you handle hallucinations in LLM applications?", "difficulty": "hard", "hint": "Grounding with RAG, citations, confidence scoring, fact-checking, guardrails.", "frequency": "very_high"},
            {"question": "Explain vector embeddings and how they're used in semantic search.", "difficulty": "easy", "hint": "Dense representations of meaning. Similarity search with cosine distance.", "frequency": "very_high"},
            {"question": "What are AI Agents and how do they differ from simple LLM calls?", "difficulty": "medium", "hint": "Agents have planning, tool use, memory, and can take actions.", "frequency": "very_high"},
            {"question": "How does function calling work in LLMs like GPT-4?", "difficulty": "medium", "hint": "Model outputs structured JSON to call predefined functions. Parse and execute.", "frequency": "high"},
            {"question": "Explain the concept of prompt injection and how to prevent it.", "difficulty": "hard", "hint": "Malicious prompts to override instructions. Use input validation, sandboxing, guardrails.", "frequency": "high"},
            {"question": "What's the difference between zero-shot, few-shot, and chain-of-thought prompting?", "difficulty": "medium", "hint": "Zero-shot: no examples. Few-shot: examples in prompt. CoT: reasoning steps.", "frequency": "very_high"},
            {"question": "How do you evaluate LLM outputs? What metrics do you use?", "difficulty": "medium", "hint": "BLEU, ROUGE for text. Human eval for quality. Task-specific metrics.", "frequency": "high"},
            {"question": "Explain the architecture of a production RAG system.", "difficulty": "hard", "hint": "Document ingestion, chunking, embedding, vector DB, retriever, reranker, generator.", "frequency": "very_high"},
            {"question": "What are the trade-offs between different embedding models?", "difficulty": "medium", "hint": "Dimension size, speed, quality, domain-specificity, cost.", "frequency": "high"},
            {"question": "How do you handle context window limitations in LLMs?", "difficulty": "medium", "hint": "Chunking, summarization, map-reduce, sliding window, long-context models.", "frequency": "high"},
            {"question": "Explain how to build a conversational AI with memory.", "difficulty": "hard", "hint": "Short-term (buffer), long-term (vector DB), summarization, context management.", "frequency": "high"},
            {"question": "What's the difference between semantic and lexical search?", "difficulty": "easy", "hint": "Semantic: meaning-based (embeddings). Lexical: keyword matching (BM25).", "frequency": "high"},
            {"question": "How do you optimize LLM costs in production?", "difficulty": "medium", "hint": "Caching, smaller models, batching, prompt optimization, response streaming.", "frequency": "high"},
            {"question": "Explain hybrid search and when to use it.", "difficulty": "medium", "hint": "Combine semantic + lexical. Better for mixed queries, proper nouns.", "frequency": "high"},
            {"question": "What is semantic caching and how does it work?", "difficulty": "medium", "hint": "Cache similar queries, not exact matches. Use embedding similarity.", "frequency": "medium"},
            {"question": "How do you implement guardrails for LLM applications?", "difficulty": "hard", "hint": "Input validation, output filtering, content moderation, rate limiting.", "frequency": "high"},
            {"question": "Explain the ReAct pattern for AI agents.", "difficulty": "hard", "hint": "Reasoning + Acting. Think → Act → Observe → Repeat.", "frequency": "high"},
            {"question": "What's the difference between LangChain and LlamaIndex?", "difficulty": "medium", "hint": "LangChain: general agent framework. LlamaIndex: data indexing focused.", "frequency": "high"},
        ],
        "behavioral": [
            {"question": "Describe a time when you had to choose between different LLM providers for a project.", "difficulty": "medium", "hint": "Consider cost, performance, latency, features, API reliability.", "frequency": "high"},
            {"question": "How do you stay updated with the rapidly evolving AI/LLM landscape?", "difficulty": "easy", "hint": "Papers, Twitter/X, Hacker News, company blogs, Discord communities.", "frequency": "high"},
            {"question": "Tell me about a time when you had to optimize an AI system for cost while maintaining quality.", "difficulty": "medium", "hint": "Caching, smaller models, batching, prompt optimization, hybrid approaches.", "frequency": "high"},
            {"question": "How do you handle stakeholder expectations around AI capabilities?", "difficulty": "medium", "hint": "Set realistic expectations, demo limitations, iterate with feedback.", "frequency": "high"},
            {"question": "Describe a challenging AI project you worked on. What made it difficult?", "difficulty": "medium", "hint": "Technical challenges, data issues, integration complexity.", "frequency": "high"},
            {"question": "How do you approach testing AI/LLM applications?", "difficulty": "medium", "hint": "Unit tests, integration tests, eval sets, human evaluation.", "frequency": "high"},
            {"question": "Tell me about a time you had to debug a complex AI system.", "difficulty": "medium", "hint": "Systematic approach, logging, monitoring, isolation.", "frequency": "high"},
            {"question": "How do you balance shipping quickly vs building robust AI systems?", "difficulty": "medium", "hint": "MVP approach, iterate, monitoring, fallbacks.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design a customer support chatbot that can answer questions about company products.", "difficulty": "medium", "hint": "RAG over product docs, conversation memory, escalation to human, feedback loop.", "frequency": "very_high"},
            {"question": "Design a system that can summarize and analyze thousands of documents.", "difficulty": "hard", "hint": "Chunking, map-reduce summarization, hierarchical summaries, parallel processing.", "frequency": "high"},
            {"question": "How would you build an AI coding assistant like GitHub Copilot?", "difficulty": "hard", "hint": "Fine-tuned code model, context from file/repo, streaming, safety filters.", "frequency": "high"},
            {"question": "Design an LLM-powered enterprise search system.", "difficulty": "hard", "hint": "Hybrid search (keyword + semantic), reranking, access control, caching.", "frequency": "high"},
            {"question": "Design a multi-agent system for complex task automation.", "difficulty": "hard", "hint": "Agent orchestration, tool definitions, memory management, error handling.", "frequency": "high"},
            {"question": "Design an AI writing assistant for content creators.", "difficulty": "medium", "hint": "Style matching, tone control, suggestions, real-time collaboration.", "frequency": "high"},
            {"question": "Design a question-answering system over a company's internal knowledge base.", "difficulty": "hard", "hint": "RAG, access control, source citations, feedback loop.", "frequency": "high"},
            {"question": "Design an AI-powered data extraction system from documents.", "difficulty": "hard", "hint": "OCR, layout understanding, entity extraction, validation.", "frequency": "high"},
            {"question": "How would you design an AI meeting summarizer?", "difficulty": "medium", "hint": "Transcription, speaker diarization, action item extraction, distribution.", "frequency": "high"},
            {"question": "Design a real-time AI translation system.", "difficulty": "hard", "hint": "Streaming ASR, NMT, latency optimization, context preservation.", "frequency": "medium"},
        ],
        "coding": [
            {"question": "Write a function to chunk a long document for RAG with overlap.", "difficulty": "medium", "hint": "Split by sentences/paragraphs, maintain overlap for context.", "frequency": "high"},
            {"question": "Implement a basic ReAct (Reasoning + Acting) agent loop.", "difficulty": "hard", "hint": "Thought → Action → Observation cycle. Parse LLM output for actions.", "frequency": "high"},
            {"question": "Implement semantic search using embeddings and cosine similarity.", "difficulty": "medium", "hint": "Embed query, compute cosine sim with all docs, return top-k.", "frequency": "high"},
            {"question": "Write code to implement a simple conversational memory system.", "difficulty": "medium", "hint": "Store conversation history, summarize old messages, sliding window.", "frequency": "high"},
            {"question": "Implement a prompt template system with variable substitution.", "difficulty": "easy", "hint": "Use placeholders like {variable}, replace at runtime.", "frequency": "high"},
            {"question": "Write code to implement retry logic with exponential backoff for API calls.", "difficulty": "easy", "hint": "Retry on failure, increase wait time exponentially.", "frequency": "high"},
            {"question": "Implement a simple vector similarity search without external libraries.", "difficulty": "medium", "hint": "Cosine similarity, normalize vectors, compute dot product.", "frequency": "medium"},
        ],
        "ml_concepts": [
            {"question": "Explain how temperature and top-p affect LLM outputs.", "difficulty": "medium", "hint": "Temperature: sharpness of distribution. Top-p: nucleus sampling threshold.", "frequency": "very_high"},
            {"question": "What are the key differences between GPT, Claude, and Gemini architectures?", "difficulty": "hard", "hint": "Training data, RLHF approach, context windows, multimodal capabilities.", "frequency": "high"},
            {"question": "How do chain-of-thought prompting and few-shot learning improve LLM performance?", "difficulty": "medium", "hint": "CoT: explicit reasoning. Few-shot: in-context learning from examples.", "frequency": "very_high"},
            {"question": "Explain how RLHF (Reinforcement Learning from Human Feedback) works.", "difficulty": "hard", "hint": "Train reward model on human preferences, fine-tune LLM with RL (PPO).", "frequency": "high"},
            {"question": "What's the difference between LoRA and full fine-tuning?", "difficulty": "medium", "hint": "LoRA: low-rank adapters, fewer params. Full: update all weights.", "frequency": "high"},
            {"question": "Explain tokenization and why it matters for LLMs.", "difficulty": "medium", "hint": "Converts text to tokens. Affects context length, multilingual support.", "frequency": "high"},
            {"question": "What is Constitutional AI?", "difficulty": "hard", "hint": "Self-critique and revision based on principles. Used by Anthropic.", "frequency": "medium"},
            {"question": "Explain the concept of emergent abilities in LLMs.", "difficulty": "hard", "hint": "Capabilities that appear only at large scale, not present in smaller models.", "frequency": "medium"},
            {"question": "What is the difference between encoder-only, decoder-only, and encoder-decoder models?", "difficulty": "hard", "hint": "BERT vs GPT vs T5. Different attention patterns and use cases.", "frequency": "high"},
            {"question": "Explain knowledge distillation for LLMs.", "difficulty": "hard", "hint": "Train smaller model to mimic larger model. Compress without much quality loss.", "frequency": "medium"},
        ],
    },
    
    # ============================================
    # DATA SCIENTIST - 45+ Questions
    # ============================================
    "data_scientist": {
        "technical": [
            {"question": "How do you approach a new data science project? Walk me through your process.", "difficulty": "medium", "hint": "Problem framing → data exploration → feature eng → modeling → evaluation → deployment.", "frequency": "very_high"},
            {"question": "Explain A/B testing and common pitfalls.", "difficulty": "medium", "hint": "Sample size, duration, multiple comparisons, novelty effects, selection bias.", "frequency": "very_high"},
            {"question": "What's the difference between correlation and causation? How do you establish causality?", "difficulty": "medium", "hint": "Correlation ≠ causation. RCTs, quasi-experiments, causal inference methods.", "frequency": "very_high"},
            {"question": "Explain statistical significance and p-values. What are their limitations?", "difficulty": "medium", "hint": "P-value: prob of results if null true. Limitations: not effect size, multiple testing.", "frequency": "very_high"},
            {"question": "What's the difference between parametric and non-parametric tests?", "difficulty": "medium", "hint": "Parametric assume distribution (t-test). Non-parametric don't (Mann-Whitney).", "frequency": "high"},
            {"question": "How do you handle missing data? What are the different strategies?", "difficulty": "medium", "hint": "Deletion, mean/median imputation, regression, MICE, flag indicator.", "frequency": "very_high"},
            {"question": "Explain hypothesis testing step by step.", "difficulty": "medium", "hint": "State H0/H1, choose significance level, collect data, compute test stat, decide.", "frequency": "high"},
            {"question": "What's the central limit theorem and why is it important?", "difficulty": "medium", "hint": "Sample means are normally distributed for large n. Enables statistical inference.", "frequency": "high"},
            {"question": "Explain multicollinearity and how to detect/handle it.", "difficulty": "medium", "hint": "High correlation between features. VIF detection. Remove or combine features.", "frequency": "high"},
            {"question": "What's the difference between Type I and Type II errors?", "difficulty": "easy", "hint": "Type I: false positive (reject true null). Type II: false negative (accept false null).", "frequency": "very_high"},
            {"question": "How do you calculate sample size for an experiment?", "difficulty": "hard", "hint": "Effect size, power, significance level, variance.", "frequency": "high"},
            {"question": "Explain the concept of statistical power.", "difficulty": "medium", "hint": "Probability of detecting an effect when it exists. 1 - Type II error rate.", "frequency": "high"},
            {"question": "What is survivorship bias and how do you avoid it?", "difficulty": "medium", "hint": "Only analyzing 'survivors'. Include failed cases in analysis.", "frequency": "high"},
            {"question": "Explain Simpson's paradox with an example.", "difficulty": "hard", "hint": "Trend reverses when data is aggregated vs disaggregated by groups.", "frequency": "medium"},
            {"question": "How do you detect and handle outliers?", "difficulty": "medium", "hint": "IQR, Z-score, visual inspection. Remove, cap, or use robust methods.", "frequency": "high"},
        ],
        "behavioral": [
            {"question": "Tell me about a data insight you discovered that had significant business impact.", "difficulty": "medium", "hint": "Quantify the impact. Explain how you communicated it.", "frequency": "very_high"},
            {"question": "How do you communicate technical findings to business stakeholders?", "difficulty": "easy", "hint": "Storytelling, visualization, focus on business impact, avoid jargon.", "frequency": "high"},
            {"question": "Describe a project where you had to deal with messy or incomplete data.", "difficulty": "medium", "hint": "Data cleaning process, assumptions made, impact on analysis.", "frequency": "high"},
            {"question": "How do you prioritize analyses when you have multiple stakeholder requests?", "difficulty": "medium", "hint": "Business impact, urgency, data availability, alignment with goals.", "frequency": "high"},
            {"question": "Tell me about a time you had to change your analysis approach mid-project.", "difficulty": "medium", "hint": "Adaptability, learning, communication with stakeholders.", "frequency": "high"},
            {"question": "Describe a situation where your analysis was challenged. How did you respond?", "difficulty": "medium", "hint": "Show openness to feedback, data-driven response.", "frequency": "high"},
            {"question": "How do you ensure reproducibility in your analyses?", "difficulty": "medium", "hint": "Version control, documentation, containerization, notebooks.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design a dashboard to track key business metrics in real-time.", "difficulty": "medium", "hint": "Data pipeline, ETL, storage (data warehouse), visualization layer.", "frequency": "high"},
            {"question": "How would you design a data pipeline for a recommendation system?", "difficulty": "hard", "hint": "Data ingestion, feature engineering, model training, serving, monitoring.", "frequency": "high"},
            {"question": "Design an experimentation platform for A/B testing.", "difficulty": "hard", "hint": "Random assignment, metric tracking, statistical analysis, guardrail metrics.", "frequency": "high"},
            {"question": "Design a customer segmentation system.", "difficulty": "medium", "hint": "Feature engineering, clustering, validation, actionability.", "frequency": "high"},
            {"question": "Design a data quality monitoring system.", "difficulty": "medium", "hint": "Schema validation, anomaly detection, alerting, lineage tracking.", "frequency": "high"},
        ],
        "coding": [
            {"question": "Write SQL to find the top 10 customers by total spend in the last 90 days.", "difficulty": "easy", "hint": "GROUP BY customer, SUM(amount), WHERE date > now() - 90 days, ORDER BY, LIMIT.", "frequency": "very_high"},
            {"question": "Implement cross-validation from scratch.", "difficulty": "medium", "hint": "Split data into K folds, train on K-1, validate on 1, rotate, average.", "frequency": "high"},
            {"question": "Write a function to detect outliers using IQR method.", "difficulty": "easy", "hint": "Q1 - 1.5*IQR to Q3 + 1.5*IQR is the non-outlier range.", "frequency": "high"},
            {"question": "Write pandas code to pivot, aggregate, and analyze a dataset.", "difficulty": "medium", "hint": "pd.pivot_table, groupby, agg, merge operations.", "frequency": "high"},
            {"question": "Write SQL to calculate running total and moving average.", "difficulty": "medium", "hint": "Window functions: SUM() OVER, AVG() OVER with ORDER BY.", "frequency": "high"},
            {"question": "Implement a function to calculate confidence interval.", "difficulty": "medium", "hint": "Mean ± z * (std / sqrt(n)).", "frequency": "high"},
            {"question": "Write SQL to find the second highest value in a table.", "difficulty": "easy", "hint": "LIMIT 1 OFFSET 1 or subquery with MAX.", "frequency": "high"},
        ],
        "ml_concepts": [
            {"question": "Explain the difference between parametric and non-parametric models.", "difficulty": "medium", "hint": "Parametric: fixed params (linear regression). Non-parametric: flexible (KNN).", "frequency": "high"},
            {"question": "How do you select features for a model?", "difficulty": "medium", "hint": "Correlation, mutual information, recursive feature elimination, domain knowledge.", "frequency": "high"},
            {"question": "What's the difference between regression and classification?", "difficulty": "easy", "hint": "Regression: continuous output. Classification: discrete categories.", "frequency": "very_high"},
            {"question": "Explain ensemble methods and why they work.", "difficulty": "medium", "hint": "Combine multiple models. Reduce variance (bagging) or bias (boosting).", "frequency": "high"},
            {"question": "What is time series forecasting and what methods do you use?", "difficulty": "medium", "hint": "ARIMA, Prophet, exponential smoothing, deep learning.", "frequency": "high"},
            {"question": "Explain the bias in model predictions vs statistical bias.", "difficulty": "hard", "hint": "Model bias: systematic error. Statistical bias: estimator doesn't equal true value.", "frequency": "medium"},
        ],
    },

    # ============================================
    # PROMPT ENGINEER - 30+ Questions
    # ============================================
    "prompt_engineer": {
        "technical": [
            {"question": "What makes a good prompt? Describe the key principles.", "difficulty": "easy", "hint": "Clear instructions, context, examples, output format, constraints.", "frequency": "very_high"},
            {"question": "Explain the difference between zero-shot, one-shot, and few-shot prompting.", "difficulty": "easy", "hint": "Number of examples provided. More examples = better performance usually.", "frequency": "very_high"},
            {"question": "How does chain-of-thought prompting work and when should you use it?", "difficulty": "medium", "hint": "Ask model to reason step-by-step. Good for math, logic, complex reasoning.", "frequency": "very_high"},
            {"question": "What is prompt injection and how do you defend against it?", "difficulty": "hard", "hint": "Malicious inputs to override instructions. Defense: input validation, sandboxing.", "frequency": "very_high"},
            {"question": "How do you evaluate prompt effectiveness? What metrics do you use?", "difficulty": "medium", "hint": "Task-specific metrics, human evaluation, A/B testing, consistency.", "frequency": "high"},
            {"question": "Explain the role of system prompts vs user prompts.", "difficulty": "easy", "hint": "System: sets behavior/persona. User: actual queries. Different priority levels.", "frequency": "high"},
            {"question": "How do you handle context window limitations?", "difficulty": "medium", "hint": "Summarization, chunking, prioritizing relevant info, map-reduce.", "frequency": "high"},
            {"question": "What's the difference between temperature and top-p sampling?", "difficulty": "medium", "hint": "Temperature: distribution sharpness. Top-p: cumulative probability threshold.", "frequency": "high"},
            {"question": "How do you create prompts that are robust to edge cases?", "difficulty": "hard", "hint": "Test with adversarial inputs, add explicit constraints, use guardrails.", "frequency": "high"},
            {"question": "Explain tree-of-thought prompting.", "difficulty": "hard", "hint": "Explore multiple reasoning paths, evaluate, backtrack. Better for complex problems.", "frequency": "medium"},
            {"question": "What is self-consistency in prompting?", "difficulty": "medium", "hint": "Generate multiple responses, take majority vote. Improves reliability.", "frequency": "medium"},
            {"question": "How do you prompt for structured output (JSON, tables)?", "difficulty": "medium", "hint": "Explicit format instructions, examples, schema definition.", "frequency": "high"},
            {"question": "What is prompt chaining and when do you use it?", "difficulty": "medium", "hint": "Break complex task into steps, output of one is input to next.", "frequency": "high"},
            {"question": "How do you optimize prompts for cost without sacrificing quality?", "difficulty": "medium", "hint": "Shorter prompts, fewer examples, caching, smaller models for simple tasks.", "frequency": "high"},
            {"question": "Explain ReAct prompting pattern.", "difficulty": "hard", "hint": "Reasoning + Acting. Interleave thought, action, observation.", "frequency": "high"},
        ],
        "behavioral": [
            {"question": "Describe a time when you significantly improved a prompt's performance.", "difficulty": "medium", "hint": "Quantify improvement. Explain iteration process.", "frequency": "high"},
            {"question": "How do you handle ambiguous requirements from stakeholders?", "difficulty": "medium", "hint": "Ask clarifying questions, propose options, iterate with feedback.", "frequency": "high"},
            {"question": "How do you stay updated with new prompting techniques?", "difficulty": "easy", "hint": "Papers, blogs, experimentation, community discussions.", "frequency": "high"},
            {"question": "Describe a situation where a prompt worked in testing but failed in production.", "difficulty": "medium", "hint": "Edge cases, distribution shift, user behavior differences.", "frequency": "high"},
        ],
        "coding": [
            {"question": "Write a prompt template system with variable substitution.", "difficulty": "medium", "hint": "Use placeholders like {variable}, replace at runtime.", "frequency": "high"},
            {"question": "Implement a prompt testing framework to compare different prompts.", "difficulty": "hard", "hint": "Run same inputs through different prompts, collect metrics, compare.", "frequency": "medium"},
            {"question": "Write code to implement semantic caching for prompts.", "difficulty": "hard", "hint": "Embed prompts, find similar cached responses within threshold.", "frequency": "medium"},
            {"question": "Implement a prompt versioning system.", "difficulty": "medium", "hint": "Store versions, track performance, enable rollback.", "frequency": "medium"},
        ],
        "ml_concepts": [
            {"question": "Explain how in-context learning works in LLMs.", "difficulty": "hard", "hint": "Model learns from examples in prompt without weight updates.", "frequency": "high"},
            {"question": "What is the relationship between prompt design and model behavior?", "difficulty": "medium", "hint": "Prompts activate different model capabilities, bias outputs.", "frequency": "high"},
            {"question": "How do different models respond to the same prompt differently?", "difficulty": "medium", "hint": "Training data, RLHF, architecture differences affect behavior.", "frequency": "high"},
        ],
    },

    # ============================================
    # MLOPS ENGINEER - 35+ Questions
    # ============================================
    "mlops_engineer": {
        "technical": [
            {"question": "Explain the ML lifecycle and where MLOps fits in.", "difficulty": "easy", "hint": "Data → Training → Evaluation → Deployment → Monitoring → Retraining.", "frequency": "very_high"},
            {"question": "What's the difference between model serving and model training infrastructure?", "difficulty": "medium", "hint": "Training: batch, GPUs, experiments. Serving: real-time, low-latency, scaling.", "frequency": "high"},
            {"question": "How do you implement model versioning and reproducibility?", "difficulty": "medium", "hint": "Model registry, data versioning (DVC), experiment tracking (MLflow).", "frequency": "very_high"},
            {"question": "Explain feature stores and their benefits.", "difficulty": "medium", "hint": "Centralized feature repo. Consistency, reusability, point-in-time correctness.", "frequency": "very_high"},
            {"question": "How do you detect and handle model drift?", "difficulty": "hard", "hint": "Monitor input/output distributions. Retrain triggers. Shadow mode testing.", "frequency": "very_high"},
            {"question": "What's the difference between A/B testing and shadow mode for model deployment?", "difficulty": "medium", "hint": "A/B: split traffic. Shadow: run new model alongside without affecting users.", "frequency": "high"},
            {"question": "How do you implement CI/CD for ML models?", "difficulty": "hard", "hint": "Automated testing, validation, deployment pipelines, rollback capabilities.", "frequency": "high"},
            {"question": "Explain canary deployments for ML models.", "difficulty": "medium", "hint": "Gradual rollout to small % of traffic, monitor metrics, expand or rollback.", "frequency": "high"},
            {"question": "What metrics do you monitor for ML models in production?", "difficulty": "medium", "hint": "Latency, throughput, error rate, data drift, prediction drift, business metrics.", "frequency": "high"},
            {"question": "How do you handle model rollbacks?", "difficulty": "medium", "hint": "Version tracking, quick switch mechanism, monitoring triggers.", "frequency": "high"},
            {"question": "Explain blue-green deployment for ML models.", "difficulty": "medium", "hint": "Two identical environments, switch traffic instantly, easy rollback.", "frequency": "high"},
            {"question": "What is data drift vs concept drift?", "difficulty": "medium", "hint": "Data drift: input distribution changes. Concept drift: relationship between input/output changes.", "frequency": "very_high"},
            {"question": "How do you ensure model reproducibility?", "difficulty": "medium", "hint": "Seed fixing, environment pinning, data versioning, code versioning.", "frequency": "high"},
            {"question": "Explain model governance and compliance requirements.", "difficulty": "hard", "hint": "Audit trails, access control, bias monitoring, documentation.", "frequency": "medium"},
            {"question": "What's the difference between batch and real-time inference?", "difficulty": "easy", "hint": "Batch: process many at once, higher latency. Real-time: single, low-latency.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design an ML platform that supports 100+ data scientists.", "difficulty": "hard", "hint": "Compute isolation, shared feature store, experiment tracking, model registry.", "frequency": "high"},
            {"question": "Design a real-time feature computation system.", "difficulty": "hard", "hint": "Stream processing (Kafka/Flink), feature store, low-latency serving.", "frequency": "high"},
            {"question": "Design a model monitoring and alerting system.", "difficulty": "hard", "hint": "Metrics collection, drift detection, performance dashboards, automated alerts.", "frequency": "high"},
            {"question": "Design a model training pipeline for distributed training.", "difficulty": "hard", "hint": "Data sharding, gradient aggregation, checkpointing, fault tolerance.", "frequency": "high"},
            {"question": "Design a feature store architecture.", "difficulty": "hard", "hint": "Offline/online stores, materialization, point-in-time queries, low-latency retrieval.", "frequency": "high"},
        ],
        "coding": [
            {"question": "Write a script to track experiment metrics to MLflow.", "difficulty": "medium", "hint": "mlflow.log_metric, mlflow.log_param, mlflow.log_artifact.", "frequency": "high"},
            {"question": "Implement a simple model serving API with FastAPI.", "difficulty": "medium", "hint": "Load model, create endpoint, handle requests, return predictions.", "frequency": "high"},
            {"question": "Write code to compute data drift using KL divergence.", "difficulty": "hard", "hint": "Compare distributions of features between training and production data.", "frequency": "medium"},
            {"question": "Implement a model health check endpoint.", "difficulty": "easy", "hint": "Test model with known input, verify output, check latency.", "frequency": "high"},
        ],
        "behavioral": [
            {"question": "Tell me about a time you had to debug a production ML issue.", "difficulty": "medium", "hint": "Systematic approach, root cause analysis, fix and prevention.", "frequency": "high"},
            {"question": "How do you balance model performance vs operational simplicity?", "difficulty": "medium", "hint": "Trade-offs, business requirements, maintenance burden.", "frequency": "high"},
            {"question": "Describe a challenging deployment you handled.", "difficulty": "medium", "hint": "Challenges, solutions, lessons learned.", "frequency": "high"},
        ],
    },

    # ============================================
    # COMPUTER VISION ENGINEER - 35+ Questions  
    # ============================================
    "cv_engineer": {
        "technical": [
            {"question": "Explain how convolutional neural networks (CNNs) work.", "difficulty": "medium", "hint": "Convolution layers extract features, pooling reduces dimensions, FC layers classify.", "frequency": "very_high"},
            {"question": "What's the difference between object detection and image segmentation?", "difficulty": "easy", "hint": "Detection: bounding boxes. Segmentation: pixel-level classification.", "frequency": "very_high"},
            {"question": "Explain the architecture of YOLO. How does it achieve real-time detection?", "difficulty": "hard", "hint": "Single pass through network. Grid-based predictions. NMS for filtering.", "frequency": "high"},
            {"question": "What's the difference between semantic, instance, and panoptic segmentation?", "difficulty": "medium", "hint": "Semantic: class per pixel. Instance: separate objects. Panoptic: both.", "frequency": "high"},
            {"question": "How does transfer learning work in computer vision?", "difficulty": "medium", "hint": "Use pretrained backbone (ImageNet), fine-tune on target task.", "frequency": "very_high"},
            {"question": "Explain data augmentation techniques for images.", "difficulty": "easy", "hint": "Flip, rotate, crop, color jitter, mixup, cutout, AutoAugment.", "frequency": "very_high"},
            {"question": "What's the difference between R-CNN, Fast R-CNN, and Faster R-CNN?", "difficulty": "hard", "hint": "R-CNN: separate CNN per region. Fast: ROI pooling. Faster: Region Proposal Network.", "frequency": "high"},
            {"question": "How do Vision Transformers (ViT) work?", "difficulty": "hard", "hint": "Split image into patches, embed patches, apply transformer encoder.", "frequency": "high"},
            {"question": "Explain anchor boxes in object detection.", "difficulty": "medium", "hint": "Predefined boxes of different sizes/ratios. Model predicts offsets and classes.", "frequency": "high"},
            {"question": "What is feature pyramid network (FPN)?", "difficulty": "hard", "hint": "Multi-scale feature maps for detecting objects at different sizes.", "frequency": "high"},
            {"question": "How do you handle varying image sizes in CNNs?", "difficulty": "medium", "hint": "Resize, pad, adaptive pooling, fully convolutional networks.", "frequency": "high"},
            {"question": "Explain batch normalization in CNNs.", "difficulty": "medium", "hint": "Normalize activations per batch. Stabilizes training, allows higher LR.", "frequency": "high"},
            {"question": "What is non-maximum suppression (NMS)?", "difficulty": "medium", "hint": "Remove overlapping detections, keep highest confidence.", "frequency": "high"},
            {"question": "How do you evaluate object detection models?", "difficulty": "medium", "hint": "mAP, IoU threshold, precision-recall curves.", "frequency": "high"},
            {"question": "Explain depthwise separable convolutions.", "difficulty": "hard", "hint": "Depthwise + pointwise. Reduces params/compute. Used in MobileNet.", "frequency": "medium"},
        ],
        "system_design": [
            {"question": "Design a real-time video analytics system for security cameras.", "difficulty": "hard", "hint": "Edge processing, object detection, tracking, alerting, storage.", "frequency": "high"},
            {"question": "Design a visual search system for e-commerce.", "difficulty": "hard", "hint": "Feature extraction, similarity search, index optimization.", "frequency": "high"},
            {"question": "Design an autonomous vehicle perception system.", "difficulty": "hard", "hint": "Multi-sensor fusion, 3D detection, tracking, prediction.", "frequency": "high"},
            {"question": "Design a face recognition system at scale.", "difficulty": "hard", "hint": "Face detection, embedding, indexing, matching, privacy considerations.", "frequency": "high"},
            {"question": "Design an OCR system for document processing.", "difficulty": "hard", "hint": "Detection, recognition, layout analysis, post-processing.", "frequency": "high"},
        ],
        "coding": [
            {"question": "Implement non-maximum suppression (NMS) from scratch.", "difficulty": "hard", "hint": "Sort by confidence, keep highest, remove overlapping boxes (IoU > threshold).", "frequency": "high"},
            {"question": "Write code to compute IoU (Intersection over Union) between two boxes.", "difficulty": "medium", "hint": "Intersection area / Union area. Handle edge cases.", "frequency": "high"},
            {"question": "Implement a simple convolution operation from scratch.", "difficulty": "medium", "hint": "Slide filter over image, element-wise multiply, sum.", "frequency": "high"},
            {"question": "Write code to implement image augmentation pipeline.", "difficulty": "medium", "hint": "Random transforms: flip, rotate, color jitter, etc.", "frequency": "high"},
        ],
        "behavioral": [
            {"question": "Describe a challenging CV project you worked on.", "difficulty": "medium", "hint": "Technical challenges, data issues, solutions.", "frequency": "high"},
            {"question": "How do you handle limited training data in CV?", "difficulty": "medium", "hint": "Augmentation, transfer learning, synthetic data, semi-supervised.", "frequency": "high"},
        ],
        "ml_concepts": [
            {"question": "What is the receptive field in CNNs?", "difficulty": "hard", "hint": "Region of input that affects a particular output neuron.", "frequency": "high"},
            {"question": "Explain dilated/atrous convolutions.", "difficulty": "hard", "hint": "Increase receptive field without losing resolution. Used in segmentation.", "frequency": "medium"},
            {"question": "What is focal loss and when do you use it?", "difficulty": "hard", "hint": "Down-weights easy examples. Helps with class imbalance in detection.", "frequency": "medium"},
        ],
    },

    # ============================================
    # NLP ENGINEER - 35+ Questions
    # ============================================
    "nlp_engineer": {
        "technical": [
            {"question": "Explain the transformer architecture in detail.", "difficulty": "hard", "hint": "Self-attention, multi-head attention, positional encoding, encoder-decoder.", "frequency": "very_high"},
            {"question": "What's the difference between BERT and GPT architectures?", "difficulty": "medium", "hint": "BERT: encoder, bidirectional. GPT: decoder, autoregressive.", "frequency": "very_high"},
            {"question": "How does tokenization work? Compare BPE, WordPiece, and SentencePiece.", "difficulty": "medium", "hint": "Subword tokenization. BPE: merge frequent pairs. WordPiece: likelihood-based.", "frequency": "high"},
            {"question": "Explain attention mechanisms. What's the difference between self-attention and cross-attention?", "difficulty": "hard", "hint": "Self: attend to same sequence. Cross: attend to different sequence (encoder-decoder).", "frequency": "very_high"},
            {"question": "What's the difference between word embeddings (Word2Vec) and contextual embeddings (BERT)?", "difficulty": "medium", "hint": "Word2Vec: static per word. BERT: context-dependent representations.", "frequency": "high"},
            {"question": "How do you handle out-of-vocabulary words?", "difficulty": "medium", "hint": "Subword tokenization, character-level models, special tokens.", "frequency": "high"},
            {"question": "Explain named entity recognition (NER) and common approaches.", "difficulty": "medium", "hint": "Sequence labeling. BIO tagging. CRF layer, transformer-based models.", "frequency": "high"},
            {"question": "What is positional encoding and why is it needed?", "difficulty": "hard", "hint": "Transformers have no inherent position info. Add position via sinusoidal or learned.", "frequency": "high"},
            {"question": "Explain the difference between encoder-only, decoder-only, and encoder-decoder models.", "difficulty": "hard", "hint": "Encoder: BERT (classification). Decoder: GPT (generation). Both: T5 (seq2seq).", "frequency": "high"},
            {"question": "How do you handle long documents in NLP?", "difficulty": "hard", "hint": "Chunking, hierarchical models, sparse attention, long-context models.", "frequency": "high"},
            {"question": "What is perplexity and how is it used to evaluate language models?", "difficulty": "medium", "hint": "Exponentiated cross-entropy. Lower is better. Measures prediction confidence.", "frequency": "high"},
            {"question": "Explain text classification approaches.", "difficulty": "medium", "hint": "Traditional (TF-IDF + SVM), neural (CNN, LSTM), transformers (BERT fine-tuning).", "frequency": "high"},
            {"question": "What is the masked language modeling objective?", "difficulty": "medium", "hint": "Predict masked tokens. Used in BERT pretraining.", "frequency": "high"},
            {"question": "Explain sentiment analysis approaches.", "difficulty": "medium", "hint": "Lexicon-based, ML classifiers, deep learning, fine-tuned transformers.", "frequency": "high"},
            {"question": "How do you handle multilingual NLP?", "difficulty": "hard", "hint": "Multilingual models (mBERT, XLM-R), translation, language-specific fine-tuning.", "frequency": "medium"},
        ],
        "system_design": [
            {"question": "Design a search engine with semantic understanding.", "difficulty": "hard", "hint": "Query understanding, retrieval (sparse + dense), ranking, personalization.", "frequency": "high"},
            {"question": "Design a text summarization system.", "difficulty": "hard", "hint": "Extractive vs abstractive, chunking, evaluation.", "frequency": "high"},
            {"question": "Design a machine translation system.", "difficulty": "hard", "hint": "Encoder-decoder, attention, beam search, evaluation (BLEU).", "frequency": "high"},
            {"question": "Design a chatbot system with intent classification.", "difficulty": "hard", "hint": "Intent detection, entity extraction, dialog management, response generation.", "frequency": "high"},
        ],
        "coding": [
            {"question": "Implement a simple BPE tokenizer from scratch.", "difficulty": "hard", "hint": "Start with characters, iteratively merge most frequent pairs.", "frequency": "medium"},
            {"question": "Write code to compute BLEU score.", "difficulty": "medium", "hint": "N-gram precision with brevity penalty.", "frequency": "high"},
            {"question": "Implement TF-IDF from scratch.", "difficulty": "medium", "hint": "TF: term frequency. IDF: inverse document frequency.", "frequency": "high"},
            {"question": "Write code to implement beam search for text generation.", "difficulty": "hard", "hint": "Maintain top-k sequences at each step, expand and prune.", "frequency": "medium"},
        ],
        "behavioral": [
            {"question": "Describe a challenging NLP project you worked on.", "difficulty": "medium", "hint": "Data challenges, model selection, evaluation.", "frequency": "high"},
            {"question": "How do you handle low-resource languages?", "difficulty": "hard", "hint": "Transfer learning, data augmentation, multilingual models.", "frequency": "medium"},
        ],
        "ml_concepts": [
            {"question": "What is the attention mechanism formula?", "difficulty": "hard", "hint": "Attention(Q,K,V) = softmax(QK^T/√d_k)V.", "frequency": "high"},
            {"question": "Explain multi-head attention.", "difficulty": "hard", "hint": "Multiple attention heads in parallel, concatenate, project.", "frequency": "high"},
            {"question": "What is layer normalization and why is it used in transformers?", "difficulty": "medium", "hint": "Normalize across features. Stabilizes training, works with varying batch sizes.", "frequency": "high"},
        ],
    },
}

# ============================================
# ADDITIONAL ROLES - Add more questions
# ============================================

ROLE_QUESTIONS.update({
    "ai_product_manager": {
        "technical": [
            {"question": "How do you prioritize features for an AI product?", "difficulty": "medium", "hint": "User value, technical feasibility, business impact, AI-specific risks.", "frequency": "very_high"},
            {"question": "How do you measure success for an AI/ML product?", "difficulty": "medium", "hint": "Business metrics, model metrics, user satisfaction, safety metrics.", "frequency": "very_high"},
            {"question": "How do you handle AI model failures in production?", "difficulty": "medium", "hint": "Fallbacks, monitoring, user communication, incident response.", "frequency": "high"},
            {"question": "How do you communicate AI limitations to stakeholders?", "difficulty": "medium", "hint": "Set expectations, show failure cases, explain uncertainty.", "frequency": "high"},
            {"question": "What's your framework for evaluating build vs buy for AI features?", "difficulty": "medium", "hint": "Cost, time, differentiation, maintenance, data privacy.", "frequency": "high"},
            {"question": "How do you handle ethical concerns in AI product development?", "difficulty": "hard", "hint": "Bias audits, transparency, user consent, governance.", "frequency": "high"},
            {"question": "How do you write requirements for AI/ML features?", "difficulty": "medium", "hint": "Performance bounds, edge cases, evaluation criteria, data requirements.", "frequency": "high"},
            {"question": "How do you manage stakeholder expectations for AI timelines?", "difficulty": "medium", "hint": "Uncertainty in ML, iterative approach, clear milestones.", "frequency": "high"},
        ],
        "behavioral": [
            {"question": "Tell me about an AI product you launched. What was your approach?", "difficulty": "medium", "hint": "Cover research, MVP, iteration, scaling.", "frequency": "very_high"},
            {"question": "How do you balance user needs with AI capabilities?", "difficulty": "medium", "hint": "User research, technical constraints, iteration.", "frequency": "high"},
            {"question": "Describe a time when an AI feature didn't meet expectations.", "difficulty": "medium", "hint": "Learning, pivoting, stakeholder management.", "frequency": "high"},
            {"question": "How do you work with data scientists and ML engineers?", "difficulty": "medium", "hint": "Collaboration, communication, shared understanding.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design the product strategy for an AI writing assistant.", "difficulty": "hard", "hint": "User segments, use cases, differentiation, monetization.", "frequency": "high"},
            {"question": "How would you design the rollout strategy for a high-risk AI feature?", "difficulty": "hard", "hint": "Staged rollout, monitoring, rollback plan, user communication.", "frequency": "high"},
        ],
    },

    "ai_research_scientist": {
        "technical": [
            {"question": "Describe your research methodology.", "difficulty": "medium", "hint": "Hypothesis, experiments, baselines, ablations, analysis.", "frequency": "very_high"},
            {"question": "How do you decide which research direction to pursue?", "difficulty": "hard", "hint": "Impact, feasibility, novelty, alignment with goals.", "frequency": "high"},
            {"question": "Explain a paper you've published in detail.", "difficulty": "hard", "hint": "Motivation, methods, results, limitations, impact.", "frequency": "very_high"},
            {"question": "What's a research area you think is underexplored?", "difficulty": "hard", "hint": "Show awareness of field, identify gaps.", "frequency": "high"},
            {"question": "How do you handle negative results in research?", "difficulty": "medium", "hint": "Learning, pivoting, sometimes publishing negative results.", "frequency": "high"},
            {"question": "How do you validate your research findings?", "difficulty": "hard", "hint": "Multiple experiments, ablations, statistical significance, reproducibility.", "frequency": "high"},
        ],
        "ml_concepts": [
            {"question": "Explain the attention mechanism mathematically.", "difficulty": "hard", "hint": "Q, K, V, softmax, scaling factor.", "frequency": "very_high"},
            {"question": "What are the limitations of current transformer architectures?", "difficulty": "hard", "hint": "Quadratic attention, context length, reasoning.", "frequency": "high"},
            {"question": "Explain the theory behind contrastive learning.", "difficulty": "hard", "hint": "Learn representations by contrasting positive/negative pairs.", "frequency": "high"},
            {"question": "What is the lottery ticket hypothesis?", "difficulty": "hard", "hint": "Sparse subnetworks can match full network performance.", "frequency": "medium"},
        ],
        "behavioral": [
            {"question": "How do you collaborate with other researchers?", "difficulty": "medium", "hint": "Communication, code sharing, paper writing.", "frequency": "high"},
            {"question": "Describe a time when your research direction changed.", "difficulty": "medium", "hint": "Adaptability, learning from results.", "frequency": "high"},
        ],
    },

    "deep_learning_engineer": {
        "technical": [
            {"question": "Explain how GPU training differs from CPU training.", "difficulty": "medium", "hint": "Parallelism, memory hierarchy, batching.", "frequency": "very_high"},
            {"question": "How do you debug a neural network that's not training?", "difficulty": "hard", "hint": "Learning rate, gradients, data, architecture, initialization.", "frequency": "very_high"},
            {"question": "Explain mixed-precision training and its benefits.", "difficulty": "medium", "hint": "FP16 for speed, FP32 for stability, loss scaling.", "frequency": "high"},
            {"question": "How do you optimize inference for deployment?", "difficulty": "hard", "hint": "Quantization, pruning, distillation, TensorRT.", "frequency": "high"},
            {"question": "Explain gradient clipping and when to use it.", "difficulty": "medium", "hint": "Prevents exploding gradients. Clip by norm or value.", "frequency": "high"},
            {"question": "What is knowledge distillation?", "difficulty": "hard", "hint": "Train smaller student model to mimic larger teacher model.", "frequency": "high"},
            {"question": "How do you handle memory constraints when training large models?", "difficulty": "hard", "hint": "Gradient checkpointing, mixed precision, model parallelism.", "frequency": "high"},
            {"question": "Explain the difference between data parallelism and model parallelism.", "difficulty": "hard", "hint": "Data: split batch. Model: split model across devices.", "frequency": "high"},
        ],
        "coding": [
            {"question": "Implement a custom loss function in PyTorch.", "difficulty": "medium", "hint": "Subclass nn.Module or use functional API.", "frequency": "high"},
            {"question": "Write code to implement learning rate scheduling.", "difficulty": "medium", "hint": "StepLR, CosineAnnealing, warmup.", "frequency": "high"},
            {"question": "Implement gradient accumulation.", "difficulty": "medium", "hint": "Accumulate gradients over multiple batches before optimizer step.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design a distributed training system.", "difficulty": "hard", "hint": "Data parallelism, gradient synchronization, fault tolerance.", "frequency": "high"},
            {"question": "Design a model serving system with GPU inference.", "difficulty": "hard", "hint": "Batching, model loading, request queuing, scaling.", "frequency": "high"},
        ],
    },

    "llm_engineer": {
        "technical": [
            {"question": "Explain the difference between pre-training and fine-tuning.", "difficulty": "medium", "hint": "Pre-training: general knowledge. Fine-tuning: task-specific.", "frequency": "very_high"},
            {"question": "How do you optimize LLM inference latency?", "difficulty": "hard", "hint": "KV-cache, batching, quantization, speculative decoding.", "frequency": "very_high"},
            {"question": "Explain parameter-efficient fine-tuning methods.", "difficulty": "hard", "hint": "LoRA, prefix tuning, adapters.", "frequency": "high"},
            {"question": "How do you evaluate LLM quality?", "difficulty": "hard", "hint": "Perplexity, downstream tasks, human eval, safety benchmarks.", "frequency": "high"},
            {"question": "What is the KV cache and why is it important?", "difficulty": "hard", "hint": "Stores key-value pairs from previous tokens. Avoids recomputation.", "frequency": "high"},
            {"question": "Explain speculative decoding.", "difficulty": "hard", "hint": "Use smaller model to draft, larger model to verify. Speeds up generation.", "frequency": "medium"},
            {"question": "How do you handle long contexts in LLMs?", "difficulty": "hard", "hint": "Sliding window, chunking, sparse attention, RoPE scaling.", "frequency": "high"},
            {"question": "What is rotary position embedding (RoPE)?", "difficulty": "hard", "hint": "Encodes position in rotation matrix. Better length generalization.", "frequency": "medium"},
        ],
        "system_design": [
            {"question": "Design an LLM serving infrastructure.", "difficulty": "hard", "hint": "Load balancing, batching, caching, GPU management.", "frequency": "high"},
            {"question": "Design a fine-tuning pipeline for custom LLM applications.", "difficulty": "hard", "hint": "Data prep, training infrastructure, evaluation, deployment.", "frequency": "high"},
        ],
        "coding": [
            {"question": "Implement streaming response for LLM inference.", "difficulty": "medium", "hint": "Yield tokens as generated, handle async.", "frequency": "high"},
            {"question": "Write code to implement KV cache.", "difficulty": "hard", "hint": "Store K, V tensors, append new, manage memory.", "frequency": "medium"},
        ],
    },

    "rag_engineer": {
        "technical": [
            {"question": "Design a production RAG system architecture.", "difficulty": "hard", "hint": "Ingestion, chunking, embedding, retrieval, reranking, generation.", "frequency": "very_high"},
            {"question": "How do you evaluate RAG system quality?", "difficulty": "hard", "hint": "Retrieval metrics (recall, MRR), generation metrics, E2E eval.", "frequency": "high"},
            {"question": "How do you handle multi-hop questions in RAG?", "difficulty": "hard", "hint": "Iterative retrieval, query decomposition, graph RAG.", "frequency": "high"},
            {"question": "Explain different chunking strategies and their tradeoffs.", "difficulty": "medium", "hint": "Fixed-size, semantic, document structure, recursive.", "frequency": "high"},
            {"question": "What is hybrid search and when should you use it?", "difficulty": "medium", "hint": "Combine dense + sparse retrieval. Better for diverse queries.", "frequency": "high"},
            {"question": "How do you handle document updates in a RAG system?", "difficulty": "hard", "hint": "Incremental indexing, versioning, cache invalidation.", "frequency": "high"},
            {"question": "Explain reranking in RAG systems.", "difficulty": "medium", "hint": "Two-stage retrieval: fast retrieval then precise reranking.", "frequency": "high"},
            {"question": "How do you handle structured data in RAG?", "difficulty": "hard", "hint": "Text-to-SQL, knowledge graphs, table understanding.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design a RAG system for a legal document database.", "difficulty": "hard", "hint": "Citation handling, hierarchical docs, access control.", "frequency": "high"},
            {"question": "Design a conversational RAG system with memory.", "difficulty": "hard", "hint": "Context management, query reformulation, coherence.", "frequency": "high"},
        ],
        "coding": [
            {"question": "Implement semantic chunking for documents.", "difficulty": "medium", "hint": "Use sentence embeddings to find natural break points.", "frequency": "high"},
            {"question": "Write code to implement reciprocal rank fusion.", "difficulty": "medium", "hint": "Combine rankings from multiple retrievers using RRF formula.", "frequency": "medium"},
        ],
    },

    "robotics_ml_engineer": {
        "technical": [
            {"question": "Explain sim-to-real transfer in robotics.", "difficulty": "hard", "hint": "Domain randomization, system identification, real-world fine-tuning.", "frequency": "very_high"},
            {"question": "How do you handle sensor noise in robot perception?", "difficulty": "medium", "hint": "Filtering, sensor fusion, robust features.", "frequency": "high"},
            {"question": "Explain imitation learning vs reinforcement learning for robotics.", "difficulty": "hard", "hint": "IL: expert demos. RL: reward signal. Tradeoffs.", "frequency": "high"},
            {"question": "What is inverse kinematics and how is it used?", "difficulty": "medium", "hint": "Calculate joint angles to reach target position.", "frequency": "high"},
            {"question": "Explain SLAM (Simultaneous Localization and Mapping).", "difficulty": "hard", "hint": "Build map while tracking robot position. Sensor fusion.", "frequency": "high"},
            {"question": "How do you handle real-time constraints in robotics ML?", "difficulty": "hard", "hint": "Model optimization, efficient inference, prioritization.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design a robot manipulation system.", "difficulty": "hard", "hint": "Perception, planning, control, error handling.", "frequency": "high"},
            {"question": "Design an autonomous navigation system.", "difficulty": "hard", "hint": "Mapping, localization, path planning, obstacle avoidance.", "frequency": "high"},
        ],
    },

    "ai_safety_researcher": {
        "technical": [
            {"question": "Explain RLHF and its limitations.", "difficulty": "hard", "hint": "Reward hacking, distribution shift, preference inconsistency.", "frequency": "very_high"},
            {"question": "How do you evaluate model alignment?", "difficulty": "hard", "hint": "Red-teaming, benchmarks, behavioral analysis.", "frequency": "high"},
            {"question": "What are the main AI safety research directions?", "difficulty": "hard", "hint": "Alignment, interpretability, robustness, governance.", "frequency": "high"},
            {"question": "Explain Constitutional AI.", "difficulty": "hard", "hint": "Self-critique and revision based on principles.", "frequency": "high"},
            {"question": "What is the alignment tax?", "difficulty": "hard", "hint": "Performance cost of making models safer/aligned.", "frequency": "medium"},
            {"question": "How do you detect deceptive behavior in AI systems?", "difficulty": "hard", "hint": "Interpretability, behavioral testing, adversarial probing.", "frequency": "medium"},
        ],
        "behavioral": [
            {"question": "Why do you care about AI safety?", "difficulty": "medium", "hint": "Show genuine concern and understanding of risks.", "frequency": "very_high"},
            {"question": "How do you balance capability and safety research?", "difficulty": "hard", "hint": "Both are needed, responsible development.", "frequency": "high"},
        ],
    },

    "ai_infrastructure_engineer": {
        "technical": [
            {"question": "Design a multi-tenant GPU cluster for ML training.", "difficulty": "hard", "hint": "Resource isolation, scheduling, queuing, quota management.", "frequency": "very_high"},
            {"question": "How do you optimize distributed training across nodes?", "difficulty": "hard", "hint": "Data parallelism, model parallelism, communication optimization.", "frequency": "high"},
            {"question": "Design a model serving infrastructure for high availability.", "difficulty": "hard", "hint": "Load balancing, autoscaling, caching, failover.", "frequency": "high"},
            {"question": "Explain GPU memory management for ML workloads.", "difficulty": "hard", "hint": "Memory allocation, fragmentation, optimization strategies.", "frequency": "high"},
            {"question": "How do you handle ML training job scheduling?", "difficulty": "hard", "hint": "Priority, preemption, resource allocation, fairness.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design an ML platform for a large organization.", "difficulty": "hard", "hint": "Compute, storage, orchestration, monitoring, security.", "frequency": "high"},
            {"question": "Design a data lake for ML workloads.", "difficulty": "hard", "hint": "Storage, versioning, access control, processing.", "frequency": "high"},
        ],
    },

    "generative_ai_engineer": {
        "technical": [
            {"question": "Explain diffusion models and their training process.", "difficulty": "hard", "hint": "Forward (noise) + reverse (denoise) process. DDPM.", "frequency": "very_high"},
            {"question": "How do you control generation in diffusion models?", "difficulty": "hard", "hint": "Classifier-free guidance, conditioning, ControlNet.", "frequency": "high"},
            {"question": "Compare VAEs, GANs, and diffusion models.", "difficulty": "hard", "hint": "Different training objectives, quality, diversity, speed.", "frequency": "high"},
            {"question": "Explain CLIP and how it enables text-to-image generation.", "difficulty": "hard", "hint": "Contrastive learning of image-text pairs. Guides generation.", "frequency": "high"},
            {"question": "What is classifier-free guidance?", "difficulty": "hard", "hint": "Combine conditional and unconditional predictions. Improves quality.", "frequency": "high"},
            {"question": "How do you evaluate generative model quality?", "difficulty": "hard", "hint": "FID, IS, human evaluation, task-specific metrics.", "frequency": "high"},
        ],
        "system_design": [
            {"question": "Design an image generation service.", "difficulty": "hard", "hint": "Generation, safety filtering, storage, API design.", "frequency": "high"},
            {"question": "Design a video generation pipeline.", "difficulty": "hard", "hint": "Frame generation, temporal consistency, compute optimization.", "frequency": "high"},
        ],
    },

    "applied_scientist": {
        "technical": [
            {"question": "How do you balance research innovation with product requirements?", "difficulty": "medium", "hint": "Ship iteratively, research in parallel.", "frequency": "very_high"},
            {"question": "Describe a time you took a research idea to production.", "difficulty": "medium", "hint": "Cover challenges in scaling, reliability, integration.", "frequency": "high"},
            {"question": "How do you decide when to use existing methods vs developing new ones?", "difficulty": "medium", "hint": "Baseline first, iterate if needed, consider maintenance.", "frequency": "high"},
            {"question": "How do you validate research findings before productionization?", "difficulty": "medium", "hint": "A/B testing, offline evaluation, shadow mode.", "frequency": "high"},
        ],
        "behavioral": [
            {"question": "Describe a project where research and engineering had to collaborate closely.", "difficulty": "medium", "hint": "Communication, shared goals, iteration.", "frequency": "high"},
            {"question": "How do you handle time pressure while maintaining research rigor?", "difficulty": "medium", "hint": "Prioritization, MVP approach, documentation.", "frequency": "high"},
        ],
    },

    "ai_ethics_researcher": {
        "technical": [
            {"question": "How do you measure fairness in ML models?", "difficulty": "hard", "hint": "Demographic parity, equalized odds, individual fairness.", "frequency": "very_high"},
            {"question": "Explain the tradeoffs between different fairness metrics.", "difficulty": "hard", "hint": "They can be mutually exclusive. Context-dependent choice.", "frequency": "high"},
            {"question": "How do you audit an ML system for bias?", "difficulty": "hard", "hint": "Data analysis, model testing, outcome monitoring.", "frequency": "high"},
            {"question": "What is algorithmic transparency and how do you achieve it?", "difficulty": "hard", "hint": "Explainability, documentation, model cards.", "frequency": "high"},
            {"question": "How do you handle privacy in ML systems?", "difficulty": "hard", "hint": "Differential privacy, federated learning, anonymization.", "frequency": "high"},
        ],
        "behavioral": [
            {"question": "Describe a situation where ethical concerns conflicted with business goals.", "difficulty": "hard", "hint": "Show principled thinking and communication.", "frequency": "high"},
            {"question": "How do you advocate for ethical AI development?", "difficulty": "medium", "hint": "Evidence-based, stakeholder engagement, practical solutions.", "frequency": "high"},
        ],
    },

    "ai_business_analyst": {
        "technical": [
            {"question": "How do you quantify the ROI of an AI project?", "difficulty": "medium", "hint": "Cost savings, revenue impact, efficiency gains, risk reduction.", "frequency": "very_high"},
            {"question": "How do you communicate AI project risks to leadership?", "difficulty": "medium", "hint": "Clear metrics, scenarios, mitigation plans.", "frequency": "high"},
            {"question": "How do you evaluate AI vendor solutions?", "difficulty": "medium", "hint": "Capability, cost, integration, scalability, support.", "frequency": "high"},
            {"question": "How do you create an AI roadmap for an organization?", "difficulty": "hard", "hint": "Current state, goals, prioritization, dependencies.", "frequency": "high"},
        ],
        "behavioral": [
            {"question": "Describe a time you had to translate technical AI concepts for executives.", "difficulty": "medium", "hint": "Simplification, business impact, analogies.", "frequency": "high"},
            {"question": "How do you handle pushback on AI investment recommendations?", "difficulty": "medium", "hint": "Data-driven arguments, address concerns, alternatives.", "frequency": "high"},
        ],
    },
})


# ============================================
# COMPANY-SPECIFIC QUESTION BANKS - EXPANDED
# ============================================

COMPANY_QUESTIONS = {
    "google": {
        "name": "Google AI",
        "logo": "🔍",
        "description": "Google AI / Google Brain / DeepMind interview questions",
        "technical": [
            {"question": "Given a binary tree, find the maximum path sum (path may start/end at any node).", "difficulty": "hard", "hint": "DFS with global max. Return max single path from each node.", "frequency": "high", "category": "coding"},
            {"question": "Given an encoded string like '3[a2[c]]', return the decoded string 'accaccacc'.", "difficulty": "medium", "hint": "Stack-based approach. Handle nested brackets.", "frequency": "high", "category": "coding"},
            {"question": "Implement a decision tree classifier from scratch.", "difficulty": "hard", "hint": "Information gain or Gini impurity. Recursive splitting.", "frequency": "medium", "category": "coding"},
            {"question": "Design a system to detect offensive multimedia/ad content at Google scale.", "difficulty": "hard", "hint": "Multimodal ML, ensemble models, human review pipeline.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design autocomplete/spell check on mobile.", "difficulty": "hard", "hint": "Trie, language model, personalization, latency optimization.", "frequency": "high", "category": "system_design"},
            {"question": "Design email autocomplete/automatic responses (Gmail Smart Compose).", "difficulty": "hard", "hint": "Seq2seq, personalization, real-time inference.", "frequency": "high", "category": "system_design"},
            {"question": "Design YouTube recommendation system.", "difficulty": "hard", "hint": "Two-tower model, candidate generation + ranking, embeddings.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design Google Photos search and organization.", "difficulty": "hard", "hint": "Face recognition, object detection, embeddings, clustering.", "frequency": "high", "category": "system_design"},
            {"question": "Explain the bias-variance tradeoff with concrete examples.", "difficulty": "medium", "hint": "High bias: underfitting. High variance: overfitting.", "frequency": "very_high", "category": "ml_concepts"},
            {"question": "What are loss functions for RNN-based models and their optimization?", "difficulty": "hard", "hint": "Cross-entropy, CTC loss, attention mechanisms.", "frequency": "medium", "category": "ml_concepts"},
            {"question": "Explain Neural Networks, Gradient Boosting, SVM, Random Forest - when to use each?", "difficulty": "medium", "hint": "Consider data size, interpretability, feature engineering needs.", "frequency": "high", "category": "ml_concepts"},
            {"question": "How would you design a system to reduce latency in Google Search?", "difficulty": "hard", "hint": "Caching, precomputation, model distillation, edge serving.", "frequency": "high", "category": "system_design"},
            {"question": "Design a real-time translation system for Google Translate.", "difficulty": "hard", "hint": "NMT, streaming, quality estimation, low-latency serving.", "frequency": "high", "category": "system_design"},
        ],
        "behavioral": [
            {"question": "Why Google? What's your favorite Google product and how would you improve it?", "difficulty": "medium", "hint": "Show product sense and specific improvement ideas.", "frequency": "very_high"},
            {"question": "Describe an ML project you worked on. What were the challenges and impact?", "difficulty": "medium", "hint": "STAR format. Quantify impact.", "frequency": "very_high"},
            {"question": "Explain a complex ML concept to a non-technical audience.", "difficulty": "medium", "hint": "Use analogies, avoid jargon, focus on intuition.", "frequency": "high"},
            {"question": "Tell me about a time you resolved a team conflict.", "difficulty": "medium", "hint": "Show empathy and collaboration.", "frequency": "high"},
            {"question": "Describe a time you had to make a decision with ambiguous requirements.", "difficulty": "medium", "hint": "Show structured thinking and risk management.", "frequency": "high"},
        ],
    },
    
    "meta": {
        "name": "Meta AI",
        "logo": "📱",
        "description": "Meta (Facebook) AI / FAIR interview questions",
        "technical": [
            {"question": "Design a recommendation engine at Meta scale (billions of users).", "difficulty": "hard", "hint": "Candidate generation, real-time ranking, feature store, CTR monitoring.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design a feature store for large-scale ML.", "difficulty": "hard", "hint": "Offline/online stores, low-latency retrieval, point-in-time correctness.", "frequency": "very_high", "category": "system_design"},
            {"question": "How would you handle model drift at scale?", "difficulty": "hard", "hint": "Detection, retraining pipelines, monitoring offline/online metrics.", "frequency": "high", "category": "system_design"},
            {"question": "Design an ads/real-time bidding system with ML.", "difficulty": "hard", "hint": "Low-latency personalization, A/B testing, budget pacing.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design a conversational AI for Messenger.", "difficulty": "hard", "hint": "Multi-turn handling, low-latency NLP, bias monitoring.", "frequency": "high", "category": "system_design"},
            {"question": "Design a feed ranking system for Facebook/Instagram.", "difficulty": "hard", "hint": "Multi-objective ranking, engagement prediction, diversity.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design an integrity system to detect fake accounts.", "difficulty": "hard", "hint": "Behavioral signals, graph analysis, adversarial robustness.", "frequency": "high", "category": "system_design"},
            {"question": "Implement LRU cache with O(1) operations.", "difficulty": "medium", "hint": "HashMap + Doubly linked list.", "frequency": "very_high", "category": "coding"},
            {"question": "Find median from data stream.", "difficulty": "hard", "hint": "Two heaps: max-heap for lower half, min-heap for upper half.", "frequency": "high", "category": "coding"},
            {"question": "Serialize and deserialize a binary tree.", "difficulty": "hard", "hint": "BFS or DFS traversal with null markers.", "frequency": "high", "category": "coding"},
        ],
        "behavioral": [
            {"question": "Why Meta? How would you use ML to improve Meta products?", "difficulty": "medium", "hint": "Connect to Meta's mission and specific products.", "frequency": "high"},
            {"question": "Tell me about a time you shipped an ML product end-to-end.", "difficulty": "medium", "hint": "Cover data, modeling, deployment, monitoring.", "frequency": "high"},
            {"question": "Describe a time you had to move fast while maintaining quality.", "difficulty": "medium", "hint": "Meta's 'Move Fast' culture. Balance speed and quality.", "frequency": "high"},
        ],
    },
    
    "openai": {
        "name": "OpenAI",
        "logo": "🤖",
        "description": "OpenAI interview questions for AI/ML roles",
        "technical": [
            {"question": "Implement an LRU cache with persistence.", "difficulty": "hard", "hint": "HashMap + DLL, add file/DB persistence layer.", "frequency": "very_high", "category": "coding"},
            {"question": "Implement an in-memory database with transactions.", "difficulty": "hard", "hint": "Key-value store, transaction log, commit/rollback.", "frequency": "high", "category": "coding"},
            {"question": "Design a webhook delivery system (components, sharding, failures).", "difficulty": "hard", "hint": "Queue-based, retry logic, dead-letter queue, monitoring.", "frequency": "high", "category": "system_design"},
            {"question": "Design an LLM-powered enterprise search system.", "difficulty": "hard", "hint": "RAG, hybrid search, access control, caching.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design a system to deploy/monitor ML models in production.", "difficulty": "hard", "hint": "Model registry, serving infra, metrics, alerting.", "frequency": "high", "category": "system_design"},
            {"question": "Design a GPU scheduling system using credits.", "difficulty": "hard", "hint": "Resource allocation, preemption, fairness, quota tracking.", "frequency": "high", "category": "system_design"},
            {"question": "Design the ChatGPT API rate limiting and quota system.", "difficulty": "hard", "hint": "Token counting, rate limiting, fair usage, abuse prevention.", "frequency": "high", "category": "system_design"},
            {"question": "Compute KL divergence for random variables.", "difficulty": "hard", "hint": "KL(P||Q) = Σ P(x) log(P(x)/Q(x)). Measure distribution difference.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Explain backpropagation in neural networks with math.", "difficulty": "medium", "hint": "Chain rule, compute gradients layer by layer.", "frequency": "high", "category": "ml_concepts"},
            {"question": "If classifier accuracy is 1, what are the bounds on loss for a training example?", "difficulty": "hard", "hint": "Loss can still be positive due to margin/confidence.", "frequency": "medium", "category": "ml_concepts"},
            {"question": "Explain RLHF and its challenges.", "difficulty": "hard", "hint": "Reward modeling, policy optimization, reward hacking.", "frequency": "very_high", "category": "ml_concepts"},
        ],
        "behavioral": [
            {"question": "Why OpenAI? How do you think about AI safety?", "difficulty": "medium", "hint": "Show alignment with mission, understanding of risks.", "frequency": "very_high"},
            {"question": "What's your most proud project/accomplishment?", "difficulty": "medium", "hint": "Technical depth + impact + learning.", "frequency": "high"},
            {"question": "How do you balance innovation with ethical considerations in AI?", "difficulty": "hard", "hint": "Show nuanced thinking about tradeoffs.", "frequency": "high"},
            {"question": "Describe a time you changed your mind based on new evidence.", "difficulty": "medium", "hint": "Show intellectual humility and adaptability.", "frequency": "high"},
        ],
    },
    
    "anthropic": {
        "name": "Anthropic",
        "logo": "🧠",
        "description": "Anthropic interview questions - AI safety focused",
        "technical": [
            {"question": "Implement an LRU Cache and make it persistent.", "difficulty": "hard", "hint": "HashMap + DLL + file/DB backing.", "frequency": "very_high", "category": "coding"},
            {"question": "Design a rate limiter or producer-consumer system.", "difficulty": "hard", "hint": "Token bucket, sliding window, queue-based.", "frequency": "high", "category": "coding"},
            {"question": "Develop a banking app: record deposits/transfers and compute metrics.", "difficulty": "hard", "hint": "OOP design, transactions, aggregations.", "frequency": "high", "category": "coding"},
            {"question": "Design an API for an LLM with a safety layer (Constitutional AI).", "difficulty": "hard", "hint": "Input/output filtering, red-teaming, monitoring.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design a Claude chat service for multi-question handling.", "difficulty": "hard", "hint": "Context management, streaming, rate limiting.", "frequency": "high", "category": "system_design"},
            {"question": "System for safe AI model deployment in production (guardrails, reliability).", "difficulty": "hard", "hint": "Safety filters, fallbacks, monitoring, human escalation.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design a system for evaluating model harmfulness.", "difficulty": "hard", "hint": "Automated testing, human evaluation, adversarial probing.", "frequency": "high", "category": "system_design"},
            {"question": "How do you evaluate creativity in generative AI?", "difficulty": "hard", "hint": "Novelty, coherence, utility. Benchmarks + human eval.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Design guardrails for ethical AI usage; handle adversarial prompts.", "difficulty": "hard", "hint": "Input validation, output filtering, red-teaming.", "frequency": "very_high", "category": "ml_concepts"},
            {"question": "Balance performance optimization with interpretability.", "difficulty": "hard", "hint": "Tradeoffs, explainability methods, use-case dependent.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Explain Constitutional AI and how it differs from RLHF.", "difficulty": "hard", "hint": "Self-critique, principle-based revision, less human feedback needed.", "frequency": "high", "category": "ml_concepts"},
        ],
        "behavioral": [
            {"question": "Why Anthropic? What draws you to AI safety?", "difficulty": "medium", "hint": "Show genuine interest in safety research.", "frequency": "very_high"},
            {"question": "How do you ensure safe AI deployment or mitigate risks in projects?", "difficulty": "hard", "hint": "Concrete examples of safety considerations.", "frequency": "high"},
            {"question": "Present your research: explain methods, results, limitations.", "difficulty": "hard", "hint": "Be honest about limitations, show scientific rigor.", "frequency": "high"},
            {"question": "Describe a time you identified and raised a potential risk.", "difficulty": "medium", "hint": "Show proactive risk identification.", "frequency": "high"},
        ],
    },
    
    "deepmind": {
        "name": "DeepMind",
        "logo": "🎮",
        "description": "Google DeepMind interview questions",
        "technical": [
            {"question": "Explain reinforcement learning and its applications (AlphaZero).", "difficulty": "hard", "hint": "Agent, environment, reward, policy, value function.", "frequency": "very_high", "category": "ml_concepts"},
            {"question": "What's the role of feed-forward layers in transformers?", "difficulty": "hard", "hint": "Non-linear transformation after attention. Memory storage.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Explain positional embeddings (sinusoidal vs learned).", "difficulty": "hard", "hint": "Encode position information. Sinusoidal: generalizable. Learned: flexible.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Explain layer normalization (pre vs post) for stabilizing gradients.", "difficulty": "hard", "hint": "Pre-LN: more stable training. Post-LN: original transformer.", "frequency": "high", "category": "ml_concepts"},
            {"question": "What's the difference between GANs and diffusion models?", "difficulty": "hard", "hint": "GANs: adversarial. Diffusion: iterative denoising.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Fix poor model performance (bias/variance, quantization, pruning).", "difficulty": "hard", "hint": "Diagnose first. Different fixes for different problems.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Explain Monte Carlo Tree Search (MCTS).", "difficulty": "hard", "hint": "Selection, expansion, simulation, backpropagation. Used in AlphaGo.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Distribute large-model training across multiple GPUs.", "difficulty": "hard", "hint": "Data parallelism, model parallelism, pipeline parallelism.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design an ML system for healthcare diagnostics.", "difficulty": "hard", "hint": "Data privacy, interpretability, clinical validation.", "frequency": "high", "category": "system_design"},
            {"question": "Design a game-playing AI system.", "difficulty": "hard", "hint": "Environment modeling, policy learning, search, self-play.", "frequency": "high", "category": "system_design"},
        ],
        "behavioral": [
            {"question": "Tell me about collaboration/learning from challenges.", "difficulty": "medium", "hint": "Show growth mindset and teamwork.", "frequency": "high"},
            {"question": "How do you handle feedback/research disagreements?", "difficulty": "medium", "hint": "Scientific approach, evidence-based discussion.", "frequency": "high"},
            {"question": "What research problem would you want to solve at DeepMind?", "difficulty": "hard", "hint": "Show awareness of DeepMind's research areas.", "frequency": "high"},
        ],
    },
    
    "nvidia": {
        "name": "NVIDIA",
        "logo": "🎮",
        "description": "NVIDIA AI/Deep Learning interview questions",
        "technical": [
            {"question": "Implement beam search for LLM inference; analyze time complexity.", "difficulty": "hard", "hint": "Maintain k best sequences at each step. O(k * V * L).", "frequency": "very_high", "category": "coding"},
            {"question": "Describe Mixture-of-Experts (MoE) models.", "difficulty": "hard", "hint": "Sparse activation, routing, expert networks.", "frequency": "high", "category": "ml_concepts"},
            {"question": "How does autoregressive decoding work with KV-cache?", "difficulty": "hard", "hint": "Cache key-value pairs to avoid recomputation.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Explain Low-rank adaptation (LoRA) principles.", "difficulty": "medium", "hint": "Add low-rank matrices to frozen weights. Efficient fine-tuning.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Optimize CUDA kernel for matrix multiplication.", "difficulty": "hard", "hint": "Shared memory tiling, coalesced access, warp-level ops.", "frequency": "very_high", "category": "coding"},
            {"question": "Explain warp divergence in GPU computing.", "difficulty": "hard", "hint": "Threads in warp take different paths, reducing parallelism.", "frequency": "high", "category": "technical"},
            {"question": "How do Tensor Cores work for deep learning?", "difficulty": "hard", "hint": "Mixed-precision matrix multiply-accumulate operations.", "frequency": "high", "category": "technical"},
            {"question": "Explain GPU memory hierarchy and optimization strategies.", "difficulty": "hard", "hint": "Registers > Shared > L2 > Global. Tiling, caching.", "frequency": "high", "category": "technical"},
            {"question": "How do you profile and optimize GPU workloads?", "difficulty": "hard", "hint": "Nsight, occupancy, memory bandwidth, compute utilization.", "frequency": "high", "category": "technical"},
            {"question": "Explain flash attention and its benefits.", "difficulty": "hard", "hint": "IO-aware attention. Reduces memory reads/writes.", "frequency": "high", "category": "ml_concepts"},
        ],
        "behavioral": [
            {"question": "What's your most recent invention?", "difficulty": "medium", "hint": "Show creativity and technical depth.", "frequency": "high"},
            {"question": "Time you got stuck 75% through a project?", "difficulty": "medium", "hint": "Show problem-solving and persistence.", "frequency": "high"},
            {"question": "Time you failed; key learnings?", "difficulty": "medium", "hint": "Show growth mindset and accountability.", "frequency": "high"},
            {"question": "How do you deal with ambiguity (e.g., insufficient data)?", "difficulty": "medium", "hint": "Show structured approach to uncertainty.", "frequency": "high"},
        ],
    },
    
    "amazon": {
        "name": "Amazon AI",
        "logo": "📦",
        "description": "Amazon / AWS AI interview questions",
        "technical": [
            {"question": "Design a product recommendation system for Amazon.", "difficulty": "hard", "hint": "Collaborative filtering, real-time ranking, A/B testing.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design Alexa's speech recognition and NLU pipeline.", "difficulty": "hard", "hint": "ASR, NLU, intent classification, slot filling.", "frequency": "high", "category": "system_design"},
            {"question": "Design a fraud detection system for e-commerce.", "difficulty": "hard", "hint": "Real-time, feature engineering, ensemble models.", "frequency": "high", "category": "system_design"},
            {"question": "Design a demand forecasting system for inventory.", "difficulty": "hard", "hint": "Time series, external features, hierarchical forecasting.", "frequency": "high", "category": "system_design"},
            {"question": "Design a review classification system (fake review detection).", "difficulty": "hard", "hint": "Text classification, behavioral signals, adversarial robustness.", "frequency": "high", "category": "system_design"},
            {"question": "Design Amazon Go's checkout-free shopping system.", "difficulty": "hard", "hint": "Computer vision, sensor fusion, tracking.", "frequency": "high", "category": "system_design"},
        ],
        "behavioral": [
            {"question": "Tell me about a time you had to make a decision with incomplete data.", "difficulty": "medium", "hint": "Show bias for action while managing risk.", "frequency": "very_high"},
            {"question": "Describe a time you disagreed with your manager.", "difficulty": "medium", "hint": "Show backbone and data-driven approach.", "frequency": "high"},
            {"question": "How do you prioritize competing ML projects?", "difficulty": "medium", "hint": "Customer obsession, business impact, feasibility.", "frequency": "high"},
            {"question": "Tell me about a time you simplified a complex problem.", "difficulty": "medium", "hint": "Show ability to break down complexity.", "frequency": "high"},
        ],
    },
    
    "microsoft": {
        "name": "Microsoft AI",
        "logo": "💻",
        "description": "Microsoft AI / Azure ML interview questions",
        "technical": [
            {"question": "Design Copilot for Microsoft Office (Word, Excel, etc.).", "difficulty": "hard", "hint": "Context understanding, action generation, safety.", "frequency": "very_high", "category": "system_design"},
            {"question": "Design a search engine with ML ranking (Bing).", "difficulty": "hard", "hint": "Query understanding, retrieval, learning to rank.", "frequency": "high", "category": "system_design"},
            {"question": "Design a real-time translation system for Teams.", "difficulty": "hard", "hint": "Streaming ASR, NMT, low-latency serving.", "frequency": "high", "category": "system_design"},
            {"question": "Design an AI-powered code completion system.", "difficulty": "hard", "hint": "Context extraction, model serving, personalization.", "frequency": "high", "category": "system_design"},
            {"question": "Design Azure Cognitive Services architecture.", "difficulty": "hard", "hint": "Multi-model serving, API gateway, scaling.", "frequency": "high", "category": "system_design"},
        ],
        "behavioral": [
            {"question": "How would you use AI to make Microsoft products more accessible?", "difficulty": "medium", "hint": "Show empathy and product sense.", "frequency": "high"},
            {"question": "Tell me about shipping an ML feature at scale.", "difficulty": "medium", "hint": "Cover challenges, iterations, impact.", "frequency": "high"},
            {"question": "Describe a time you had to learn something quickly to solve a problem.", "difficulty": "medium", "hint": "Show learning agility.", "frequency": "high"},
        ],
    },
    
    "tesla": {
        "name": "Tesla AI",
        "logo": "⚡",
        "description": "Tesla Autopilot / FSD interview questions",
        "technical": [
            {"question": "Design the perception system for autonomous vehicles.", "difficulty": "hard", "hint": "Multi-sensor fusion, object detection, tracking.", "frequency": "very_high", "category": "system_design"},
            {"question": "How would you improve autonomous driving in edge cases?", "difficulty": "hard", "hint": "Data collection, simulation, transfer learning.", "frequency": "high", "category": "ml_concepts"},
            {"question": "Explain end-to-end learning vs modular pipelines for self-driving.", "difficulty": "hard", "hint": "Tradeoffs: interpretability, data needs, failure modes.", "frequency": "high", "category": "ml_concepts"},
            {"question": "How do you train models on large-scale video data efficiently?", "difficulty": "hard", "hint": "Distributed training, data sampling, clip selection.", "frequency": "high", "category": "system_design"},
            {"question": "Design a system for automatic labeling of driving data.", "difficulty": "hard", "hint": "Auto-labeling, active learning, quality control.", "frequency": "high", "category": "system_design"},
            {"question": "How do you handle rare events in autonomous driving?", "difficulty": "hard", "hint": "Simulation, synthetic data, importance sampling.", "frequency": "high", "category": "ml_concepts"},
        ],
        "behavioral": [
            {"question": "Why Tesla? What excites you about autonomous driving?", "difficulty": "medium", "hint": "Show passion for the mission.", "frequency": "high"},
            {"question": "How do you work under pressure with tight deadlines?", "difficulty": "medium", "hint": "Show resilience and prioritization.", "frequency": "high"},
            {"question": "Describe a time you had to rapidly iterate on a solution.", "difficulty": "medium", "hint": "Show agility and learning.", "frequency": "high"},
        ],
    },
}


# Export functions
def get_role_questions(role_id: str) -> dict:
    """Get questions for a specific role"""
    return ROLE_QUESTIONS.get(role_id, {})

def get_company_questions(company_id: str) -> dict:
    """Get questions for a specific company"""
    return COMPANY_QUESTIONS.get(company_id, {})

def get_all_roles() -> list:
    """Get list of all roles with questions"""
    return list(ROLE_QUESTIONS.keys())

def get_all_companies() -> list:
    """Get list of all companies with questions"""
    return list(COMPANY_QUESTIONS.keys())

def count_questions() -> dict:
    """Count total questions"""
    role_count = sum(
        len(qs) for role in ROLE_QUESTIONS.values() 
        for qs in role.values()
    )
    company_count = sum(
        len(qs) for comp in COMPANY_QUESTIONS.values() 
        for k, qs in comp.items() if isinstance(qs, list)
    )
    return {
        "roles": len(ROLE_QUESTIONS),
        "companies": len(COMPANY_QUESTIONS),
        "role_questions": role_count,
        "company_questions": company_count,
        "total": role_count + company_count
    }
