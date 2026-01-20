import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../lib/api";
import {
  BookOpen, Target, Sparkles, Loader2, ExternalLink, Clock,
  ChevronDown, ChevronUp, CheckCircle2, AlertCircle, Download,
  Calendar, Award, Briefcase, Code, Upload, FileText, Heart,
  Check, Circle, BookmarkPlus, Bookmark, Zap, Star
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Progress } from "../components/ui/progress";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import AppNavigation from "../components/AppNavigation";

// API base URL configured in lib/api.js

const LOCATIONS = [
  { id: "us", name: "US", flag: "🇺🇸" },
  { id: "india", name: "India", flag: "🇮🇳" },
  { id: "europe", name: "Europe", flag: "🇪🇺" },
  { id: "brazil", name: "Brazil", flag: "🇧🇷" },
  { id: "se_asia", name: "SE Asia", flag: "🌏" }
];

// Learning Path Generation Status Bar
const GenerationStatus = ({ stage, progress }) => {
  const stages = [
    { id: 1, name: "Analyzing Profile", icon: "📊" },
    { id: 2, name: "Matching Courses", icon: "📚" },
    { id: 3, name: "Creating Timeline", icon: "📅" },
    { id: 4, name: "Generating Path", icon: "🎯" },
    { id: 5, name: "Finalizing", icon: "✅" }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-2xl p-6 space-y-4"
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-semibold flex items-center gap-2">
          <Loader2 className="w-5 h-5 animate-spin text-indigo-400" />
          Creating Your Learning Path...
        </h3>
        <span className="text-sm text-muted-foreground">{Math.round(progress)}%</span>
      </div>

      <Progress value={progress} className="h-2" />

      <div className="grid grid-cols-5 gap-2 mt-4">
        {stages.map((s) => (
          <div
            key={s.id}
            className={`text-center p-2 rounded-lg transition-all ${s.id < stage ? "bg-indigo-500/20 text-indigo-300" :
                s.id === stage ? "bg-purple-500/30 text-purple-300 animate-pulse" :
                  "bg-white/5 text-muted-foreground"
              }`}
          >
            <div className="text-lg mb-1">{s.icon}</div>
            <div className="text-xs">{s.name}</div>
          </div>
        ))}
      </div>

      <p className="text-center text-sm text-muted-foreground mt-2">
        This usually takes 20-40 seconds. Curating personalized courses from 28+ sources...
      </p>
    </motion.div>
  );
};

