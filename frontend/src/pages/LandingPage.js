import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Brain, Zap, Target, TrendingUp, FileText, Sparkles,
  CheckCircle2, ArrowRight, Star, Users, Award, Clock,
  BookOpen, Download, Globe, Briefcase, GraduationCap,
  ChevronRight, Play, Shield, BarChart3, FileEdit, Send,
  Building2, Search, Calendar, Mail
} from "lucide-react";
import { Button } from "../components/ui/button";
import { useAuth } from "../context/AuthContext";

const aiRoles = [
  "AI/ML Engineer", "Prompt Engineer", "AI Product Manager", "Data Scientist",
  "MLOps Engineer", "Generative AI Developer", "AI Solutions Architect",
  "NLP Engineer", "Computer Vision Engineer", "Autonomous Agent Developer"
];

const testimonials = [
  {
    name: "Sarah Chen",
    role: "Backend Dev → ML Engineer",
    quote: "Used all 5 features - Career Analysis showed my 92% match, Learning Path got me ready, Resume + Cover Letter got me interviews, and Auto-Apply landed me 3 offers!",
    rating: 5,
    company: "Google",
    feature: "Complete Platform"
  },
  {
    name: "Marcus Johnson",
    role: "Product Manager → AI PM",
    quote: "The Auto-Apply feature changed everything. I got 67 applications sent while I focused on learning. 5 interviews in 2 weeks!",
    rating: 5,
    company: "OpenAI",
    feature: "Auto-Apply"
  },
  {
    name: "Priya Sharma",
    role: "Data Analyst → Data Scientist",
    quote: "The personalized cover letters were incredible. Each one was tailored to the job description. Hiring managers noticed!",
    rating: 5,
    company: "Meta",
    feature: "Cover Letter"
  }
];

