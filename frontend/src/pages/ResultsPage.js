import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import axios from "axios";
import {
  Brain, ChevronLeft, Target, FileText, TrendingUp, AlertTriangle,
  CheckCircle2, XCircle, Clock, DollarSign, BookOpen, Copy, Download,
  ChevronDown, ChevronUp, Sparkles, Award, Zap, Lightbulb, Users
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Progress } from "../components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import {
  RadialBarChart, RadialBar, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip
} from "recharts";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function ResultsPage() {
  const { analysisId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [expandedWeeks, setExpandedWeeks] = useState([1]);

  useEffect(() => {
    fetchAnalysis();
  }, [analysisId]);

  const fetchAnalysis = async () => {
    try {
      const response = await axios.get(`${API}/analyses/${analysisId}`);
      setAnalysis(response.data);
    } catch (error) {
      toast.error("Failed to load analysis");
      navigate("/dashboard");
    } finally {
      setLoading(false);
    }
  };

  const toggleWeek = (week) => {
    setExpandedWeeks(prev =>
      prev.includes(week) ? prev.filter(w => w !== week) : [...prev, week]
    );
  };

  const copyToClipboard = (text, type) => {
    navigator.clipboard.writeText(text);
    toast.success(`${type} copied to clipboard!`);
  };

  const getRatingStyle = (rating) => {
    switch (rating?.toUpperCase()) {
      case "EXCELLENT": return "score-excellent";
      case "GOOD": return "score-good";
      case "FEASIBLE": return "score-feasible";
      case "CHALLENGING": return "score-challenging";
      default: return "";
    }
  };

  const getSkillRatingStyle = (rating) => {
    switch (rating?.toUpperCase()) {
      case "VERY_HIGH": return "skill-very-high";
      case "HIGH": return "skill-high";
      case "MEDIUM": return "skill-medium";
      case "LOW": return "skill-low";
      default: return "";
    }
  };

  const getPriorityStyle = (priority) => {
    switch (priority?.toUpperCase()) {
      case "CRITICAL": return "priority-critical";
      case "HIGH": return "priority-high";
      case "MEDIUM": return "priority-medium";
      default: return "";
    }
  };

  const getATSScoreColor = (score) => {
    if (score >= 75) return "#10b981";
    if (score >= 60) return "#f59e0b";
    if (score >= 40) return "#f97316";
    return "#ef4444";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (!analysis) return null;

  const { analysis_result: result, target_role } = analysis;

  const atsChartData = [
    { name: "ATS Score", value: result?.ats_score?.score || 0, fill: getATSScoreColor(result?.ats_score?.score || 0) }
  ];

  return (
    <div className="min-h-screen bg-background noise-bg">
      {/* Header */}
      <header className="glass-heavy border-b border-white/5 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">CareerLift</span>
            </Link>

            <div className="flex items-center gap-4">
              <Button variant="ghost" onClick={() => navigate("/dashboard")} data-testid="results-back-btn">
                <ChevronLeft className="w-4 h-4 mr-1" />
                Dashboard
              </Button>
              <Button className="btn-primary" onClick={() => navigate("/analyze")} data-testid="results-new-analysis-btn">
                New Analysis
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Target Role Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-2xl p-8 mb-8"
        >
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <div className="text-sm text-indigo-400 mb-2">Analysis Results for</div>
              <h1 className="text-3xl font-bold mb-2">{target_role?.name}</h1>
              <p className="text-muted-foreground">{target_role?.description}</p>
            </div>
            <div className={`
              px-6 py-3 rounded-full text-xl font-bold border-2
              ${getRatingStyle(result?.career_fit?.rating)}
            `} data-testid="career-fit-rating">
              {result?.career_fit?.rating || "N/A"}
            </div>
          </div>
        </motion.div>

        {/* Overview Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {/* Career Fit Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="glass rounded-2xl p-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <Award className="w-5 h-5 text-indigo-400" />
              <h3 className="font-semibold">Career Fit Score</h3>
            </div>
            <div className="text-5xl font-bold gradient-text mb-2">
              {result?.career_fit?.score || 0}%
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              {result?.career_fit?.explanation?.slice(0, 100)}...
            </p>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <div className="text-muted-foreground">Timeline</div>
                <div className="flex items-center gap-1 font-medium">
                  <Clock className="w-4 h-4 text-amber-400" />
                  {result?.career_fit?.timeline_weeks || target_role?.transition_weeks} weeks
                </div>
              </div>
              <div>
                <div className="text-muted-foreground">Salary</div>
                <div className="flex items-center gap-1 font-medium">
                  <DollarSign className="w-4 h-4 text-emerald-400" />
                  {result?.career_fit?.salary_if_hired_today || target_role?.salary_range}
                </div>
              </div>
            </div>
          </motion.div>

          {/* ATS Score Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="glass rounded-2xl p-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-emerald-400" />
              <h3 className="font-semibold">ATS Compatibility</h3>
            </div>
            <div className="h-32">
              <ResponsiveContainer width="100%" height="100%">
                <RadialBarChart
                  cx="50%"
                  cy="50%"
                  innerRadius="60%"
                  outerRadius="100%"
                  data={atsChartData}
                  startAngle={180}
                  endAngle={0}
                >
                  <RadialBar
                    dataKey="value"
                    cornerRadius={10}
                    background={{ fill: "#1f2937" }}
                  />
                </RadialBarChart>
              </ResponsiveContainer>
            </div>
            <div className="text-center -mt-8">
              <span className="text-4xl font-bold" style={{ color: getATSScoreColor(result?.ats_score?.score || 0) }}>
                {result?.ats_score?.score || 0}
              </span>
              <span className="text-muted-foreground">/100</span>
            </div>
          </motion.div>

          {/* Quick Stats Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass rounded-2xl p-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <Zap className="w-5 h-5 text-amber-400" />
              <h3 className="font-semibold">Quick Stats</h3>
            </div>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-muted-foreground">Transferable Skills</span>
                  <span className="font-medium">{result?.transferable_skills?.length || 0}</span>
                </div>
                <Progress value={Math.min((result?.transferable_skills?.length || 0) * 10, 100)} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-muted-foreground">Skill Gaps</span>
                  <span className="font-medium">{result?.skill_gaps?.length || 0}</span>
                </div>
                <Progress value={Math.min((result?.skill_gaps?.length || 0) * 15, 100)} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-muted-foreground">Learning Path</span>
                  <span className="font-medium">{result?.learning_path?.total_weeks || 16} weeks</span>
                </div>
                <Progress value={100} className="h-2" />
              </div>
            </div>
          </motion.div>
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="skills" className="space-y-6">
          <TabsList className="glass p-1 rounded-xl">
            <TabsTrigger value="skills" className="rounded-lg" data-testid="tab-skills">
              <TrendingUp className="w-4 h-4 mr-2" />
              Skills Analysis
            </TabsTrigger>
            <TabsTrigger value="learning" className="rounded-lg" data-testid="tab-learning">
              <BookOpen className="w-4 h-4 mr-2" />
              Learning Path
            </TabsTrigger>
            <TabsTrigger value="cv" className="rounded-lg" data-testid="tab-cv">
              <FileText className="w-4 h-4 mr-2" />
              Resume Versions
            </TabsTrigger>
            <TabsTrigger value="next" className="rounded-lg" data-testid="tab-next">
              <Target className="w-4 h-4 mr-2" />
              Next Steps
            </TabsTrigger>
          </TabsList>

          {/* Skills Analysis Tab */}
          <TabsContent value="skills" className="space-y-6">
            {/* ATS Details */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass rounded-2xl p-6"
            >
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5 text-emerald-400" />
                ATS Score Breakdown
              </h3>
              <p className="text-muted-foreground mb-4">{result?.ats_score?.explanation}</p>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-emerald-400 mb-3 flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4" /> What Helps Your Score
                  </h4>
                  <ul className="space-y-2">
                    {result?.ats_score?.helps_score?.map((item, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-red-400 mb-3 flex items-center gap-2">
                    <XCircle className="w-4 h-4" /> What Hurts Your Score
                  </h4>
                  <ul className="space-y-2">
                    {result?.ats_score?.hurts_score?.map((item, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm">
                        <XCircle className="w-4 h-4 text-red-400 mt-0.5 flex-shrink-0" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div className="mt-6 pt-6 border-t border-white/10">
                <h4 className="font-medium mb-3">Quick Fixes</h4>
                <div className="grid md:grid-cols-2 gap-3">
                  {result?.ats_score?.quick_fixes?.map((fix, i) => (
                    <div key={i} className="flex items-start gap-2 p-3 rounded-lg bg-white/5">
                      <Lightbulb className="w-4 h-4 text-amber-400 mt-0.5 flex-shrink-0" />
                      <span className="text-sm">{fix}</span>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>

            {/* Transferable Skills */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="glass rounded-2xl p-6"
            >
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-indigo-400" />
                Transferable Skills
              </h3>
              <div className="grid md:grid-cols-2 gap-4">
                {result?.transferable_skills?.map((skill, i) => (
                  <div key={i} className={`p-4 rounded-xl ${getSkillRatingStyle(skill.rating)}`}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">{skill.skill}</span>
                      <span className="text-xs px-2 py-1 rounded-full bg-white/10">{skill.rating}</span>
                    </div>
                    <p className="text-sm opacity-80">{skill.explanation}</p>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Skill Gaps */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="glass rounded-2xl p-6"
            >
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-amber-400" />
                Skill Gaps to Address
              </h3>
              <div className="space-y-4">
                {result?.skill_gaps?.map((gap, i) => (
                  <div key={i} className={`p-4 rounded-xl border ${getPriorityStyle(gap.priority)}`}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-lg">{gap.skill}</span>
                      <span className="text-xs px-2 py-1 rounded-full bg-white/10">{gap.priority}</span>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm mb-3">
                      <div>
                        <span className="text-muted-foreground">Time to Learn</span>
                        <div className="font-medium">{gap.months_to_learn} months</div>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Difficulty</span>
                        <div className="font-medium">{gap.difficulty}</div>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Resources</span>
                        <div className="font-medium">{gap.resources?.length || 0} available</div>
                      </div>
                    </div>
                    {gap.resources?.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {gap.resources.map((resource, j) => (
                          <span key={j} className="text-xs px-2 py-1 rounded-full bg-white/5">
                            {resource}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </motion.div>
          </TabsContent>

          {/* Learning Path Tab */}
          <TabsContent value="learning" className="space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass rounded-2xl p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <BookOpen className="w-5 h-5 text-purple-400" />
                    {result?.learning_path?.total_weeks || 16}-Week Learning Path
                  </h3>
                  <p className="text-muted-foreground">
                    {result?.learning_path?.hours_per_week || 15} hours/week commitment
                  </p>
                </div>
              </div>

              <div className="relative">
                <div className="timeline-line"></div>
                <div className="space-y-4 pl-10">
                  {result?.learning_path?.weeks?.map((week, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="relative"
                    >
                      <div className={`timeline-dot ${i === 0 ? 'current' : ''}`}></div>
                      <div
                        className="glass rounded-xl p-4 cursor-pointer"
                        onClick={() => toggleWeek(week.week)}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="text-sm text-indigo-400">Week {week.week}</div>
                            <h4 className="font-semibold">{week.focus}</h4>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-muted-foreground">{week.hours}h</span>
                            {expandedWeeks.includes(week.week) ? (
                              <ChevronUp className="w-5 h-5" />
                            ) : (
                              <ChevronDown className="w-5 h-5" />
                            )}
                          </div>
                        </div>

                        {expandedWeeks.includes(week.week) && (
                          <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                            className="mt-4 pt-4 border-t border-white/10 space-y-4"
                          >
                            {week.courses?.length > 0 && (
                              <div>
                                <div className="text-sm text-muted-foreground mb-2">Courses</div>
                                <div className="flex flex-wrap gap-2">
                                  {week.courses.map((course, j) => (
                                    <span key={j} className="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-sm">
                                      {course}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}
                            {week.milestones?.length > 0 && (
                              <div>
                                <div className="text-sm text-muted-foreground mb-2">Milestones</div>
                                <ul className="space-y-1">
                                  {week.milestones.map((milestone, j) => (
                                    <li key={j} className="flex items-center gap-2 text-sm">
                                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                                      {milestone}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            {week.skills_developed?.length > 0 && (
                              <div>
                                <div className="text-sm text-muted-foreground mb-2">Skills Developed</div>
                                <div className="flex flex-wrap gap-2">
                                  {week.skills_developed.map((skill, j) => (
                                    <span key={j} className="px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs">
                                      {skill}
                                    </span>
                                  ))}
                                </div>
                              </div>
                            )}
                          </motion.div>
                        )}
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          </TabsContent>

          {/* CV Versions Tab */}
          <TabsContent value="cv" className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Natural Resume */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-2xl p-6"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Users className="w-5 h-5 text-blue-400" />
                    Natural Authentic
                  </h3>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => copyToClipboard(
                      `${result?.cv_natural?.summary}\n\n${result?.cv_natural?.experience_bullets?.join('\n')}\n\n${result?.cv_natural?.skills_section}`,
                      "Natural Resume"
                    )}
                    data-testid="copy-natural-cv-btn"
                  >
                    <Copy className="w-4 h-4" />
                  </Button>
                </div>
                <div className="space-y-4 text-sm">
                  <div>
                    <div className="text-muted-foreground mb-1">Summary</div>
                    <p className="bg-white/5 p-3 rounded-lg">{result?.cv_natural?.summary}</p>
                  </div>
                  <div>
                    <div className="text-muted-foreground mb-1">Experience Highlights</div>
                    <ul className="space-y-2 bg-white/5 p-3 rounded-lg">
                      {result?.cv_natural?.experience_bullets?.map((bullet, i) => (
                        <li key={i}>• {bullet}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <div className="text-muted-foreground mb-1">Skills</div>
                    <p className="bg-white/5 p-3 rounded-lg">{result?.cv_natural?.skills_section}</p>
                  </div>
                </div>
              </motion.div>

              {/* ATS Optimized Resume */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="glass rounded-2xl p-6 border-2 border-emerald-500/30"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-emerald-400" />
                    ATS Optimized 90+
                  </h3>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => copyToClipboard(
                      `${result?.cv_ats_optimized?.summary}\n\n${result?.cv_ats_optimized?.experience_bullets?.join('\n')}\n\n${result?.cv_ats_optimized?.skills_section}`,
                      "ATS Resume"
                    )}
                    data-testid="copy-ats-cv-btn"
                  >
                    <Copy className="w-4 h-4" />
                  </Button>
                </div>
                <div className="space-y-4 text-sm">
                  <div>
                    <div className="text-muted-foreground mb-1">Summary</div>
                    <p className="bg-white/5 p-3 rounded-lg">{result?.cv_ats_optimized?.summary}</p>
                  </div>
                  <div>
                    <div className="text-muted-foreground mb-1">Experience Highlights</div>
                    <ul className="space-y-2 bg-white/5 p-3 rounded-lg">
                      {result?.cv_ats_optimized?.experience_bullets?.map((bullet, i) => (
                        <li key={i}>• {bullet}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <div className="text-muted-foreground mb-1">Skills</div>
                    <p className="bg-white/5 p-3 rounded-lg">{result?.cv_ats_optimized?.skills_section}</p>
                  </div>
                </div>
              </motion.div>
            </div>
          </TabsContent>

          {/* Next Steps Tab */}
          <TabsContent value="next" className="space-y-6">
            <div className="grid md:grid-cols-3 gap-6">
              {/* This Week */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-2xl p-6"
              >
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <Zap className="w-5 h-5 text-amber-400" />
                  This Week
                </h3>
                <ul className="space-y-3">
                  {result?.next_steps?.this_week?.map((step, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <div className="w-6 h-6 rounded-full bg-amber-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs text-amber-400">{i + 1}</span>
                      </div>
                      <span className="text-sm">{step}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>

              {/* This Month */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="glass rounded-2xl p-6"
              >
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <Target className="w-5 h-5 text-indigo-400" />
                  This Month
                </h3>
                <ul className="space-y-3">
                  {result?.next_steps?.this_month?.map((step, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <div className="w-6 h-6 rounded-full bg-indigo-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs text-indigo-400">{i + 1}</span>
                      </div>
                      <span className="text-sm">{step}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>

              {/* Next 3 Months */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="glass rounded-2xl p-6"
              >
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-emerald-400" />
                  Next 3 Months
                </h3>
                <ul className="space-y-3">
                  {result?.next_steps?.next_3_months?.map((step, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <div className="w-6 h-6 rounded-full bg-emerald-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs text-emerald-400">{i + 1}</span>
                      </div>
                      <span className="text-sm">{step}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            </div>

            {/* Alternative Roles */}
            {result?.alternative_roles?.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="glass rounded-2xl p-6"
              >
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <Users className="w-5 h-5 text-purple-400" />
                  Alternative Roles to Consider
                </h3>
                <div className="grid md:grid-cols-3 gap-4">
                  {result?.alternative_roles?.map((role, i) => (
                    <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/10">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium">{role.role_name}</span>
                        <span className="text-sm text-emerald-400">{role.fit_score}% fit</span>
                      </div>
                      <p className="text-sm text-muted-foreground mb-2">{role.reason}</p>
                      <div className="text-xs text-amber-400">
                        <Clock className="w-3 h-3 inline mr-1" />
                        {role.timeline_weeks} weeks
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Warning Flags */}
            {result?.warning_flags?.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="glass rounded-2xl p-6 border border-amber-500/30"
              >
                <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-amber-400" />
                  Challenges & How to Overcome Them
                </h3>
                <div className="space-y-4">
                  {result?.warning_flags?.map((flag, i) => (
                    <div key={i} className="p-4 rounded-xl bg-amber-500/10">
                      <h4 className="font-medium mb-2">{flag.obstacle}</h4>
                      <p className="text-sm text-muted-foreground mb-2">{flag.how_to_overcome}</p>
                      {flag.resources?.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {flag.resources.map((resource, j) => (
                            <span key={j} className="text-xs px-2 py-1 rounded-full bg-white/10">
                              {resource}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </motion.div>
            )}
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
