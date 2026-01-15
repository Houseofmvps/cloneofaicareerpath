import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
import { 
  Brain, FileText, Target, Clock, ChevronRight, Zap, BarChart3, BookOpen,
  Briefcase, TrendingUp, CheckCircle2, Circle, ArrowRight, Sparkles,
  DollarSign, Calendar, ExternalLink, Send, GraduationCap, FileCheck,
  Users, Award, Rocket, AlertCircle, Play
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Progress } from "../components/ui/progress";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import AppNavigation from "../components/AppNavigation";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

// Stage indicator component
const StageIndicator = ({ stage, isActive, isCompleted }) => {
  return (
    <div className="flex flex-col items-center">
      <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
        isCompleted ? "bg-emerald-500 text-white" :
        isActive ? "bg-indigo-500 text-white animate-pulse" :
        "bg-white/10 text-muted-foreground"
      }`}>
        {isCompleted ? <CheckCircle2 className="w-5 h-5" /> : <Circle className="w-5 h-5" />}
      </div>
      <span className={`text-xs mt-1 ${isCompleted ? "text-emerald-400" : isActive ? "text-indigo-400" : "text-muted-foreground"}`}>
        {stage.label}
      </span>
    </div>
  );
};

// Metric Card component
const MetricCard = ({ icon: Icon, title, value, subtitle, color, link, linkText }) => {
  const navigate = useNavigate();
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-xl p-5 hover:bg-white/5 transition-all cursor-pointer"
      onClick={() => link && navigate(link)}
    >
      <div className="flex items-start justify-between">
        <div className={`w-12 h-12 rounded-xl ${color} flex items-center justify-center`}>
          <Icon className="w-6 h-6" />
        </div>
        {link && (
          <ChevronRight className="w-5 h-5 text-muted-foreground" />
        )}
      </div>
      <div className="mt-4">
        <div className="text-2xl font-bold">{value}</div>
        <div className="text-sm font-medium text-foreground/80">{title}</div>
        <div className="text-xs text-muted-foreground mt-1">{subtitle}</div>
      </div>
      {linkText && (
        <div className="mt-3 text-xs text-indigo-400 flex items-center gap-1">
          {linkText} <ArrowRight className="w-3 h-3" />
        </div>
      )}
    </motion.div>
  );
};

// Action Card component
const ActionCard = ({ action, index }) => {
  const navigate = useNavigate();
  const icons = {
    analysis: Brain,
    learning: GraduationCap,
    resume: FileText,
    apply: Send,
    interview: Users
  };
  const Icon = icons[action.type] || Zap;
  
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      className="flex items-start gap-4 p-4 glass rounded-xl hover:bg-white/5 transition-all cursor-pointer"
      onClick={() => navigate(action.link)}
    >
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
        action.priority === 1 ? "bg-indigo-500/20 text-indigo-400" : "bg-white/10 text-muted-foreground"
      }`}>
        <Icon className="w-5 h-5" />
      </div>
      <div className="flex-1">
        <div className="font-medium flex items-center gap-2">
          {action.title}
          {action.priority === 1 && (
            <span className="text-xs bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full">
              Priority
            </span>
          )}
        </div>
        <div className="text-sm text-muted-foreground mt-0.5">{action.description}</div>
      </div>
      <ArrowRight className="w-5 h-5 text-muted-foreground" />
    </motion.div>
  );
};