export default function LandingPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [showAuth, setShowAuth] = useState(false);

  const handleGetStarted = (path = "/analyze") => {
    if (isAuthenticated) {
      navigate(path);
    } else {
      setShowAuth(true);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Brain className="w-8 h-8 text-indigo-400" />
              <span className="text-xl font-bold">TechShift AI</span>
            </div>

            {/* Feature Navigation - All 5 Features */}
            <div className="hidden lg:flex items-center gap-4">
              <a href="#analysis" className="text-sm text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1">
                <Target className="w-4 h-4" /> Analysis
              </a>
              <a href="#learning" className="text-sm text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1">
                <BookOpen className="w-4 h-4" /> Learning
              </a>
              <a href="#resume" className="text-sm text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1">
                <FileText className="w-4 h-4" /> Resume
              </a>
              <a href="#cover-letter" className="text-sm text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1">
                <FileEdit className="w-4 h-4" /> Cover Letter
              </a>
              <a href="#auto-apply" className="text-sm text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1">
                <Zap className="w-4 h-4" /> Auto-Apply
              </a>
              <a href="#pricing" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
                Pricing
              </a>
            </div>

            <div className="flex items-center gap-3">
              {isAuthenticated ? (
                <Button onClick={() => navigate("/dashboard")} className="btn-primary" data-testid="dashboard-btn">
                  Dashboard
                </Button>
              ) : (
                <>
                  <Button variant="ghost" onClick={() => setShowAuth(true)} data-testid="signin-btn">
                    Sign In
                  </Button>
                  <Button onClick={() => setShowAuth(true)} className="btn-primary" data-testid="get-started-btn">
                    Get Started Free
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-16 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/30 mb-6">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span className="text-sm text-indigo-300">Complete AI Career Platform - 5 Powerful Features</span>
            </div>

            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Land Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">AI Job</span> in 90 Days
            </h1>

            <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
              From skill gap analysis to job offers. Complete AI career platform with automated job applications.
            </p>

            {/* Stats Banner */}
            <div className="flex flex-wrap justify-center gap-8 mb-12">
              <div className="text-center">
                <div className="text-2xl font-bold text-indigo-400">10,000+</div>
                <div className="text-sm text-muted-foreground">AI Job Seekers</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-emerald-400">87%</div>
                <div className="text-sm text-muted-foreground">Get Interviews</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-400">78%</div>
                <div className="text-sm text-muted-foreground">Get Offers</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-amber-400">$200K+</div>
                <div className="text-sm text-muted-foreground">Avg. AI Salary</div>
              </div>
            </div>
          </motion.div>

          {/* 5-Step Journey Visual */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass rounded-2xl p-8 mb-12"
          >
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold mb-2">Your Complete AI Job Landing Journey</h2>
              <p className="text-muted-foreground">5 steps from confusion to offers</p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              {[
                { icon: Target, label: "ANALYZE", time: "5 min", color: "indigo", desc: "Find your AI role fit" },
                { icon: BookOpen, label: "LEARN", time: "16 weeks", color: "purple", desc: "Follow guided path" },
                { icon: FileText, label: "RESUME", time: "30 sec", color: "emerald", desc: "Get 2 versions" },
                { icon: FileEdit, label: "COVER LETTER", time: "2 min", color: "amber", desc: "3 variations" },
                { icon: Zap, label: "AUTO-APPLY", time: "Passive", color: "rose", desc: "Apply 24/7" }
              ].map((step, i) => (
                <div key={i} className="text-center relative">
                  <div className={`w-16 h-16 mx-auto rounded-2xl bg-${step.color}-500/20 flex items-center justify-center mb-3`}>
                    <step.icon className={`w-8 h-8 text-${step.color}-400`} />
                  </div>
                  <div className="font-bold text-sm mb-1">{step.label}</div>
                  <div className="text-xs text-muted-foreground">{step.time}</div>
                  <div className="text-xs text-muted-foreground mt-1">{step.desc}</div>
                  {i < 4 && (
                    <ChevronRight className="hidden md:block absolute top-8 -right-2 w-4 h-4 text-muted-foreground" />
                  )}
                </div>
              ))}
            </div>

            <div className="text-center mt-8">
              <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-gradient-to-r from-indigo-500/20 to-rose-500/20 border border-indigo-500/30">
                <span className="text-lg">🎯</span>
                <span className="font-semibold">Result: Get Hired While You Sleep</span>
              </div>
            </div>
          </motion.div>

          {/* 5 Feature Cards */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="grid md:grid-cols-5 gap-4 max-w-6xl mx-auto"
          >
            {/* Analysis Card */}
            <div
              className="glass rounded-xl p-5 border border-indigo-500/30 hover:border-indigo-500/60 transition-all cursor-pointer group"
              onClick={() => handleGetStarted("/analyze")}
              data-testid="feature-analysis"
            >
              <div className="w-12 h-12 rounded-xl bg-indigo-500/20 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <Target className="w-6 h-6 text-indigo-400" />
              </div>
              <h3 className="font-bold mb-1">🔍 Analysis</h3>
              <p className="text-xs text-muted-foreground mb-3">Which AI role fits me?</p>
              <ul className="space-y-1 text-xs text-muted-foreground">
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-indigo-400" /> 20+ AI roles</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-indigo-400" /> Skill gaps</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-indigo-400" /> 90-day roadmap</li>
              </ul>
            </div>

            {/* Learning Card */}
            <div
              className="glass rounded-xl p-5 border border-purple-500/30 hover:border-purple-500/60 transition-all cursor-pointer group"
              onClick={() => handleGetStarted("/learning-path")}
              data-testid="feature-learning"
            >
              <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <BookOpen className="w-6 h-6 text-purple-400" />
              </div>
              <h3 className="font-bold mb-1">📚 Learning</h3>
              <p className="text-xs text-muted-foreground mb-3">How do I get there?</p>
              <ul className="space-y-1 text-xs text-muted-foreground">
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-purple-400" /> 16-week path</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-purple-400" /> Real courses</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-purple-400" /> Interview prep</li>
              </ul>
            </div>

            {/* Resume Card */}
            <div
              className="glass rounded-xl p-5 border border-emerald-500/30 hover:border-emerald-500/60 transition-all cursor-pointer group"
              onClick={() => handleGetStarted("/cv-generator")}
              data-testid="feature-resume"
            >
              <div className="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <FileText className="w-6 h-6 text-emerald-400" />
              </div>
              <h3 className="font-bold mb-1">📄 Resume</h3>
              <p className="text-xs text-muted-foreground mb-3">How do I apply?</p>
              <ul className="space-y-1 text-xs text-muted-foreground">
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-emerald-400" /> 2 versions</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-emerald-400" /> 90+ ATS score</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-emerald-400" /> 60+ countries</li>
              </ul>
            </div>

            {/* Cover Letter Card */}
            <div
              className="glass rounded-xl p-5 border border-amber-500/30 hover:border-amber-500/60 transition-all cursor-pointer group"
              onClick={() => handleGetStarted("/cover-letter")}
              data-testid="feature-cover-letter"
            >
              <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <FileEdit className="w-6 h-6 text-amber-400" />
              </div>
              <h3 className="font-bold mb-1">📝 Cover Letter</h3>
              <p className="text-xs text-muted-foreground mb-3">How do I stand out?</p>
              <ul className="space-y-1 text-xs text-muted-foreground">
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-amber-400" /> Job-matched</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-amber-400" /> 3 versions</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-amber-400" /> ATS keywords</li>
              </ul>
            </div>

            {/* Auto-Apply Card - Highlighted */}
            <div
              className="glass rounded-xl p-5 border-2 border-rose-500/50 hover:border-rose-500 transition-all cursor-pointer group relative"
              onClick={() => handleGetStarted("/auto-apply")}
              data-testid="feature-auto-apply"
            >
              <div className="absolute -top-2 right-2 px-2 py-0.5 bg-rose-500 rounded-full text-xs font-medium">
                NEW
              </div>
              <div className="w-12 h-12 rounded-xl bg-rose-500/20 flex items-center justify-center mb-3 group-hover:scale-110 transition-transform">
                <Zap className="w-6 h-6 text-rose-400" />
              </div>
              <h3 className="font-bold mb-1">⚡ Auto-Apply</h3>
              <p className="text-xs text-muted-foreground mb-3">Get me the jobs!</p>
              <ul className="space-y-1 text-xs text-muted-foreground">
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-rose-400" /> 24/7 scanning</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-rose-400" /> Auto-submit</li>
                <li className="flex items-center gap-1"><CheckCircle2 className="w-3 h-3 text-rose-400" /> Track offers</li>
              </ul>
            </div>
          </motion.div>
        </div>
      </section>

      {/* AI Roles Marquee */}
      <section className="py-8 border-y border-white/10 overflow-hidden">
        <div className="flex animate-marquee whitespace-nowrap">
          {[...aiRoles, ...aiRoles].map((role, index) => (
            <span key={index} className="mx-8 text-lg text-muted-foreground">
              {role} <span className="text-indigo-400">•</span>
            </span>
          ))}
        </div>
      </section>

      {/* Feature 1: Career Analysis */}
      <section id="analysis" className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="grid md:grid-cols-2 gap-8 items-center"
          >
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 mb-4">
                <Target className="w-4 h-4 text-indigo-400" />
                <span className="text-sm text-indigo-300">Step 1: Analyze</span>
              </div>
              <h2 className="text-3xl font-bold mb-4">🔍 Career Gap Analysis</h2>
              <p className="text-muted-foreground mb-6">
                Upload your resume and discover which AI roles are the best fit. See your skill gaps,
                transferable skills, and get a 90-day roadmap.
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-400" /> Match to 20+ AI roles</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-400" /> Identify skill gaps</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-400" /> Get personalized roadmap</li>
              </ul>
              <Button onClick={() => handleGetStarted("/analyze")} className="btn-primary">
                Analyze My Career <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </div>
            <div className="glass rounded-2xl p-6">
              <div className="text-sm text-muted-foreground mb-3">Sample Output:</div>
              <div className="space-y-3">
                <div className="bg-black/20 rounded-lg p-3">
                  <div className="text-indigo-400 font-semibold mb-1">Your Best Matches</div>
                  <div className="text-sm text-muted-foreground">
                    🥇 MLOps Engineer (92%)<br />
                    🥈 AI/ML Engineer (88%)<br />
                    🥉 Prompt Engineer (85%)
                  </div>
                </div>
                <div className="bg-black/20 rounded-lg p-3">
                  <div className="text-amber-400 font-semibold mb-1">Skills to Learn</div>
                  <div className="text-sm text-muted-foreground">Model Deployment, ML Monitoring, Kubernetes</div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Feature 2: Learning Path */}
      <section id="learning" className="py-16 px-4 bg-purple-500/5">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="grid md:grid-cols-2 gap-8 items-center"
          >
            <div className="order-2 md:order-1 glass rounded-2xl p-6">
              <div className="text-sm text-muted-foreground mb-3">16-Week Structure:</div>
              <div className="space-y-2">
                {[
                  { week: "1-4", name: "Foundations", color: "emerald" },
                  { week: "5-8", name: "Intermediate ML", color: "indigo" },
                  { week: "9-12", name: "Advanced + LLMs", color: "purple" },
                  { week: "13-16", name: "Interview Prep", color: "amber" }
                ].map((phase, i) => (
                  <div key={i} className={`bg-${phase.color}-500/10 rounded-lg p-3 flex items-center justify-between`}>
                    <span className="text-sm font-medium">Week {phase.week}</span>
                    <span className={`text-sm text-${phase.color}-400`}>{phase.name}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="order-1 md:order-2">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/30 mb-4">
                <BookOpen className="w-4 h-4 text-purple-400" />
                <span className="text-sm text-purple-300">Step 2: Learn</span>
              </div>
              <h2 className="text-3xl font-bold mb-4">📚 16-Week AI Learning Path</h2>
              <p className="text-muted-foreground mb-6">
                Stop taking random courses. Get a personalized curriculum with real courses
                from Fast.ai, DeepLearning.AI, Coursera, and more.
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-purple-400" /> Clickable course links</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-purple-400" /> Weekly projects</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-purple-400" /> Interview prep included</li>
              </ul>
              <Button onClick={() => handleGetStarted("/learning-path")} className="btn-primary">
                View Learning Path <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Feature 3: Resume Generator */}
      <section id="resume" className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="grid md:grid-cols-2 gap-8 items-center"
          >
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 mb-4">
                <FileText className="w-4 h-4 text-emerald-400" />
                <span className="text-sm text-emerald-300">Step 3: Resume</span>
              </div>
              <h2 className="text-3xl font-bold mb-4">📄 AI Resume That Gets Interviews</h2>
              <p className="text-muted-foreground mb-6">
                Upload your resume and get 2 professionally formatted versions - Natural Voice
                and ATS Optimized - tailored to 60+ countries.
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-emerald-400" /> 90+ ATS score guaranteed</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-emerald-400" /> Region-specific formatting</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-emerald-400" /> PDF + DOCX download</li>
              </ul>
              <Button onClick={() => handleGetStarted("/cv-generator")} className="btn-primary">
                Generate 2 Resumes <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </div>
            <div className="glass rounded-2xl p-6">
              <div className="flex gap-4">
                <div className="flex-1 bg-black/20 rounded-lg p-4 text-center">
                  <div className="text-2xl mb-2">✍️</div>
                  <div className="font-semibold text-sm">Natural</div>
                  <div className="text-xs text-muted-foreground">Human, story-driven</div>
                </div>
                <div className="flex-1 bg-black/20 rounded-lg p-4 text-center">
                  <div className="text-2xl mb-2">🎯</div>
                  <div className="font-semibold text-sm">ATS Optimized</div>
                  <div className="text-xs text-muted-foreground">90+ score</div>
                </div>
              </div>
              <div className="mt-4 text-center">
                <div className="text-5xl font-bold text-emerald-400">90+</div>
                <div className="text-sm text-muted-foreground">ATS Score</div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Feature 4: Cover Letter - NEW */}
      <section id="cover-letter" className="py-16 px-4 bg-amber-500/5">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="grid md:grid-cols-2 gap-8 items-center"
          >
            <div className="order-2 md:order-1 glass rounded-2xl p-6">
              <div className="text-sm text-muted-foreground mb-3">3 Variations:</div>
              <div className="space-y-3">
                <div className="bg-black/20 rounded-lg p-3">
                  <div className="font-semibold text-sm text-amber-400">V1: Technical Focus</div>
                  <div className="text-xs text-muted-foreground">Emphasizes technical skills</div>
                </div>
                <div className="bg-black/20 rounded-lg p-3">
                  <div className="font-semibold text-sm text-indigo-400">V2: Problem-Solving</div>
                  <div className="text-xs text-muted-foreground">Emphasizes impact & results</div>
                </div>
                <div className="bg-black/20 rounded-lg p-3">
                  <div className="font-semibold text-sm text-purple-400">V3: Culture Fit</div>
                  <div className="text-xs text-muted-foreground">Emphasizes values & growth</div>
                </div>
              </div>
            </div>
            <div className="order-1 md:order-2">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 mb-4">
                <FileEdit className="w-4 h-4 text-amber-400" />
                <span className="text-sm text-amber-300">Step 4: Cover Letter</span>
                <span className="text-xs bg-amber-500 text-black px-2 py-0.5 rounded-full ml-2">NEW</span>
              </div>
              <h2 className="text-3xl font-bold mb-4">📝 AI Cover Letter That Stands Out</h2>
              <p className="text-muted-foreground mb-6">
                Paste a job description and get 3 unique variations of your cover letter. Each version
                highlights different aspects - technical skills, problem-solving, or culture fit.
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-amber-400" /> Job-matched content</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-amber-400" /> 3 tone options</li>
                <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-amber-400" /> ATS-optimized keywords</li>
              </ul>
              <Button onClick={() => handleGetStarted("/cover-letter")} className="btn-primary">
                Generate Cover Letter <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Feature 5: Auto-Apply - NEW & HIGHLIGHTED */}
      <section id="auto-apply" className="py-16 px-4 bg-gradient-to-b from-rose-500/10 to-transparent">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-rose-500/10 border border-rose-500/30 mb-4">
              <Zap className="w-4 h-4 text-rose-400" />
              <span className="text-sm text-rose-300">Step 5: Auto-Apply</span>
              <span className="text-xs bg-rose-500 text-white px-2 py-0.5 rounded-full ml-2">GAME CHANGER</span>
            </div>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              ⚡ AI Auto-Apply - Apply to Jobs While You Sleep
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Set your preferences once. We scan job boards 24/7, match jobs to your profile,
              and auto-submit your resume + cover letter.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="glass rounded-xl p-6">
              <Search className="w-10 h-10 text-rose-400 mb-4" />
              <h3 className="font-semibold mb-2">Real-Time Scanning</h3>
              <p className="text-sm text-muted-foreground">
                We monitor 100+ job boards 24/7. New matching jobs → auto-apply within 1 hour.
              </p>
            </div>
            <div className="glass rounded-xl p-6">
              <Send className="w-10 h-10 text-rose-400 mb-4" />
              <h3 className="font-semibold mb-2">Smart Applications</h3>
              <p className="text-sm text-muted-foreground">
                Each application is customized. Resume version selected based on job. Cover letter auto-generated.
              </p>
            </div>
            <div className="glass rounded-xl p-6">
              <Calendar className="w-10 h-10 text-rose-400 mb-4" />
              <h3 className="font-semibold mb-2">Interview Alerts</h3>
              <p className="text-sm text-muted-foreground">
                Get instant alerts when companies show interest. Prep materials provided automatically.
              </p>
            </div>
          </div>

          {/* Mock Dashboard Preview */}
          <div className="glass rounded-2xl p-6">
            <div className="text-sm text-muted-foreground mb-4">Sample Dashboard:</div>
            <div className="grid md:grid-cols-4 gap-4 mb-6">
              <div className="bg-black/20 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-rose-400">67</div>
                <div className="text-xs text-muted-foreground">Applications</div>
              </div>
              <div className="bg-black/20 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-amber-400">9</div>
                <div className="text-xs text-muted-foreground">Interviews</div>
              </div>
              <div className="bg-black/20 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-emerald-400">2</div>
                <div className="text-xs text-muted-foreground">Offers</div>
              </div>
              <div className="bg-black/20 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-indigo-400">13%</div>
                <div className="text-xs text-muted-foreground">Callback Rate</div>
              </div>
            </div>
            <div className="text-center">
              <Button onClick={() => handleGetStarted("/auto-apply")} size="lg" className="btn-primary">
                Activate Auto-Apply <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold mb-4">Success Stories</h2>
            <p className="text-muted-foreground">Real people. Real transitions. Real offers.</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="glass rounded-2xl p-6"
              >
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 text-amber-400 fill-amber-400" />
                  ))}
                </div>
                <p className="text-muted-foreground mb-4 text-sm">&ldquo;{testimonial.quote}&rdquo;</p>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold">{testimonial.name}</div>
                    <div className="text-xs text-muted-foreground">{testimonial.role}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-indigo-400 font-medium">{testimonial.company}</div>
                    <div className="text-xs text-muted-foreground">{testimonial.feature}</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-16 px-4 bg-indigo-500/5">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold mb-4">One Price. Unlimited Possibilities.</h2>
            <p className="text-muted-foreground">Try all 5 features free. No credit card required.</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {/* Free Tier */}
            <div className="glass rounded-2xl p-6 border border-white/10">
              <h3 className="text-xl font-bold mb-2">Free</h3>
              <div className="text-3xl font-bold mb-4">$0<span className="text-lg text-muted-foreground">/month</span></div>
              <ul className="space-y-3 mb-6 text-sm">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> 1 Career Analysis/month</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> 1 Learning Path/month</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> 2 Resumes/month</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> 1 Cover Letter/month</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Auto-Apply: 5 jobs/week</li>
              </ul>
              <Button onClick={() => handleGetStarted()} className="w-full btn-secondary" data-testid="pricing-free">
                Start Free
              </Button>
            </div>

            {/* Pro Tier */}
            <div className="glass rounded-2xl p-6 border-2 border-indigo-500/50 relative">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-indigo-500 rounded-full text-xs font-medium">
                BEST VALUE
              </div>
              <h3 className="text-xl font-bold mb-2">Pro</h3>
              <div className="text-3xl font-bold mb-4">$9.99<span className="text-lg text-muted-foreground">/month</span></div>
              <ul className="space-y-3 mb-6 text-sm">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-indigo-400" /> Unlimited Analyses</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-indigo-400" /> Unlimited Learning Paths</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-indigo-400" /> Unlimited Resumes</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-indigo-400" /> Unlimited Cover Letters</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-indigo-400" /> Unlimited Auto-Apply</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-indigo-400" /> Priority support</li>
              </ul>
              <Button onClick={() => handleGetStarted()} className="w-full btn-primary" data-testid="pricing-pro">
                Start Pro Trial
              </Button>
            </div>

            {/* Enterprise */}
            <div className="glass rounded-2xl p-6 border border-white/10">
              <h3 className="text-xl font-bold mb-2">Enterprise</h3>
              <div className="text-3xl font-bold mb-4">$49<span className="text-lg text-muted-foreground">/month</span></div>
              <ul className="space-y-3 mb-6 text-sm">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> Everything in Pro</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> Recruiter outreach</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> Salary negotiation</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> 1-on-1 coaching</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-amber-400" /> Company research</li>
              </ul>
              <Button onClick={() => handleGetStarted()} className="w-full btn-secondary" data-testid="pricing-enterprise">
                Contact Sales
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Land Your AI Job in 90 Days?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Get analyzed. Get trained. Get hired. Free to start. No credit card required.
            </p>

            <div className="flex flex-wrap justify-center gap-3">
              <Button onClick={() => handleGetStarted("/analyze")} size="lg" className="btn-primary" data-testid="cta-analyze">
                <Target className="w-5 h-5 mr-2" /> Analyze
              </Button>
              <Button onClick={() => handleGetStarted("/learning-path")} size="lg" variant="outline">
                <BookOpen className="w-5 h-5 mr-2" /> Learn
              </Button>
              <Button onClick={() => handleGetStarted("/cv-generator")} size="lg" variant="outline">
                <FileText className="w-5 h-5 mr-2" /> Resume
              </Button>
              <Button onClick={() => handleGetStarted("/cover-letter")} size="lg" variant="outline">
                <FileEdit className="w-5 h-5 mr-2" /> Cover Letter
              </Button>
              <Button onClick={() => handleGetStarted("/auto-apply")} size="lg" variant="outline">
                <Zap className="w-5 h-5 mr-2" /> Auto-Apply
              </Button>
            </div>

            <p className="text-sm text-muted-foreground mt-8">
              Join 10,000+ AI job seekers. Getting trained. Getting interviewed. Getting hired.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-white/10">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Brain className="w-6 h-6 text-indigo-400" />
            <span className="font-semibold">TechShift AI</span>
          </div>
          <div className="text-sm text-muted-foreground">
            © 2025 TechShift AI. Complete AI career platform.
          </div>
        </div>
      </footer>

      {/* Auth Modal */}
      {showAuth && (
        <AuthModal onClose={() => setShowAuth(false)} />
      )}

      {/* Marquee Animation Style */}
      <style>{`
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-marquee {
          animation: marquee 30s linear infinite;
        }
      `}</style>
    </div>
  );
}

