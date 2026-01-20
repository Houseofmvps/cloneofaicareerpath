import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../lib/api";
import {
  MessageSquare, Brain, Code, Users, Sparkles, Loader2,
  ChevronRight, ChevronDown, CheckCircle2, XCircle, RefreshCw,
  BookOpen, Target, Lightbulb, Play, Pause, Volume2, Clock,
  ThumbsUp, ThumbsDown, RotateCcw, Star, Award, Mic, Send
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Textarea } from "../components/ui/textarea";
import { Progress } from "../components/ui/progress";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import AppNavigation from "../components/AppNavigation";

// API base URL configured in lib/api.js

// Question categories with icons
const QUESTION_CATEGORIES = [
  { id: "technical", name: "Technical", icon: Code, color: "text-blue-400 bg-blue-500/20" },
  { id: "behavioral", name: "Behavioral", icon: Users, color: "text-purple-400 bg-purple-500/20" },
  { id: "system_design", name: "System Design", icon: Brain, color: "text-emerald-400 bg-emerald-500/20" },
  { id: "coding", name: "Coding", icon: Code, color: "text-amber-400 bg-amber-500/20" },
  { id: "ml_concepts", name: "ML Concepts", icon: Sparkles, color: "text-pink-400 bg-pink-500/20" },
];

// Difficulty levels
const DIFFICULTY_LEVELS = [
  { id: "easy", name: "Easy", color: "text-green-400" },
  { id: "medium", name: "Medium", color: "text-yellow-400" },
  { id: "hard", name: "Hard", color: "text-red-400" },
];