// Fast Track Banner Component
const FastTrackBanner = ({ fastTrack, isCollapsed, onToggle }) => {
  if (!fastTrack?.enabled) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-6"
    >
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-amber-500/20 via-orange-500/20 to-red-500/20 border border-amber-500/30">
        {/* Animated glow effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-amber-500/10 via-orange-500/10 to-red-500/10 animate-pulse" />

        <div className="relative p-5">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-lg flex items-center gap-2">
                  {fastTrack.title}
                  <span className="px-2 py-0.5 text-xs rounded-full bg-amber-500/30 text-amber-300">
                    Recommended
                  </span>
                </h3>
                <p className="text-sm text-muted-foreground">{fastTrack.description}</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={onToggle}
              className="text-amber-400 hover:text-amber-300"
            >
              {isCollapsed ? <ChevronDown className="w-5 h-5" /> : <ChevronUp className="w-5 h-5" />}
            </Button>
          </div>

          <AnimatePresence>
            {!isCollapsed && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="overflow-hidden"
              >
                <div className="mt-4 grid md:grid-cols-2 gap-4">
                  {fastTrack.courses?.map((course, idx) => (
                    <a
                      key={idx}
                      href={course.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group block p-4 rounded-xl bg-black/20 border border-white/10 hover:border-amber-500/50 transition-all hover:bg-black/30"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h4 className="font-semibold group-hover:text-amber-400 transition-colors flex items-center gap-2">
                            {course.name}
                            <ExternalLink className="w-3 h-3 opacity-50 group-hover:opacity-100" />
                          </h4>
                          <p className="text-xs text-muted-foreground">{course.platform} • {course.duration}</p>
                        </div>
                        {course.badge && (
                          <span className="px-2 py-0.5 text-xs rounded-full bg-amber-500/20 text-amber-300 whitespace-nowrap">
                            {course.badge}
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-muted-foreground mb-2">{course.description}</p>
                      <p className="text-xs text-amber-400/80">💡 {course.why}</p>
                    </a>
                  ))}
                </div>

                <div className="mt-4 flex flex-wrap gap-2">
                  {fastTrack.benefits?.map((benefit, idx) => (
                    <span key={idx} className="text-xs px-2 py-1 rounded-full bg-white/5 text-muted-foreground">
                      {benefit}
                    </span>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );
};

export default function LearningPathPage() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [generationStage, setGenerationStage] = useState(0);
  const [generationProgress, setGenerationProgress] = useState(0);
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState("");
  const [currentRole, setCurrentRole] = useState("");
  const [yearsExp, setYearsExp] = useState("");
  const [skills, setSkills] = useState("");
  const [location, setLocation] = useState("us");
  const [generatedPath, setGeneratedPath] = useState(null);
  const [usage, setUsage] = useState({ used: 0, limit: 1, credits: 0 });
  const [expandedWeeks, setExpandedWeeks] = useState([1]);
  const [pathHistory, setPathHistory] = useState([]);
  const [fastTrackCollapsed, setFastTrackCollapsed] = useState(false);

  // Interactive learning path state
  const [courseProgress, setCourseProgress] = useState({});
  const [weekProgress, setWeekProgress] = useState({});
  const [overallStats, setOverallStats] = useState({ completedCourses: 0, totalCourses: 0 });
  const [savedCourses, setSavedCourses] = useState([]);
  const [savingCourse, setSavingCourse] = useState(null);

  useEffect(() => {
    fetchRoles();
    fetchUsage();
    fetchHistory();
    fetchSavedCourses();
  }, []);

  // Fetch course progress when path changes
  useEffect(() => {
    if (generatedPath?.id) {
      fetchCourseProgress(generatedPath.id);
    }
  }, [generatedPath?.id]);

  const fetchCourseProgress = async (pathId) => {
    try {
      const response = await api.get(`/learning-path/${pathId}/course-progress`);
      setCourseProgress(response.data.course_progress || {});
      setWeekProgress(response.data.week_progress || {});
      setOverallStats({
        completedCourses: response.data.stats?.completed_courses || 0,
        totalCourses: response.data.stats?.total_courses || 0
      });
    } catch (error) {
      // New path, no progress yet
      setCourseProgress({});
      setWeekProgress({});
    }
  };

  const fetchSavedCourses = async () => {
    try {
      const response = await api.get(`/user/saved-courses`);
      setSavedCourses(response.data.saved_courses || []);
    } catch (error) {
      console.error("Failed to fetch saved courses:", error);
    }
  };

  const toggleCourseComplete = async (weekNum, courseIndex) => {
    if (!generatedPath?.id) {
      toast.error("Please generate a learning path first");
      return;
    }

    const weekKey = String(weekNum);
    const courseKey = String(courseIndex);
    const isCurrentlyCompleted = courseProgress[weekKey]?.[courseKey]?.completed || false;

    try {
      const response = await api.post(`/learning-path/${generatedPath.id}/course-progress`, {
        week: weekNum,
        course_index: courseIndex,
        completed: !isCurrentlyCompleted
      });

      // Update local state
      setCourseProgress(prev => ({
        ...prev,
        [weekKey]: {
          ...prev[weekKey],
          [courseKey]: {
            completed: !isCurrentlyCompleted,
            completed_at: !isCurrentlyCompleted ? new Date().toISOString() : null
          }
        }
      }));

      if (response.data.week_completed) {
        setWeekProgress(prev => ({
          ...prev,
          [weekKey]: { completed: true }
        }));
      }

      setOverallStats({
        completedCourses: response.data.total_courses_completed,
        totalCourses: response.data.total_courses
      });

      toast.success(response.data.message);
    } catch (error) {
      toast.error("Failed to update course progress");
    }
  };

  const saveCourse = async (course, weekNum) => {
    if (!generatedPath?.id) {
      toast.error("Please generate a learning path first");
      return;
    }

    const courseUrl = course.url;
    if (savedCourses.some(c => c.course_url === courseUrl)) {
      toast.info("Course already saved!");
      return;
    }

    setSavingCourse(courseUrl);
    try {
      await api.post(`/user/saved-courses`, {
        course_name: course.name,
        course_url: courseUrl,
        platform: course.platform,
        week: weekNum,
        learning_path_id: generatedPath.id
      });

      await fetchSavedCourses();
      toast.success("Course saved to your profile!");
    } catch (error) {
      toast.error(error.response?.data?.detail || "Failed to save course");
    } finally {
      setSavingCourse(null);
    }
  };

  const isCourseCompleted = (weekNum, courseIndex) => {
    return courseProgress[String(weekNum)]?.[String(courseIndex)]?.completed || false;
  };

  const isCourseSaved = (courseUrl) => {
    return savedCourses.some(c => c.course_url === courseUrl);
  };

  const fetchRoles = async () => {
    try {
      const response = await api.get(`/roles?location=${location}`);
      setRoles(response.data.roles || []);
    } catch (error) {
      console.error("Failed to fetch roles:", error);
    }
  };

  const fetchUsage = async () => {
    try {
      const response = await api.get(`/usage`);
      setUsage({
        used: response.data.learning_paths_used,
        limit: response.data.learning_paths_limit,
        credits: response.data.learning_path_credits || 0
      });
    } catch (error) {
      console.error("Failed to fetch usage:", error);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await api.get(`/learning-path/history`);
      setPathHistory(response.data.learning_paths || []);
    } catch (error) {
      console.error("Failed to fetch history:", error);
    }
  };

  useEffect(() => {
    fetchRoles();
  }, [location]);

  const handleGenerate = async () => {
    if (!currentRole.trim() || !selectedRole) {
      toast.error("Please enter your current role and select a target role");
      return;
    }

    setLoading(true);
    setGenerationStage(1);
    setGenerationProgress(10);

    // Simulate progress stages
    const progressInterval = setInterval(() => {
      setGenerationProgress(prev => {
        if (prev >= 90) return prev;
        const newProgress = prev + Math.random() * 12;

        // Update stage based on progress
        if (newProgress > 20 && newProgress <= 40) setGenerationStage(2);
        else if (newProgress > 40 && newProgress <= 60) setGenerationStage(3);
        else if (newProgress > 60 && newProgress <= 80) setGenerationStage(4);
        else if (newProgress > 80) setGenerationStage(5);

        return Math.min(newProgress, 90);
      });
    }, 1000);

    try {
      const response = await api.post(`/learning-path/generate`, {
        current_role: currentRole,
        years_experience: parseInt(yearsExp) || 0,
        current_skills: skills.split(",").map(s => s.trim()).filter(Boolean),
        target_role_id: selectedRole,
        location: location
      });

      clearInterval(progressInterval);
      setGenerationProgress(100);
      setGenerationStage(5);

      setTimeout(() => {
        setGeneratedPath(response.data);
        setUsage(response.data.usage);
        setExpandedWeeks([1]);
        toast.success("Learning path generated with 28+ real courses!");
        fetchHistory();
        setLoading(false);
        setGenerationStage(0);
        setGenerationProgress(0);
      }, 500);

    } catch (error) {
      clearInterval(progressInterval);
      const detail = error.response?.data?.detail;
      let errorMessage = "Failed to generate learning path";

      if (typeof detail === "string") {
        errorMessage = detail;
      } else if (Array.isArray(detail) && detail.length > 0) {
        // Handle Pydantic validation errors array
        errorMessage = detail.map(err => err.msg || err.message || "Validation error").join(", ");
      } else if (typeof detail === "object" && detail?.message) {
        errorMessage = detail.message;
      }

      toast.error(errorMessage);
      setLoading(false);
      setGenerationStage(0);
      setGenerationProgress(0);
    }
  };

  const toggleWeek = (week) => {
    setExpandedWeeks(prev =>
      prev.includes(week) ? prev.filter(w => w !== week) : [...prev, week]
    );
  };

  const expandAll = () => {
    const allWeeks = generatedPath?.learning_path?.weeks?.map(w => w.week) || [];
    setExpandedWeeks(allWeeks);
  };

  const collapseAll = () => {
    setExpandedWeeks([]);
  };

  const downloadPath = async (format = "txt") => {
    if (!generatedPath) return;

    // Check if user can download PDF/DOCX (Pro or has credits)
    if (format !== "txt" && !isPro) {
      toast.error(
        <div className="flex flex-col">
          <span className="font-semibold">PDF/DOCX Download - Pro Feature</span>
          <span className="text-sm">Upgrade to Pro or purchase credits to download as PDF/DOCX</span>
        </div>,
        { duration: 5000 }
      );
      return;
    }

    // Text download (instant, free for all)
    if (format === "txt") {
      let text = `16-WEEK LEARNING PATH\n`;
      text += `From: ${generatedPath.current_role} → To: ${generatedPath.target_role}\n`;
      text += `Estimated Salary: ${generatedPath.location_salary}\n\n`;

      generatedPath.learning_path?.weeks?.forEach(week => {
        text += `\n=== WEEK ${week.week}: ${week.focus} ===\n`;
        text += `Hours: ${week.hours}\n`;
        text += `Phase: ${week.phase || ''}\n\n`;

        if (week.courses?.length) {
          text += `Courses:\n`;
          week.courses.forEach(c => {
            text += `• ${c.name} (${c.platform}) - ${c.url}\n`;
          });
        }

        if (week.milestones?.length) {
          text += `\nMilestones:\n`;
          week.milestones.forEach(m => text += `• ${m}\n`);
        }

        if (week.projects?.length) {
          text += `\nProjects:\n`;
          week.projects.forEach(p => text += `• ${p}\n`);
        }
      });

      const blob = new Blob([text], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const userName = user?.name?.replace(/\s+/g, '_') || 'User';
      const role = generatedPath.target_role?.replace(/\s+/g, '_') || 'AI_Role';
      a.download = `${userName}_${role}_Learning_Path.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      toast.success("Learning path downloaded as TXT!");
      return;
    }

    // PDF/DOCX download via API
    try {
      toast.loading(`Generating ${format.toUpperCase()}...`, { id: 'download' });

      const response = await api.post(
        `/learning-path/download-direct?format=${format}`,
        {
          path_data: generatedPath.learning_path,
          target_role: generatedPath.target_role,
          user_name: user?.name || "User"
        },
        { responseType: 'blob' }
      );

      const blob = new Blob([response.data], {
        type: format === "pdf"
          ? "application/pdf"
          : "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const userName = (user?.name || 'User').replace(/[^\w\s-]/g, '').replace(/\s+/g, '_');
      const role = (generatedPath.target_role || 'AI_Role').replace(/[^\w\s-]/g, '').replace(/\s+/g, '_');
      a.download = `${userName}_${role}_Learning_Path.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      toast.dismiss('download');
      toast.success(`Learning path downloaded as ${format.toUpperCase()}!`);
    } catch (error) {
      toast.dismiss('download');
      console.error("Download error:", error);
      toast.error(`Failed to generate ${format.toUpperCase()}. Try TXT instead.`);
    }
  };

  const markWeekComplete = async (weekNum) => {
    if (!generatedPath?.id) {
      toast.error("Save your learning path first");
      return;
    }

    try {
      const response = await api.post(`/learning-path/${generatedPath.id}/progress`, {
        week: weekNum,
        completed: !weekProgress[weekNum]?.completed
      });

      setWeekProgress(prev => ({
        ...prev,
        [weekNum]: { completed: !prev[weekNum]?.completed }
      }));

      toast.success(response.data.message);
    } catch (error) {
      toast.error("Failed to update progress");
    }
  };

  // Resume upload for skill parsing
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleResumeUpload = async (file) => {
    if (!file) return;

    setUploading(true);
    setUploadProgress(0);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post(`/resume/parse`, formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        }
      });

      if (response.data) {
        // Extract skills from parsed resume
        const extractedSkills = response.data.extracted_skills || [];
        const extractedRole = response.data.current_role || "";
        const extractedYears = response.data.years_experience || "";

        // Update form fields
        if (extractedSkills.length > 0) {
          setSkills(extractedSkills.join(", "));
        }
        if (extractedRole) {
          setCurrentRole(extractedRole);
        }
        if (extractedYears) {
          setYearsExp(String(extractedYears));
        }

        toast.success("Resume parsed! Skills and experience extracted.");
      }
    } catch (error) {
      toast.error("Failed to parse resume");
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const trackCourseClick = async (course) => {
    try {
      await api.post(`/analytics/course-click`, {
        course_id: course.course_id || course.name?.toLowerCase().replace(/\s+/g, '_'),
        course_name: course.name,
        course_url: course.url,
        learning_path_id: generatedPath?.id
      });
    } catch (error) {
      // Silent fail for analytics
      console.log("Analytics tracking:", error.message);
    }
  };

  const isPro = user?.subscription_tier === "pro";
  const canGenerate = isPro || usage.used < usage.limit || usage.credits > 0;
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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
                <BookOpen className="w-8 h-8 text-purple-400" />
                Learning Path Generator
              </h1>
              <p className="text-muted-foreground">
                Generate a personalized 16-week roadmap with real courses and clickable links
              </p>
            </div>

            {/* Usage Counter */}
            <div className="glass rounded-xl px-6 py-4 text-center">
              <div className="text-sm text-muted-foreground mb-1">FREE this month</div>
              <div className="text-2xl font-bold">
                <span className={usage.used >= usage.limit && !isPro ? "text-red-400" : "text-purple-400"}>
                  {usage.used}
                </span>
                <span className="text-muted-foreground">/{isPro ? "∞" : usage.limit}</span>
              </div>
              {usage.credits > 0 && (
                <div className="text-xs text-amber-400 mt-1">+{usage.credits} credits</div>
              )}
              {!canGenerate && (
                <Button size="sm" className="mt-2 btn-primary text-xs" data-testid="lp-buy-more-btn">
                  Buy More: $0.99
                </Button>
              )}
            </div>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Input Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="space-y-6"
          >
            {/* Current State */}
            <div className="glass rounded-2xl p-6 space-y-4">
              <Label className="text-lg font-semibold block">Your Current State</Label>

              {/* Resume Upload for Auto-Fill */}
              <div className="p-4 bg-purple-500/10 border border-purple-500/30 rounded-xl">
                <input
                  type="file"
                  accept=".pdf,.doc,.docx,.txt"
                  className="hidden"
                  id="lp-resume-upload"
                  onChange={(e) => handleResumeUpload(e.target.files?.[0])}
                  disabled={uploading}
                  data-testid="lp-resume-upload"
                />

                {uploading ? (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 text-purple-400 animate-spin" />
                      <span className="text-sm text-purple-300">Parsing resume...</span>
                      <span className="text-sm font-bold text-purple-400">{Math.round(uploadProgress)}%</span>
                    </div>
                    <Progress value={uploadProgress} className="h-1.5" />
                  </div>
                ) : (
                  <label htmlFor="lp-resume-upload" className="flex items-center gap-3 cursor-pointer">
                    <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center">
                      <Upload className="w-5 h-5 text-purple-400" />
                    </div>
                    <div>
                      <div className="text-sm font-medium text-purple-300">Upload Resume to Auto-Fill</div>
                      <div className="text-xs text-muted-foreground">We&apos;ll extract your skills and experience automatically</div>
                    </div>
                  </label>
                )}
              </div>

              <div>
                <Label htmlFor="lp-current-role" className="text-sm">Current Role *</Label>
                <div className="relative mt-1">
                  <Briefcase className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    id="lp-current-role"
                    placeholder="e.g., Software Engineer"
                    className="pl-10 input-dark"
                    value={currentRole}
                    onChange={(e) => setCurrentRole(e.target.value)}
                    data-testid="lp-current-role-input"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="lp-years" className="text-sm">Years Experience</Label>
                <div className="relative mt-1">
                  <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    id="lp-years"
                    type="number"
                    placeholder="e.g., 5"
                    className="pl-10 input-dark"
                    value={yearsExp}
                    onChange={(e) => setYearsExp(e.target.value)}
                    data-testid="lp-years-input"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="lp-skills" className="text-sm">Current Skills (comma separated)</Label>
                <div className="relative mt-1">
                  <Code className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    id="lp-skills"
                    placeholder="e.g., Python, SQL, Excel"
                    className="pl-10 input-dark"
                    value={skills}
                    onChange={(e) => setSkills(e.target.value)}
                    data-testid="lp-skills-input"
                  />
                </div>
              </div>
            </div>

            {/* Location */}
            <div className="glass rounded-2xl p-6">
              <Label className="text-lg font-semibold mb-4 block">Your Location</Label>
              <div className="grid grid-cols-5 gap-2">
                {LOCATIONS.map((loc) => (
                  <button
                    key={loc.id}
                    type="button"
                    onClick={() => setLocation(loc.id)}
                    className={`
                      p-2 rounded-lg text-center transition-all text-xs
                      ${location === loc.id
                        ? 'bg-purple-500/20 border-2 border-purple-500 text-purple-300'
                        : 'bg-white/5 border border-white/10 hover:border-purple-500/50'
                      }
                    `}
                    data-testid={`lp-location-${loc.id}`}
                  >
                    <div className="text-lg">{loc.flag}</div>
                    <div>{loc.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Target Role */}
            <div className="glass rounded-2xl p-6">
              <Label className="text-lg font-semibold mb-4 block">
                <Target className="w-5 h-5 inline mr-2 text-purple-400" />
                Target AI Role
              </Label>

              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="w-full h-12 px-4 rounded-lg bg-black/20 border border-white/10 text-foreground focus:border-purple-500"
                data-testid="lp-role-select"
              >
                <option value="">Select a role...</option>
                {roles.map((role) => (
                  <option key={role.id} value={role.id}>
                    {role.name} ({role.transition_weeks}w)
                  </option>
                ))}
              </select>

              {selectedRoleData && (
                <div className="mt-4 p-3 rounded-lg bg-purple-500/10 border border-purple-500/30">
                  <div className="text-sm font-medium text-purple-300">{selectedRoleData.name}</div>
                  <div className="text-xs text-muted-foreground mt-1">{selectedRoleData.description}</div>
                  <div className="flex items-center gap-4 mt-2 text-xs">
                    <span className="text-emerald-400">
                      {selectedRoleData.local_salary || selectedRoleData.salary_range}
                    </span>
                    <span className="text-amber-400">{selectedRoleData.transition_weeks} weeks</span>
                  </div>
                </div>
              )}
            </div>

            {/* Generate Button */}
            <Button
              onClick={handleGenerate}
              disabled={loading || !canGenerate || !currentRole.trim() || !selectedRole}
              className="w-full btn-primary py-6 text-lg bg-gradient-to-r from-purple-500 to-indigo-500"
              data-testid="lp-generate-btn"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                  Generating 16-Week Path...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 mr-2" />
                  Generate Learning Path
                </>
              )}
            </Button>

            {!canGenerate && (
              <div className="glass rounded-xl p-4 border border-amber-500/30">
                <div className="flex items-center gap-2 text-amber-400 mb-2">
                  <AlertCircle className="w-5 h-5" />
                  <span className="font-medium">Free limit reached</span>
                </div>
                <div className="flex gap-2">
                  <Button size="sm" className="btn-secondary text-xs">$0.99 for 1</Button>
                  <Button size="sm" className="btn-secondary text-xs">$3.99 for 5</Button>
                  <Button size="sm" className="btn-primary text-xs">$29/mo Pro</Button>
                </div>
              </div>
            )}

            {/* History */}
            {pathHistory.length > 0 && (
              <div className="glass rounded-2xl p-6">
                <h3 className="font-semibold mb-4">Recent Paths</h3>
                <div className="space-y-2">
                  {pathHistory.slice(0, 3).map((path) => (
                    <div
                      key={path.id}
                      className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer"
                      onClick={() => setGeneratedPath({
                        current_role: path.current_role,
                        target_role: path.target_role,
                        learning_path: path.path_data
                      })}
                    >
                      <div>
                        <div className="font-medium text-sm">{path.target_role}</div>
                        <div className="text-xs text-muted-foreground">
                          from {path.current_role}
                        </div>
                      </div>
                      <BookOpen className="w-4 h-4 text-muted-foreground" />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>

          {/* Output Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2 space-y-6"
          >
            {/* Show loading status bar while generating */}
            {loading && (
              <GenerationStatus stage={generationStage} progress={generationProgress} />
            )}

            {!loading && generatedPath ? (
              <>
                {/* Summary with Progress Stats */}
                <div className="glass rounded-2xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h2 className="text-xl font-bold">
                        {generatedPath.current_role} → {generatedPath.target_role}
                      </h2>
                      <p className="text-muted-foreground">
                        {generatedPath.learning_path?.total_weeks || 16} weeks • {generatedPath.learning_path?.hours_per_week || 15}h/week • {generatedPath.location_salary}
                      </p>
                    </div>
                    <div className="flex gap-1">
                      <Button size="sm" variant="ghost" onClick={expandAll}>Expand All</Button>
                      <Button size="sm" variant="ghost" onClick={collapseAll}>Collapse</Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => downloadPath("pdf")}
                        className="text-red-400 hover:text-red-300"
                        title="Download PDF"
                        data-testid="lp-download-pdf"
                      >
                        <Download className="w-4 h-4 mr-1" />
                        <span className="text-xs">PDF</span>
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => downloadPath("docx")}
                        className="text-blue-400 hover:text-blue-300"
                        title="Download Word"
                        data-testid="lp-download-docx"
                      >
                        <Download className="w-4 h-4 mr-1" />
                        <span className="text-xs">DOCX</span>
                      </Button>
                    </div>
                  </div>

                  {/* Progress Stats */}
                  {generatedPath.id && (
                    <div className="grid grid-cols-3 gap-4 mb-4">
                      <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                        <div className="text-2xl font-bold text-emerald-400">
                          {overallStats.completedCourses}/{overallStats.totalCourses}
                        </div>
                        <div className="text-xs text-muted-foreground">Courses Completed</div>
                      </div>
                      <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20">
                        <div className="text-2xl font-bold text-purple-400">
                          {Object.values(weekProgress).filter(w => w?.completed).length}/{generatedPath.learning_path?.weeks?.length || 16}
                        </div>
                        <div className="text-xs text-muted-foreground">Weeks Completed</div>
                      </div>
                      <div className="p-3 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
                        <div className="text-2xl font-bold text-indigo-400">
                          {overallStats.totalCourses > 0
                            ? Math.round((overallStats.completedCourses / overallStats.totalCourses) * 100)
                            : 0}%
                        </div>
                        <div className="text-xs text-muted-foreground">Overall Progress</div>
                      </div>
                    </div>
                  )}

                  <Progress
                    value={overallStats.totalCourses > 0
                      ? (overallStats.completedCourses / overallStats.totalCourses) * 100
                      : 0
                    }
                    className="h-2"
                  />
                  <p className="text-xs text-muted-foreground mt-2 text-center">
                    {generatedPath.id
                      ? "Click the circle next to each course to mark it complete"
                      : "Progress tracking available after path is saved"
                    }
                  </p>
                </div>

                {/* Fast Track Banner */}
                <FastTrackBanner
                  fastTrack={generatedPath.learning_path?.fast_track}
                  isCollapsed={fastTrackCollapsed}
                  onToggle={() => setFastTrackCollapsed(!fastTrackCollapsed)}
                />

                {/* Week by Week Timeline */}
                <div className="space-y-4">
                  {generatedPath.learning_path?.weeks?.map((week, index) => {
                    const isWeekCompleted = weekProgress[String(week.week)]?.completed;
                    const weekCourseCount = week.courses?.length || 0;
                    const completedInWeek = week.courses?.filter((_, i) =>
                      isCourseCompleted(week.week, i)
                    ).length || 0;

                    return (
                      <motion.div
                        key={week.week}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.05 }}
                        className={`glass rounded-xl overflow-hidden ${isWeekCompleted ? "ring-2 ring-emerald-500/50" : ""
                          }`}
                      >
                        <div
                          className="p-4 cursor-pointer flex items-center justify-between hover:bg-white/5"
                          onClick={() => toggleWeek(week.week)}
                        >
                          <div className="flex items-center gap-4">
                            <div className={`
                              w-12 h-12 rounded-xl flex items-center justify-center font-bold relative
                              ${isWeekCompleted
                                ? "bg-emerald-500/30 text-emerald-300"
                                : week.phase === "Foundation" ? "bg-blue-500/20 text-blue-400" :
                                  week.phase === "Core" ? "bg-purple-500/20 text-purple-400" :
                                    week.phase === "Advanced" ? "bg-orange-500/20 text-orange-400" :
                                      "bg-emerald-500/20 text-emerald-400"}
                            `}>
                              {isWeekCompleted ? (
                                <CheckCircle2 className="w-6 h-6" />
                              ) : (
                                `W${week.week}`
                              )}
                            </div>
                            <div>
                              <h3 className={`font-semibold ${isWeekCompleted ? "text-emerald-300" : ""}`}>
                                Week {week.week}: {week.theme}
                              </h3>
                              <p className="text-sm text-muted-foreground">{week.focus}</p>
                              <div className="flex items-center gap-3 text-sm text-muted-foreground mt-1">
                                <span className="flex items-center gap-1">
                                  <Clock className="w-3 h-3" /> {week.hours}h
                                </span>
                                {weekCourseCount > 0 && (
                                  <span className={`px-2 py-0.5 rounded-full text-xs ${completedInWeek === weekCourseCount
                                      ? "bg-emerald-500/20 text-emerald-300"
                                      : "bg-white/10"
                                    }`}>
                                    {completedInWeek}/{weekCourseCount} courses
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            {isWeekCompleted && (
                              <span className="text-xs text-emerald-400 font-medium">Complete</span>
                            )}
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
                            className="px-4 pb-4 space-y-4 border-t border-white/10"
                          >
                            {/* Courses */}
                            {week.courses?.length > 0 && (
                              <div className="pt-4">
                                <div className="text-sm font-medium text-indigo-400 mb-3 flex items-center justify-between">
                                  <span className="flex items-center gap-2">
                                    <BookOpen className="w-4 h-4" /> Recommended Courses
                                  </span>
                                  <span className="text-xs text-muted-foreground">
                                    {week.courses.filter((_, i) => isCourseCompleted(week.week, i)).length}/{week.courses.length} completed
                                  </span>
                                </div>
                                <div className="grid gap-3">
                                  {week.courses.map((course, i) => {
                                    const isCompleted = isCourseCompleted(week.week, i);
                                    const isSaved = isCourseSaved(course.url);

                                    return (
                                      <div
                                        key={i}
                                        className={`p-4 rounded-xl border transition-all group ${isCompleted
                                            ? "bg-emerald-500/10 border-emerald-500/30"
                                            : "bg-white/5 border-white/10 hover:border-indigo-500/30"
                                          }`}
                                      >
                                        <div className="flex items-start gap-3">
                                          {/* Completion checkbox */}
                                          <button
                                            onClick={() => toggleCourseComplete(week.week, i)}
                                            className={`mt-1 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all flex-shrink-0 ${isCompleted
                                                ? "bg-emerald-500 border-emerald-500 text-white"
                                                : "border-white/30 hover:border-emerald-400"
                                              }`}
                                            data-testid={`course-complete-${week.week}-${i}`}
                                          >
                                            {isCompleted && <Check className="w-4 h-4" />}
                                          </button>

                                          <div className="flex-1 min-w-0">
                                            <div className={`font-semibold transition-colors ${isCompleted
                                                ? "text-emerald-300 line-through opacity-80"
                                                : "text-white group-hover:text-indigo-300"
                                              }`}>
                                              {course.name}
                                            </div>
                                            <div className="flex items-center flex-wrap gap-2 mt-2 text-xs">
                                              <span className="px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300">
                                                {course.platform}
                                              </span>
                                              <span className="flex items-center gap-1 text-muted-foreground">
                                                <Clock className="w-3 h-3" />
                                                {course.duration_hours ? `${course.duration_hours}h` : course.duration}
                                              </span>
                                              <span className={`px-2 py-0.5 rounded-full ${course.cost_type === "free"
                                                  ? "bg-emerald-500/20 text-emerald-300"
                                                  : course.cost_type === "freemium"
                                                    ? "bg-blue-500/20 text-blue-300"
                                                    : "bg-amber-500/20 text-amber-300"
                                                }`}>
                                                {course.cost_type === "free" ? "🆓 Free" :
                                                  course.cost_type === "freemium" ? "Free to audit" :
                                                    course.cost || "Paid"}
                                              </span>
                                              {course.badge && (
                                                <span className="px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300">
                                                  {course.badge}
                                                </span>
                                              )}
                                              {course.is_optional && (
                                                <span className="px-2 py-0.5 rounded-full bg-gray-500/20 text-gray-300">
                                                  Optional (Paid)
                                                </span>
                                              )}
                                              {isCompleted && (
                                                <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300">
                                                  ✓ Completed
                                                </span>
                                              )}
                                            </div>
                                            {course.why_recommended && (
                                              <p className="mt-2 text-xs text-muted-foreground italic">
                                                💡 {course.why_recommended}
                                              </p>
                                            )}
                                          </div>

                                          <div className="flex items-center gap-2 flex-shrink-0">
                                            {/* Save course button */}
                                            <button
                                              onClick={() => saveCourse(course, week.week)}
                                              disabled={savingCourse === course.url || isSaved}
                                              className={`p-2 rounded-lg transition-colors ${isSaved
                                                  ? "bg-pink-500/20 text-pink-400"
                                                  : "bg-white/5 text-muted-foreground hover:bg-pink-500/20 hover:text-pink-400"
                                                }`}
                                              title={isSaved ? "Saved" : "Save to profile"}
                                              data-testid={`course-save-${week.week}-${i}`}
                                            >
                                              {savingCourse === course.url ? (
                                                <Loader2 className="w-4 h-4 animate-spin" />
                                              ) : isSaved ? (
                                                <Bookmark className="w-4 h-4 fill-current" />
                                              ) : (
                                                <BookmarkPlus className="w-4 h-4" />
                                              )}
                                            </button>

                                            {/* Take course link */}
                                            <a
                                              href={course.url}
                                              target="_blank"
                                              rel="noopener noreferrer"
                                              onClick={() => trackCourseClick(course)}
                                              className="px-3 py-2 rounded-lg bg-indigo-500/20 text-indigo-300 hover:bg-indigo-500/30 transition-colors flex items-center gap-1 text-sm font-medium whitespace-nowrap"
                                              data-testid={`course-link-${week.week}-${i}`}
                                            >
                                              Take Course
                                              <ExternalLink className="w-3 h-3" />
                                            </a>
                                          </div>
                                        </div>
                                      </div>
                                    );
                                  })}
                                </div>
                              </div>
                            )}

                            {/* Milestones */}
                            {week.milestones?.length > 0 && (
                              <div>
                                <div className="text-sm font-medium text-emerald-400 mb-2 flex items-center gap-2">
                                  <CheckCircle2 className="w-4 h-4" /> Milestones
                                </div>
                                <ul className="space-y-1">
                                  {week.milestones.map((m, i) => (
                                    <li key={i} className="flex items-start gap-2 text-sm">
                                      <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                                      {m}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}

                            {/* Projects */}
                            {week.projects?.length > 0 && (
                              <div>
                                <div className="text-sm font-medium text-amber-400 mb-2 flex items-center gap-2">
                                  <Award className="w-4 h-4" /> Projects
                                </div>
                                <ul className="space-y-1">
                                  {week.projects.map((p, i) => (
                                    <li key={i} className="flex items-start gap-2 text-sm">
                                      <span className="text-amber-400">•</span>
                                      {p}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}

                            {/* Skills */}
                            {week.skills_developed?.length > 0 && (
                              <div className="flex flex-wrap gap-2">
                                {week.skills_developed.map((skill, i) => (
                                  <span key={i} className="px-2 py-1 rounded-full bg-purple-500/20 text-purple-300 text-xs">
                                    {skill}
                                  </span>
                                ))}
                              </div>
                            )}
                          </motion.div>
                        )}
                      </motion.div>
                    );
                  })}
                </div>

                {/* Career Readiness */}
                {generatedPath.learning_path?.career_readiness_checklist?.length > 0 && (
                  <div className="glass rounded-2xl p-6">
                    <h3 className="font-semibold mb-4 flex items-center gap-2">
                      <Award className="w-5 h-5 text-emerald-400" />
                      Career Readiness Checklist
                    </h3>
                    <ul className="space-y-2">
                      {generatedPath.learning_path.career_readiness_checklist.map((item, i) => (
                        <li key={i} className="flex items-center gap-2">
                          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                          {item}
                        </li>
                      ))}
                    </ul>
                    {generatedPath.learning_path.job_search_timeline && (
                      <div className="mt-4 p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
                        <Calendar className="w-4 h-4 inline mr-2 text-emerald-400" />
                        {generatedPath.learning_path.job_search_timeline}
                      </div>
                    )}
                  </div>
                )}
              </>
            ) : !loading ? (
              <div className="glass rounded-2xl p-12 text-center lg:col-span-2">
                <BookOpen className="w-16 h-16 text-muted-foreground mx-auto mb-4 opacity-50" />
                <h3 className="text-lg font-semibold mb-2">No Learning Path Generated Yet</h3>
                <p className="text-muted-foreground">
                  Enter your current state, select a target role, and generate your personalized 16-week roadmap with real courses.
                </p>
              </div>
            ) : null}
          </motion.div>
        </div>
      </main>
    </div>
  );
}