// Auth Modal Component
function AuthModal({ onClose }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(email, password, name);
      }
      onClose();
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70" onClick={onClose}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass rounded-2xl p-8 w-full max-w-md"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-2xl font-bold mb-6 text-center">
          {isLogin ? "Welcome Back" : "Create Account"}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <div>
              <label className="block text-sm mb-2">Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full h-12 px-4 rounded-lg bg-black/20 border border-white/10 focus:border-indigo-500 outline-none"
                placeholder="Your name"
                required={!isLogin}
                data-testid="auth-name-input"
              />
            </div>
          )}

          <div>
            <label className="block text-sm mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full h-12 px-4 rounded-lg bg-black/20 border border-white/10 focus:border-indigo-500 outline-none"
              placeholder="you@example.com"
              required
              data-testid="auth-email-input"
            />
          </div>

          <div>
            <label className="block text-sm mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full h-12 px-4 rounded-lg bg-black/20 border border-white/10 focus:border-indigo-500 outline-none"
              placeholder="••••••••"
              required
              data-testid="auth-password-input"
            />
          </div>

          {error && (
            <div className="text-red-400 text-sm text-center">{error}</div>
          )}

          <Button type="submit" disabled={loading} className="w-full btn-primary h-12" data-testid="auth-submit-btn">
            {loading ? "Loading..." : isLogin ? "Sign In" : "Create Account"}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm">
          {isLogin ? (
            <span>
              Don&apos;t have an account?{" "}
              <button onClick={() => setIsLogin(false)} className="text-indigo-400 hover:underline">
                Sign up
              </button>
            </span>
          ) : (
            <span>
              Already have an account?{" "}
              <button onClick={() => setIsLogin(true)} className="text-indigo-400 hover:underline">
                Sign in
              </button>
            </span>
          )}
        </div>
      </motion.div>
    </div>
  );
}