// Question Card Component
const QuestionCard = ({ question, index, onAnswer, onGetHint, onGetFeedback, isExpanded, onToggle }) => {
  const [userAnswer, setUserAnswer] = useState("");
  const [showHint, setShowHint] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [rating, setRating] = useState(null);

  const category = QUESTION_CATEGORIES.find(c => c.id === question.category);
  const difficulty = DIFFICULTY_LEVELS.find(d => d.id === question.difficulty);

  const handleGetFeedback = async () => {
    if (!userAnswer.trim()) {
      toast.error("Please write your answer first");
      return;
    }
    setLoading(true);
    try {
      const result = await onGetFeedback(question, userAnswer);
      setFeedback(result);
    } catch (error) {
      toast.error("Failed to get feedback");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="glass rounded-xl overflow-hidden"
    >
      {/* Question Header */}
      <div
        className="p-4 cursor-pointer flex items-center justify-between hover:bg-white/5"
        onClick={onToggle}
      >
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg ${category?.color} flex items-center justify-center`}>
            {category && <category.icon className="w-5 h-5" />}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-muted-foreground">Q{index + 1}</span>
              <span className={`text-xs ${difficulty?.color}`}>{difficulty?.name}</span>
              {question.company && (
                <span className="text-xs bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full">
                  {question.company}
                </span>
              )}
            </div>
            <h3 className="font-medium mt-1 line-clamp-2">{question.question}</h3>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {feedback && (
            <span className={`text-xs px-2 py-1 rounded-full ${feedback.score >= 80 ? "bg-green-500/20 text-green-400" :
                feedback.score >= 60 ? "bg-yellow-500/20 text-yellow-400" :
                  "bg-red-500/20 text-red-400"
              }`}>
              {feedback.score}%
            </span>
          )}
          {isExpanded ? (
            <ChevronDown className="w-5 h-5" />
          ) : (
            <ChevronRight className="w-5 h-5" />
          )}
        </div>
      </div>

      {/* Expanded Content */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-white/10"
          >
            <div className="p-4 space-y-4">
              {/* Hint Section */}
              {question.hint && (
                <div className="flex items-start gap-2">
                  <button
                    onClick={() => setShowHint(!showHint)}
                    className="text-sm text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
                  >
                    <Lightbulb className="w-4 h-4" />
                    {showHint ? "Hide Hint" : "Show Hint"}
                  </button>
                  {showHint && (
                    <motion.p
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="text-sm text-muted-foreground bg-indigo-500/10 p-2 rounded-lg flex-1"
                    >
                      💡 {question.hint}
                    </motion.p>
                  )}
                </div>
              )}

              {/* Answer Textarea */}
              <div>
                <label className="text-sm font-medium text-muted-foreground mb-2 block">
                  Your Answer:
                </label>
                <Textarea
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Type your answer here... Be specific and use concrete examples."
                  className="min-h-[150px] bg-white/5 border-white/10"
                  data-testid={`answer-input-${index}`}
                />
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-3">
                <Button
                  onClick={handleGetFeedback}
                  disabled={loading || !userAnswer.trim()}
                  className="btn-primary"
                  data-testid={`get-feedback-${index}`}
                >
                  {loading ? (
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  ) : (
                    <Sparkles className="w-4 h-4 mr-2" />
                  )}
                  Get AI Feedback
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setUserAnswer("")}
                  disabled={!userAnswer}
                >
                  <RotateCcw className="w-4 h-4 mr-2" />
                  Clear
                </Button>
              </div>

              {/* AI Feedback */}
              {feedback && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-4 space-y-4"
                >
                  {/* Score */}
                  <div className="flex items-center gap-4">
                    <div className={`text-3xl font-bold ${feedback.score >= 80 ? "text-green-400" :
                        feedback.score >= 60 ? "text-yellow-400" :
                          "text-red-400"
                      }`}>
                      {feedback.score}/100
                    </div>
                    <div className="flex-1">
                      <Progress value={feedback.score} className="h-2" />
                    </div>
                  </div>

                  {/* Strengths */}
                  {feedback.strengths?.length > 0 && (
                    <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/20">
                      <h4 className="font-medium text-green-400 flex items-center gap-2 mb-2">
                        <ThumbsUp className="w-4 h-4" /> Strengths
                      </h4>
                      <ul className="text-sm text-green-300 space-y-1">
                        {feedback.strengths.map((s, i) => (
                          <li key={i}>• {s}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Improvements */}
                  {feedback.improvements?.length > 0 && (
                    <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20">
                      <h4 className="font-medium text-amber-400 flex items-center gap-2 mb-2">
                        <Lightbulb className="w-4 h-4" /> Areas to Improve
                      </h4>
                      <ul className="text-sm text-amber-300 space-y-1">
                        {feedback.improvements.map((s, i) => (
                          <li key={i}>• {s}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Sample Answer */}
                  {feedback.sample_answer && (
                    <div className="p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/20">
                      <h4 className="font-medium text-indigo-400 flex items-center gap-2 mb-2">
                        <Star className="w-4 h-4" /> Example Strong Answer
                      </h4>
                      <p className="text-sm text-indigo-200">{feedback.sample_answer}</p>
                    </div>
                  )}
                </motion.div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default function InterviewPrepPage() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [roles, setRoles] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [selectedRole, setSelectedRole] = useState("");
  const [selectedCompany, setSelectedCompany] = useState("");
  const [selectedCategories, setSelectedCategories] = useState(["technical", "behavioral", "system_design", "coding", "ml_concepts"]);
  const [questions, setQuestions] = useState([]);
  const [expandedQuestion, setExpandedQuestion] = useState(null);
  const [practiceHistory, setPracticeHistory] = useState([]);
  const [stats, setStats] = useState({ total_practiced: 0, avg_score: 0, streak: 0 });

  useEffect(() => {
    fetchRoles();
    fetchCompanies();
    fetchPracticeHistory();
  }, []);

  const fetchRoles = async () => {
    try {
      const response = await api.get(`/roles`);
      setRoles(response.data.roles || []);
      if (response.data.roles?.length > 0) {
        setSelectedRole(response.data.roles[0].id);
      }
    } catch (error) {
      console.error("Failed to fetch roles:", error);
    }
  };

  const fetchCompanies = async () => {
    try {
      const response = await api.get(`/interview-prep/companies`);
      setCompanies(response.data.companies || []);
    } catch (error) {
      console.error("Failed to fetch companies:", error);
    }
  };

  const fetchPracticeHistory = async () => {
    try {
      const response = await api.get(`/interview-prep/history`);
      setPracticeHistory(response.data.history || []);
      setStats(response.data.stats || { total_practiced: 0, avg_score: 0, streak: 0 });
    } catch (error) {
      console.error("Failed to fetch history:", error);
    }
  };

  const generateQuestions = async () => {
    if (!selectedRole) {
      toast.error("Please select a target role");
      return;
    }
    setGenerating(true);
    try {
      const response = await api.post(`/interview-prep/generate`, {
        role_id: selectedRole,
        categories: selectedCategories,
        count: 25,  // More questions for comprehensive practice
        company: selectedCompany || null
      });
      setQuestions(response.data.questions || []);
      setExpandedQuestion(0);

      const companyName = selectedCompany ? companies.find(c => c.id === selectedCompany)?.name : null;
      const msg = companyName
        ? `Generated ${response.data.questions?.length || 0} questions including ${companyName}-style questions!`
        : `Generated ${response.data.questions?.length || 0} interview questions!`;
      toast.success(msg);
    } catch (error) {
      toast.error("Failed to generate questions");
      console.error(error);
    } finally {
      setGenerating(false);
    }
  };

  const getFeedback = async (question, answer) => {
    const response = await api.post(`/interview-prep/feedback`, {
      question: question.question,
      answer: answer,
      role_id: selectedRole,
      category: question.category
    });

    // Save to history
    fetchPracticeHistory();

    return response.data;
  };

  const toggleCategory = (catId) => {
    setSelectedCategories(prev =>
      prev.includes(catId)
        ? prev.filter(c => c !== catId)
        : [...prev, catId]
    );
  };

  const selectedRoleData = roles.find(r => r.id === selectedRole);

  return (
    <div className="min-h-screen bg-background noise-bg">
      <AppNavigation />

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/30 mb-4">
                <MessageSquare className="w-4 h-4 text-purple-400" />
                <span className="text-sm text-purple-300">Interview Prep</span>
              </div>
              <h1 className="text-3xl font-bold">AI Interview Coach</h1>
              <p className="text-muted-foreground">
                Practice with role-specific questions. Get instant AI feedback on your answers.
              </p>
            </div>

            {/* Stats */}
            <div className="glass rounded-xl p-4 text-center">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <div className="text-2xl font-bold text-indigo-400">{stats.total_practiced}</div>
                  <div className="text-xs text-muted-foreground">Practiced</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-emerald-400">{stats.avg_score}%</div>
                  <div className="text-xs text-muted-foreground">Avg Score</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-amber-400">{stats.streak}🔥</div>
                  <div className="text-xs text-muted-foreground">Streak</div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Panel - Setup */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            {/* Role Selection */}
            <div className="glass rounded-2xl p-6">
              <h2 className="font-semibold mb-4 flex items-center gap-2">
                <Target className="w-5 h-5 text-indigo-400" />
                Target Role
              </h2>
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="w-full p-3 rounded-lg bg-white/5 border border-white/10 text-foreground"
                data-testid="interview-role-select"
              >
                {roles.map((role) => (
                  <option key={role.id} value={role.id} className="bg-gray-900">
                    {role.name}
                  </option>
                ))}
              </select>

              {selectedRoleData && (
                <div className="mt-4 p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/20">
                  <div className="text-sm text-indigo-300 mb-2">Key Skills to Know:</div>
                  <div className="flex flex-wrap gap-1">
                    {selectedRoleData.top_skills?.slice(0, 6).map((skill, i) => (
                      <span key={i} className="text-xs bg-indigo-500/20 px-2 py-1 rounded-full">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Company-Specific Questions */}
            <div className="glass rounded-2xl p-6">
              <h2 className="font-semibold mb-4 flex items-center gap-2">
                <Award className="w-5 h-5 text-amber-400" />
                Company-Style Questions
              </h2>
              <select
                value={selectedCompany}
                onChange={(e) => setSelectedCompany(e.target.value)}
                className="w-full p-3 rounded-lg bg-white/5 border border-white/10 text-foreground"
                data-testid="interview-company-select"
              >
                <option value="" className="bg-gray-900">No specific company</option>
                {companies.map((company) => (
                  <option key={company.id} value={company.id} className="bg-gray-900">
                    {company.logo} {company.name}
                  </option>
                ))}
              </select>
              {selectedCompany && (
                <p className="mt-2 text-xs text-muted-foreground">
                  Includes real questions from {companies.find(c => c.id === selectedCompany)?.name} interviews
                </p>
              )}
            </div>

            {/* Question Categories */}
            <div className="glass rounded-2xl p-6">
              <h2 className="font-semibold mb-4 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-purple-400" />
                Question Types
              </h2>
              <div className="space-y-2">
                {QUESTION_CATEGORIES.map((cat) => (
                  <button
                    key={cat.id}
                    onClick={() => toggleCategory(cat.id)}
                    className={`w-full p-3 rounded-lg border transition-all flex items-center gap-3 ${selectedCategories.includes(cat.id)
                        ? "bg-white/10 border-indigo-500/50"
                        : "bg-white/5 border-white/10 hover:border-white/20"
                      }`}
                    data-testid={`category-${cat.id}`}
                  >
                    <div className={`w-8 h-8 rounded-lg ${cat.color} flex items-center justify-center`}>
                      <cat.icon className="w-4 h-4" />
                    </div>
                    <span className="flex-1 text-left">{cat.name}</span>
                    {selectedCategories.includes(cat.id) && (
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Generate Button */}
            <Button
              onClick={generateQuestions}
              disabled={generating || !selectedRole || selectedCategories.length === 0}
              className="w-full btn-primary py-6 text-lg"
              data-testid="generate-questions-btn"
            >
              {generating ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Generating Questions...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 mr-2" />
                  Generate {selectedCategories.length * 2} Questions
                </>
              )}
            </Button>

            {/* Tips */}
            <div className="glass rounded-2xl p-6">
              <h3 className="font-medium text-amber-400 flex items-center gap-2 mb-3">
                <Lightbulb className="w-4 h-4" />
                Interview Tips
              </h3>
              <ul className="text-sm text-muted-foreground space-y-2">
                <li>• Use the STAR method for behavioral questions</li>
                <li>• Think out loud during technical questions</li>
                <li>• Ask clarifying questions before diving in</li>
                <li>• Practice explaining complex concepts simply</li>
                <li>• Prepare 2-3 questions to ask the interviewer</li>
              </ul>
            </div>
          </motion.div>

          {/* Right Panel - Questions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-2 space-y-4"
          >
            {questions.length === 0 ? (
              <div className="glass rounded-2xl p-12 text-center">
                <MessageSquare className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
                <h3 className="text-xl font-semibold mb-2">Ready to Practice?</h3>
                <p className="text-muted-foreground mb-6">
                  Select your target role and question types, then click Generate Questions to start practicing.
                </p>
                <div className="grid grid-cols-2 gap-4 max-w-md mx-auto text-left">
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                    <div className="text-2xl mb-2">🎯</div>
                    <div className="font-medium">Role-Specific</div>
                    <div className="text-xs text-muted-foreground">Questions tailored to your target role</div>
                  </div>
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                    <div className="text-2xl mb-2">🤖</div>
                    <div className="font-medium">AI Feedback</div>
                    <div className="text-xs text-muted-foreground">Get instant scoring and tips</div>
                  </div>
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                    <div className="text-2xl mb-2">💡</div>
                    <div className="font-medium">Sample Answers</div>
                    <div className="text-xs text-muted-foreground">Learn from example responses</div>
                  </div>
                  <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                    <div className="text-2xl mb-2">📈</div>
                    <div className="font-medium">Track Progress</div>
                    <div className="text-xs text-muted-foreground">See your improvement over time</div>
                  </div>
                </div>
              </div>
            ) : (
              <>
                {/* Progress Bar */}
                <div className="glass rounded-xl p-4 flex items-center gap-4">
                  <div className="text-sm text-muted-foreground">
                    {questions.length} questions generated
                  </div>
                  <div className="flex-1">
                    <Progress value={(expandedQuestion + 1) / questions.length * 100} className="h-2" />
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={generateQuestions}
                    disabled={generating}
                  >
                    <RefreshCw className={`w-4 h-4 mr-2 ${generating ? "animate-spin" : ""}`} />
                    Refresh
                  </Button>
                </div>

                {/* Question List */}
                <div className="space-y-4">
                  {questions.map((question, index) => (
                    <QuestionCard
                      key={index}
                      question={question}
                      index={index}
                      isExpanded={expandedQuestion === index}
                      onToggle={() => setExpandedQuestion(expandedQuestion === index ? null : index)}
                      onGetFeedback={getFeedback}
                    />
                  ))}
                </div>
              </>
            )}
          </motion.div>
        </div>
      </main>
    </div>
  );
}