// Hot Job Card component
const HotJobCard = ({ job }) => {
  const handleApply = () => {
    window.open(job.job_url, "_blank");
  };
  
  return (
    <div className="p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-all">
      <div className="flex items-start justify-between">
        <div>
          <div className="font-medium text-sm line-clamp-1">{job.title}</div>
          <div className="text-xs text-muted-foreground">{job.company}</div>
        </div>
        <div className="text-right">
          <div className="text-sm font-bold text-indigo-400">{job.match_score}%</div>
          <div className="text-xs text-muted-foreground">match</div>
        </div>
      </div>
      <div className="flex items-center justify-between mt-3">
        <span className="text-xs text-emerald-400">{job.salary_range}</span>
        <Button size="sm" variant="ghost" className="h-7 text-xs" onClick={handleApply}>
          Apply <ExternalLink className="w-3 h-3 ml-1" />
        </Button>
      </div>
    </div>
  );
};

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await axios.get(`${API}/dashboard/career-progress`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      setDashboard(response.data);
    } catch (error) {
      console.error("Failed to fetch dashboard:", error);
      toast.error("Failed to load dashboard");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="mt-4 text-muted-foreground">Loading your mission control...</p>
        </div>
      </div>
    );
  }

  const { progress, career_fit, learning, applications, market_value, daily_actions, hot_jobs } = dashboard || {};

  return (
    <div className="min-h-screen bg-background">
      <AppNavigation />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <Rocket className="w-8 h-8 text-indigo-400" />
            AI Career Mission Control
          </h1>
          <p className="text-muted-foreground mt-1">
            Welcome back, {dashboard?.user?.name || "User"}! Here's your career transition progress.
          </p>
        </motion.div>

        {/* 90-Day Progress Hero */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-2xl p-6 mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold">90-Day AI Career Transition</h2>
              <p className="text-sm text-muted-foreground">
                Day {progress?.day_of_90 || 1} of 90 • {progress?.overall_percentage || 0}% Complete
              </p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-indigo-400">{progress?.overall_percentage || 0}%</div>
              <div className="text-xs text-muted-foreground">overall progress</div>
            </div>
          </div>
          
          <Progress value={progress?.overall_percentage || 0} className="h-4 mb-6" />
          
          {/* Stage Indicators */}
          <div className="flex justify-between items-center relative">
            {/* Connecting line */}
            <div className="absolute top-5 left-0 right-0 h-0.5 bg-white/10" />
            
            {progress?.stages && Object.entries(progress.stages).map(([key, stage], index) => {
              const allStages = Object.values(progress.stages);
              const currentStageIndex = allStages.findIndex(s => !s.done);
              const isActive = index === currentStageIndex;
              
              return (
                <StageIndicator
                  key={key}
                  stage={stage}
                  isCompleted={stage.done}
                  isActive={isActive}
                />
              );
            })}
          </div>
        </motion.div>

        {/* Three Key Metrics */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <MetricCard
            icon={Target}
            title="Career Fit"
            value={career_fit?.best_role ? `${career_fit.best_role.fit_score}%` : "Not analyzed"}
            subtitle={career_fit?.best_role?.name || "Complete analysis to find your match"}
            color="bg-indigo-500/20 text-indigo-400"
            link="/analyze"
            linkText="View Analysis"
          />
          
          <MetricCard
            icon={BookOpen}
            title="Learning Progress"
            value={`Week ${learning?.current_week || 0}`}
            subtitle={`${learning?.percentage || 0}% complete • ${learning?.courses_completed || 0} courses done`}
            color="bg-purple-500/20 text-purple-400"
            link="/learning-path"
            linkText="Continue Learning"
          />
          
          <MetricCard
            icon={Briefcase}
            title="Applications"
            value={applications?.total_applied || 0}
            subtitle={`${applications?.response_rate || 0}% response rate (avg: ${applications?.industry_avg_rate || 8}%)`}
            color="bg-emerald-500/20 text-emerald-400"
            link="/auto-apply"
            linkText="Apply to Jobs"
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Actions & Funnel */}
          <div className="lg:col-span-2 space-y-8">
            {/* Today's AI-Recommended Actions */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="glass rounded-2xl p-6"
            >
              <h3 className="text-lg font-bold flex items-center gap-2 mb-4">
                <Sparkles className="w-5 h-5 text-amber-400" />
                Today's AI-Recommended Actions
              </h3>
              
              <div className="space-y-3">
                {daily_actions?.length > 0 ? (
                  daily_actions.map((action, index) => (
                    <ActionCard key={index} action={action} index={index} />
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <CheckCircle2 className="w-12 h-12 mx-auto mb-2 text-emerald-400" />
                    <p>All caught up! Keep applying to jobs.</p>
                  </div>
                )}
              </div>
            </motion.div>

            {/* Application Funnel */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="glass rounded-2xl p-6"
            >
              <h3 className="text-lg font-bold flex items-center gap-2 mb-4">
                <BarChart3 className="w-5 h-5 text-indigo-400" />
                Application Funnel
              </h3>
              
              <div className="flex items-end justify-between gap-4 h-32 mb-4">
                {[
                  { label: "Applied", value: applications?.funnel?.applied || 0, color: "bg-blue-500" },
                  { label: "Viewed", value: applications?.funnel?.viewed || 0, color: "bg-amber-500" },
                  { label: "Interviews", value: applications?.funnel?.interviews || 0, color: "bg-emerald-500" },
                  { label: "Offers", value: applications?.funnel?.offers || 0, color: "bg-green-500" }
                ].map((stage, index) => {
                  const maxVal = Math.max(applications?.funnel?.applied || 1, 1);
                  const height = Math.max((stage.value / maxVal) * 100, 5);
                  
                  return (
                    <div key={stage.label} className="flex-1 flex flex-col items-center">
                      <div className="w-full flex flex-col items-center justify-end h-24">
                        <span className="text-lg font-bold mb-1">{stage.value}</span>
                        <motion.div
                          initial={{ height: 0 }}
                          animate={{ height: `${height}%` }}
                          transition={{ delay: 0.5 + index * 0.1 }}
                          className={`w-full ${stage.color} rounded-t-lg min-h-[8px]`}
                        />
                      </div>
                      <span className="text-xs text-muted-foreground mt-2">{stage.label}</span>
                    </div>
                  );
                })}
              </div>
              
              {applications?.total_applied > 0 && (
                <div className="p-3 bg-indigo-500/10 border border-indigo-500/30 rounded-lg text-sm">
                  <span className="text-indigo-300">
                    {applications.response_rate > applications.industry_avg_rate ? (
                      <>🎉 Your response rate is <strong>{applications.response_rate}%</strong> - above industry average!</>
                    ) : (
                      <>📊 Apply to more jobs to improve your {applications.response_rate}% response rate</>
                    )}
                  </span>
                </div>
              )}
            </motion.div>

            {/* Skills Gap */}
            {career_fit?.skills_to_learn?.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="glass rounded-2xl p-6"
              >
                <h3 className="text-lg font-bold flex items-center gap-2 mb-4">
                  <GraduationCap className="w-5 h-5 text-purple-400" />
                  Priority Skills to Learn
                </h3>
                
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {career_fit.skills_to_learn.map((skill, index) => (
                    <div
                      key={index}
                      className="p-3 bg-white/5 rounded-lg text-center"
                    >
                      <span className="text-sm">{skill}</span>
                    </div>
                  ))}
                </div>
                
                <Button
                  className="w-full mt-4"
                  variant="outline"
                  onClick={() => navigate("/learning-path")}
                >
                  Start Learning Path <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </motion.div>
            )}
          </div>

          {/* Right Column - Market Value & Hot Jobs */}
          <div className="space-y-8">
            {/* Market Value */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="glass rounded-2xl p-6"
            >
              <h3 className="text-lg font-bold flex items-center gap-2 mb-4">
                <TrendingUp className="w-5 h-5 text-emerald-400" />
                Your Market Value
              </h3>
              
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Current (estimated)</span>
                  <span className="font-bold">${(market_value?.current_estimate || 0).toLocaleString()}</span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Target (AI role)</span>
                  <span className="font-bold text-emerald-400">${(market_value?.target_salary || 0).toLocaleString()}</span>
                </div>
                
                <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl text-center">
                  <div className="text-2xl font-bold text-emerald-400">
                    +{market_value?.increase_percentage || 0}%
                  </div>
                  <div className="text-sm text-muted-foreground">
                    potential salary increase
                  </div>
                  <div className="text-xs text-emerald-300 mt-1">
                    +${(market_value?.potential_increase || 0).toLocaleString()}/year
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Hot Jobs */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="glass rounded-2xl p-6"
            >
              <h3 className="text-lg font-bold flex items-center gap-2 mb-4">
                <Zap className="w-5 h-5 text-amber-400" />
                Hot Jobs For You
              </h3>
              
              <div className="space-y-3">
                {hot_jobs?.length > 0 ? (
                  hot_jobs.map((job, index) => (
                    <HotJobCard key={job.id || index} job={job} />
                  ))
                ) : (
                  <div className="text-center py-4 text-muted-foreground text-sm">
                    <Briefcase className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p>Set your preferences to see matching jobs</p>
                  </div>
                )}
              </div>
              
              <Button
                className="w-full mt-4 btn-primary"
                onClick={() => navigate("/auto-apply")}
              >
                See All Jobs <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </motion.div>

            {/* Quick Actions */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="glass rounded-2xl p-6"
            >
              <h3 className="text-lg font-bold mb-4">Quick Actions</h3>
              
              <div className="grid grid-cols-2 gap-3">
                <Button
                  variant="outline"
                  className="h-auto py-3 flex-col"
                  onClick={() => navigate("/cv-generator")}
                >
                  <FileText className="w-5 h-5 mb-1" />
                  <span className="text-xs">Resume</span>
                </Button>
                
                <Button
                  variant="outline"
                  className="h-auto py-3 flex-col"
                  onClick={() => navigate("/cover-letter")}
                >
                  <FileCheck className="w-5 h-5 mb-1" />
                  <span className="text-xs">Cover Letter</span>
                </Button>
                
                <Button
                  variant="outline"
                  className="h-auto py-3 flex-col"
                  onClick={() => navigate("/analyze")}
                >
                  <Brain className="w-5 h-5 mb-1" />
                  <span className="text-xs">Analysis</span>
                </Button>
                
                <Button
                  variant="outline"
                  className="h-auto py-3 flex-col"
                  onClick={() => navigate("/learning-path")}
                >
                  <BookOpen className="w-5 h-5 mb-1" />
                  <span className="text-xs">Learn</span>
                </Button>
              </div>
            </motion.div>
          </div>
        </div>
      </main>
    </div>
  );
}
