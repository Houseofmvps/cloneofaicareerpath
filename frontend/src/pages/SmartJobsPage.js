import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
import {
  Zap, Search, Building2, MapPin, DollarSign, CheckCircle2,
  Clock, Briefcase, Settings, ToggleLeft, ToggleRight, Filter,
  ExternalLink, Send, Eye, Calendar, TrendingUp, AlertCircle,
  Loader2, RefreshCw, Play, Pause, Bell, Mail, BellRing,
  Copy, FileText, X, Sparkles, ArrowRight
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Progress } from "../components/ui/progress";
import { Switch } from "../components/ui/switch";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import AppNavigation from "../components/AppNavigation";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const ROLE_OPTIONS = [
  "AI/ML Engineer", "Prompt Engineer", "MLOps Engineer", "Data Scientist",
  "Generative AI Developer", "NLP Engineer", "Computer Vision Engineer",
  "AI Research Scientist", "AI Product Manager", "AI Solutions Architect"
];

const LOCATION_OPTIONS = [
  "Remote (US)", "Remote (Global)", "San Francisco, CA", "New York, NY",
  "Seattle, WA", "Austin, TX", "Boston, MA", "Los Angeles, CA",
  "London, UK", "Berlin, Germany", "Singapore", "Bangalore, India"
];

const COMPANY_TYPE_OPTIONS = [
  { id: "faang", name: "FAANG+", description: "Google, Meta, Amazon, etc." },
  { id: "startup", name: "Startups", description: "Early-stage, fast-paced" },
  { id: "enterprise", name: "Enterprise", description: "Large corporations" },
  { id: "ai_native", name: "AI-Native", description: "OpenAI, Anthropic, etc." }
];

// Status Badge Component
const StatusBadge = ({ status }) => {
  const statusConfig = {
    pending: { color: "bg-gray-500/20 text-gray-300", label: "Saved" },
    applied: { color: "bg-blue-500/20 text-blue-300", label: "Applied" },
    viewed: { color: "bg-amber-500/20 text-amber-300", label: "Viewed" },
    interview_scheduled: { color: "bg-emerald-500/20 text-emerald-300", label: "Interview" },
    offer: { color: "bg-green-500/20 text-green-300", label: "Offer!" },
    rejected: { color: "bg-red-500/20 text-red-300", label: "Rejected" }
  };
  
  const config = statusConfig[status] || statusConfig.applied;
  
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
      {config.label}
    </span>
  );
};

// Apply Preparation Modal
const ApplyModal = ({ job, isOpen, onClose, onApplyComplete }) => {
  const [coverLetter, setCoverLetter] = useState("");
  const [generating, setGenerating] = useState(false);
  const [copied, setCopied] = useState(false);
  const [selectedTone, setSelectedTone] = useState("professional");

  useEffect(() => {
    if (isOpen && job) {
      generateCoverLetter();
    }
  }, [isOpen, job, selectedTone]);

  const generateCoverLetter = async () => {
    setGenerating(true);
    try {
      const response = await axios.post(`${API}/auto-apply/prepare-application`, {
        job_id: job.id,
        job_title: job.title,
        company: job.company,
        job_description: job.description,
        job_url: job.job_url,
        cover_letter_tone: selectedTone
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      setCoverLetter(response.data.cover_letter);
    } catch (error) {
      console.error("Failed to generate cover letter:", error);
      setCoverLetter(`Dear Hiring Manager,\n\nI am excited to apply for the ${job.title} position at ${job.company}. With my background in AI and machine learning, I am confident I can make meaningful contributions to your team.\n\nBest regards`);
    } finally {
      setGenerating(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(coverLetter);
    setCopied(true);
    toast.success("Cover letter copied to clipboard!");
    setTimeout(() => setCopied(false), 2000);
  };

  const handleApplyNow = async () => {
    // Track the application
    await onApplyComplete(job);
    // Open job page
    window.open(job.job_url, "_blank");
    toast.success(`Opening ${job.company} - Don't forget to paste your cover letter!`);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="glass rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden"
      >
        {/* Header */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-xl font-bold flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-indigo-400" />
                Prepare Your Application
              </h2>
              <p className="text-sm text-muted-foreground mt-1">
                {job.title} at {job.company}
              </p>
            </div>
            <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-lg">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6 max-h-[60vh] overflow-y-auto">
          {/* Job Summary */}
          <div className="bg-white/5 rounded-xl p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-indigo-500/20 flex items-center justify-center text-xl">
                {job.company_logo || "🏢"}
              </div>
              <div className="flex-1">
                <div className="font-medium">{job.title}</div>
                <div className="text-sm text-muted-foreground">{job.company} • {job.location}</div>
              </div>
              <div className="text-right">
                <div className="text-emerald-400 font-medium">{job.salary_range}</div>
                <div className="text-xs text-indigo-400">{job.match_score}% match</div>
              </div>
            </div>
          </div>

          {/* Cover Letter Section */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <Label className="text-sm font-medium">AI-Generated Cover Letter</Label>
              <div className="flex gap-1">
                {["professional", "confident", "story-driven"].map((tone) => (
                  <button
                    key={tone}
                    onClick={() => setSelectedTone(tone)}
                    className={`text-xs px-2 py-1 rounded ${
                      selectedTone === tone 
                        ? "bg-indigo-500 text-white" 
                        : "bg-white/10 hover:bg-white/20"
                    }`}
                  >
                    {tone.charAt(0).toUpperCase() + tone.slice(1)}
                  </button>
                ))}
              </div>
            </div>
            
            {generating ? (
              <div className="bg-black/20 rounded-xl p-8 flex items-center justify-center">
                <Loader2 className="w-6 h-6 animate-spin text-indigo-400" />
                <span className="ml-2 text-muted-foreground">Generating cover letter...</span>
              </div>
            ) : (
              <div className="relative">
                <textarea
                  value={coverLetter}
                  onChange={(e) => setCoverLetter(e.target.value)}
                  className="w-full h-48 bg-black/20 border border-white/10 rounded-xl p-4 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                  placeholder="Your cover letter will appear here..."
                />
                <button
                  onClick={copyToClipboard}
                  className="absolute top-3 right-3 p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
                  title="Copy to clipboard"
                >
                  {copied ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                </button>
              </div>
            )}
          </div>

          {/* Instructions */}
          <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
            <h4 className="font-medium text-indigo-300 mb-2">How to Apply:</h4>
            <ol className="text-sm text-muted-foreground space-y-1">
              <li>1. Copy your cover letter above (click the copy icon)</li>
              <li>2. Click the Open Job and Apply button below</li>
              <li>3. Paste your cover letter in the application form</li>
              <li>4. Submit your application on the job site</li>
            </ol>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-white/10 flex items-center justify-between">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <div className="flex gap-3">
            <Button variant="outline" onClick={copyToClipboard} disabled={generating}>
              <Copy className="w-4 h-4 mr-2" />
              {copied ? "Copied!" : "Copy Letter"}
            </Button>
            <Button 
              className="btn-primary"
              onClick={handleApplyNow}
              disabled={generating}
              data-testid="open-and-apply-btn"
            >
              Open Job & Apply
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

// Job Card Component
const JobCard = ({ job, onApply, applied, onOpenApplyModal }) => {
  // Source badge color
  const sourceColors = {
    adzuna: "bg-blue-500/20 text-blue-300 border-blue-500/30",
    remoteok: "bg-green-500/20 text-green-300 border-green-500/30",
    mock: "bg-amber-500/20 text-amber-300 border-amber-500/30"
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass rounded-xl p-4 hover:bg-white/5 transition-colors"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3">
          <div className="w-12 h-12 rounded-xl bg-indigo-500/20 flex items-center justify-center text-2xl">
            {job.company_logo || "🏢"}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-semibold">{job.title}</h3>
              {job.is_easy_apply && (
                <span className="text-xs bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded-full flex items-center gap-1">
                  <Zap className="w-2.5 h-2.5" /> Easy
                </span>
              )}
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Building2 className="w-3 h-3" />
              {job.company}
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <MapPin className="w-3 h-3" />
              {job.location}
            </div>
          </div>
        </div>
        
        <div className="text-right">
          <div className="text-sm font-medium text-emerald-400">{job.salary_range}</div>
          <div className="text-xs text-muted-foreground mt-1">
            Match: <span className="text-indigo-400 font-semibold">{job.match_score}%</span>
          </div>
          {job.source && (
            <span className={`inline-block mt-1 text-[10px] px-1.5 py-0.5 rounded border ${sourceColors[job.source] || sourceColors.mock}`}>
              {job.source === "remoteok" ? "RemoteOK" : job.source === "adzuna" ? "Adzuna" : "Demo"}
            </span>
          )}
        </div>
      </div>

      {/* Skills */}
      <div className="flex flex-wrap gap-1 mt-3">
        {job.required_skills?.slice(0, 4).map((skill, i) => (
          <span key={i} className="text-xs bg-white/5 px-2 py-0.5 rounded">
            {skill}
          </span>
        ))}
        {job.category && (
          <span className="text-xs bg-indigo-500/10 text-indigo-300 px-2 py-0.5 rounded">
            {job.category}
          </span>
        )}
      </div>

      {/* Description preview */}
      {job.description && (
        <p className="text-xs text-muted-foreground mt-2 line-clamp-2">
          {job.description}
        </p>
      )}

      {/* Actions */}
      <div className="flex items-center justify-between mt-4 pt-3 border-t border-white/10">
        <span className="text-xs text-muted-foreground">
          Posted {job.posted_date}
        </span>
        <div className="flex gap-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => window.open(job.job_url, "_blank")}
            data-testid={`view-job-${job.id}`}
          >
            <ExternalLink className="w-3 h-3 mr-1" /> View
          </Button>
          <Button
            size="sm"
            className={applied ? "bg-emerald-500/20 text-emerald-300" : "btn-primary"}
            onClick={() => onOpenApplyModal(job)}
            disabled={applied}
            data-testid={`apply-job-${job.id}`}
          >
            {applied ? (
              <>
                <CheckCircle2 className="w-3 h-3 mr-1" /> Applied
              </>
            ) : (
              <>
                <Sparkles className="w-3 h-3 mr-1" /> Prepare & Apply
              </>
            )}
          </Button>
        </div>
      </div>
    </motion.div>
  );
};

// Application Card Component with Status Update
const ApplicationCard = ({ application, onUpdateStatus }) => {
  const [showStatusMenu, setShowStatusMenu] = useState(false);
  
  const statuses = [
    { value: "applied", label: "Applied", color: "text-blue-400" },
    { value: "viewed", label: "Viewed by Recruiter", color: "text-amber-400" },
    { value: "interview_scheduled", label: "Interview Scheduled", color: "text-emerald-400" },
    { value: "offer", label: "Got Offer!", color: "text-green-400" },
    { value: "rejected", label: "Rejected", color: "text-red-400" }
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="glass rounded-xl p-4"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-indigo-500/20 flex items-center justify-center">
            <Briefcase className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <h4 className="font-medium">{application.job_title}</h4>
            <div className="text-sm text-muted-foreground">{application.company}</div>
          </div>
        </div>
        
        <div className="relative">
          <button 
            onClick={() => setShowStatusMenu(!showStatusMenu)}
            className="hover:opacity-80 transition-opacity"
          >
            <StatusBadge status={application.status} />
          </button>
          
          {showStatusMenu && (
            <div className="absolute right-0 top-full mt-1 bg-gray-900 border border-white/10 rounded-lg shadow-xl z-10 py-1 min-w-[160px]">
              {statuses.map((s) => (
                <button
                  key={s.value}
                  onClick={() => {
                    onUpdateStatus(application.id, s.value);
                    setShowStatusMenu(false);
                  }}
                  className={`w-full text-left px-3 py-2 text-sm hover:bg-white/10 ${s.color}`}
                >
                  {s.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-muted-foreground">
        <span>Applied {new Date(application.applied_at).toLocaleDateString()}</span>
        <div className="flex items-center gap-2">
          {application.job_url && (
            <button 
              onClick={() => window.open(application.job_url, "_blank")}
              className="text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
            >
              <ExternalLink className="w-3 h-3" /> View Job
            </button>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default function SmartJobsPage() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [searching, setSearching] = useState(false);
  
  // Dashboard state
  const [dashboard, setDashboard] = useState(null);
  const [matchingJobs, setMatchingJobs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [appliedJobIds, setAppliedJobIds] = useState(new Set());
  
  // Search state
  const [searchQuery, setSearchQuery] = useState("");
  const [searchLocation, setSearchLocation] = useState("us");
  const [remoteOnly, setRemoteOnly] = useState(false);
  const [jobSources, setJobSources] = useState([]);
  const [isMockData, setIsMockData] = useState(true);
  
  // Notification state
  const [notifications, setNotifications] = useState([]);
  const [notificationPrefs, setNotificationPrefs] = useState({
    email_interview_alerts: true,
    email_status_updates: true,
    email_weekly_summary: true  // Enable by default
  });
  
  // Preferences state
  const [preferences, setPreferences] = useState({
    target_roles: [],
    locations: [],
    remote_preference: "remote",
    min_salary: null,
    max_salary: null,
    company_types: [],
    tech_stack: [],
    experience_years: null,
    auto_apply_enabled: false
  });
  
  // View state
  const [activeTab, setActiveTab] = useState("jobs"); // jobs, applications, notifications, settings
  
  // Apply Modal state
  const [selectedJob, setSelectedJob] = useState(null);
  const [showApplyModal, setShowApplyModal] = useState(false);

  useEffect(() => {
    fetchDashboard();
    fetchApplications();
    fetchNotifications();
    fetchNotificationPrefs();
  }, []);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/auto-apply/dashboard`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      setDashboard(response.data);
      setPreferences(response.data.preferences || preferences);
      setMatchingJobs(response.data.matching_jobs || []);
      setIsMockData(response.data.is_mock !== false);
      // Extract sources from jobs
      const sources = [...new Set(response.data.matching_jobs?.map(j => j.source).filter(Boolean) || [])];
      if (sources.length > 0) setJobSources(sources);
    } catch (error) {
      console.error("Failed to fetch dashboard:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchApplications = async () => {
    try {
      const response = await axios.get(`${API}/auto-apply/applications`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      setApplications(response.data.applications || []);
      setAppliedJobIds(new Set(response.data.applications?.map(a => a.job_id) || []));
    } catch (error) {
      console.error("Failed to fetch applications:", error);
    }
  };

  const fetchNotifications = async () => {
    try {
      const response = await axios.get(`${API}/notifications/history`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      setNotifications(response.data.notifications || []);
    } catch (error) {
      console.error("Failed to fetch notifications:", error);
    }
  };
  
  const updateApplicationStatus = async (applicationId, newStatus) => {
    try {
      await axios.patch(`${API}/auto-apply/applications/${applicationId}/status`, 
        { status: newStatus },
        { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }
      );
      toast.success(`Status updated to ${newStatus}`);
      fetchApplications();
    } catch (error) {
      toast.error("Failed to update status");
    }
  };
  
  const openApplyModal = (job) => {
    setSelectedJob(job);
    setShowApplyModal(true);
  };
  
  const closeApplyModal = () => {
    setShowApplyModal(false);
    setSelectedJob(null);
  };

  const fetchNotificationPrefs = async () => {
    try {
      const response = await axios.get(`${API}/notifications/preferences`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      setNotificationPrefs(response.data.preferences || notificationPrefs);
    } catch (error) {
      console.error("Failed to fetch notification preferences:", error);
    }
  };

  const saveNotificationPrefs = async (newPrefs) => {
    try {
      const updatedPrefs = { ...notificationPrefs, ...newPrefs };
      await axios.post(`${API}/auto-apply/notification-preferences`, updatedPrefs, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      setNotificationPrefs(updatedPrefs);
    } catch (error) {
      console.error("Failed to save notification prefs:", error);
    }
  };

  const sendTestNotification = async () => {
    try {
      const response = await axios.post(`${API}/notifications/test-interview`, {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      toast.success("Test notification sent! Check your email.");
      fetchNotifications();
    } catch (error) {
      if (error.response?.data?.detail?.includes("verify a domain")) {
        toast.info("Notification queued! Email will be sent once domain is verified.");
        fetchNotifications();
      } else {
        toast.error(error.response?.data?.detail || "Failed to send test notification");
      }
    }
  };

  const fetchMatchingJobs = async (searchKeywords = null) => {
    setSearching(true);
    try {
      const params = new URLSearchParams();
      if (searchKeywords) params.append("keywords", searchKeywords);
      if (searchLocation) params.append("location", searchLocation);
      if (remoteOnly) params.append("remote_only", "true");
      
      const url = searchKeywords 
        ? `${API}/auto-apply/search?${params.toString()}`
        : `${API}/auto-apply/matching-jobs?${params.toString()}`;
        
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      setMatchingJobs(response.data.jobs || []);
      setJobSources(response.data.sources || []);
      setIsMockData(response.data.is_mock || false);
    } catch (error) {
      console.error("Failed to fetch jobs:", error);
      toast.error("Failed to search jobs");
    } finally {
      setSearching(false);
    }
  };

  const savePreferences = async () => {
    setSaving(true);
    try {
      await axios.post(`${API}/auto-apply/preferences`, preferences, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      toast.success("Preferences saved!");
      fetchMatchingJobs();
    } catch (error) {
      toast.error("Failed to save preferences");
    } finally {
      setSaving(false);
    }
  };

  const applyToJob = async (job) => {
    const response = await axios.post(
      `${API}/auto-apply/apply/${job.id}`,
      { job_data: job },
      { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }
    );
    setAppliedJobIds(prev => new Set([...prev, job.id]));
    fetchApplications();
    return response.data;
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      fetchMatchingJobs(searchQuery.trim());
    }
  };

  const toggleRole = (role) => {
    setPreferences(prev => {
      const currentRoles = prev.target_roles || [];
      return {
        ...prev,
        target_roles: currentRoles.includes(role)
          ? currentRoles.filter(r => r !== role)
          : [...currentRoles, role]
      };
    });
  };

  const toggleLocation = (location) => {
    setPreferences(prev => {
      const currentLocations = prev.locations || [];
      return {
        ...prev,
        locations: currentLocations.includes(location)
          ? currentLocations.filter(l => l !== location)
          : [...currentLocations, location]
      };
    });
  };

  const toggleCompanyType = (type) => {
    setPreferences(prev => {
      const currentTypes = prev.company_types || [];
      return {
        ...prev,
        company_types: currentTypes.includes(type)
          ? currentTypes.filter(t => t !== type)
          : [...currentTypes, type]
      };
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <AppNavigation />
        <div className="flex items-center justify-center h-[60vh]">
          <Loader2 className="w-8 h-8 animate-spin text-indigo-400" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <AppNavigation />
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/30 mb-4">
                <Search className="w-4 h-4 text-purple-400" />
                <span className="text-sm text-purple-300">Smart Job Search</span>
                <span className="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full ml-2">
                  LIVE
                </span>
              </div>
              <h1 className="text-3xl font-bold">Find AI Jobs + Get Cover Letters</h1>
              <p className="text-muted-foreground">
                Search real AI/ML jobs from 6 sources. Generate tailored cover letters instantly.
              </p>
            </div>
            
            {/* Weekly Email Toggle */}
            <div className="glass rounded-xl p-4 text-center">
              <button
                onClick={async () => {
                  const newValue = !notificationPrefs.email_weekly_summary;
                  setNotificationPrefs(prev => ({
                    ...prev,
                    email_weekly_summary: newValue
                  }));
                  await saveNotificationPrefs({ email_weekly_summary: newValue });
                  toast.success(newValue ? "Weekly job digest enabled!" : "Weekly digest disabled");
                }}
                className="flex items-center gap-2"
                data-testid="weekly-digest-toggle"
              >
                {notificationPrefs.email_weekly_summary ? (
                  <BellRing className="w-10 h-10 text-emerald-400" />
                ) : (
                  <Bell className="w-10 h-10 text-muted-foreground" />
                )}
              </button>
              <div className="text-sm mt-2">
                {notificationPrefs.email_weekly_summary ? (
                  <span className="text-emerald-400">Weekly Digest ON</span>
                ) : (
                  <span className="text-muted-foreground">Weekly Digest OFF</span>
                )}
              </div>
            </div>
          </div>

          {/* Stats Banner */}
          <div className="grid grid-cols-4 gap-4">
            <div className="glass rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-indigo-400">
                {dashboard?.stats?.total_applications || 0}
              </div>
              <div className="text-xs text-muted-foreground">Total Applied</div>
            </div>
            <div className="glass rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-amber-400">
                {dashboard?.stats?.applications_this_week || 0}
              </div>
              <div className="text-xs text-muted-foreground">This Week</div>
            </div>
            <div className="glass rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-emerald-400">
                {matchingJobs.length}
              </div>
              <div className="text-xs text-muted-foreground">Matching Jobs</div>
            </div>
            <div className="glass rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-purple-400">
                {dashboard?.stats?.avg_match_score || 0}%
              </div>
              <div className="text-xs text-muted-foreground">Avg Match</div>
            </div>
          </div>

          {/* Data Source Notice */}
          {isMockData ? (
            <div className="mt-4 p-3 bg-amber-500/10 border border-amber-500/30 rounded-lg flex items-center gap-2 text-sm text-amber-300">
              <AlertCircle className="w-4 h-4" />
              <span>DEMO MODE: Using simulated job data. Search for jobs to see real listings!</span>
            </div>
          ) : (
            <div className="mt-4 p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center gap-2 text-sm text-emerald-300">
              <CheckCircle2 className="w-4 h-4" />
              <span>LIVE DATA: Showing real jobs from {jobSources.join(" & ")}. Click Apply Now to open the job and track your application!</span>
            </div>
          )}
        </motion.div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {[
            { id: "jobs", label: "Matching Jobs", icon: Search },
            { id: "applications", label: "My Applications", icon: Briefcase },
            { id: "notifications", label: "Notifications", icon: Bell, badge: notifications.length },
            { id: "settings", label: "Preferences", icon: Settings }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                  : "text-muted-foreground hover:bg-white/5"
              }`}
              data-testid={`tab-${tab.id}`}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
              {tab.badge > 0 && (
                <span className="ml-1 px-1.5 py-0.5 text-xs bg-rose-500 text-white rounded-full">
                  {tab.badge}
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          {activeTab === "jobs" && (
            <motion.div
              key="jobs"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-4"
            >
              {/* Search Bar */}
              <form onSubmit={handleSearch} className="glass rounded-xl p-4">
                <div className="flex flex-wrap gap-3">
                  <div className="flex-1 min-w-[200px]">
                    <Input
                      placeholder="Search jobs (e.g., AI Engineer, Data Scientist)"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="bg-black/20 border-white/10"
                      data-testid="job-search-input"
                    />
                  </div>
                  <select
                    value={searchLocation}
                    onChange={(e) => setSearchLocation(e.target.value)}
                    className="bg-black/20 border border-white/10 rounded-md px-3 py-2 text-sm"
                    data-testid="location-select"
                  >
                    <option value="us">🇺🇸 United States</option>
                    <option value="uk">🇬🇧 United Kingdom</option>
                    <option value="canada">🇨🇦 Canada</option>
                    <option value="germany">🇩🇪 Germany</option>
                    <option value="india">🇮🇳 India</option>
                    <option value="australia">🇦🇺 Australia</option>
                    <option value="remote">🌍 Remote Only</option>
                  </select>
                  <label className="flex items-center gap-2 text-sm">
                    <input
                      type="checkbox"
                      checked={remoteOnly}
                      onChange={(e) => setRemoteOnly(e.target.checked)}
                      className="rounded"
                    />
                    Remote Only
                  </label>
                  <Button type="submit" disabled={searching} data-testid="search-jobs-btn">
                    {searching ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <>
                        <Search className="w-4 h-4 mr-1" /> Search
                      </>
                    )}
                  </Button>
                </div>
              </form>

              {/* Results Header */}
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold">{matchingJobs.length} Jobs Found</h2>
                  <div className="flex items-center gap-2 mt-1">
                    {jobSources.map(source => (
                      <span key={source} className={`text-xs px-2 py-0.5 rounded ${
                        source === "adzuna" ? "bg-blue-500/20 text-blue-300" :
                        source === "remoteok" ? "bg-green-500/20 text-green-300" :
                        "bg-amber-500/20 text-amber-300"
                      }`}>
                        {source === "remoteok" ? "RemoteOK" : source === "adzuna" ? "Adzuna" : source}
                      </span>
                    ))}
                    {isMockData && (
                      <span className="text-xs text-amber-400">(Demo Data)</span>
                    )}
                  </div>
                </div>
                <Button variant="outline" size="sm" onClick={() => fetchMatchingJobs(searchQuery || null)} disabled={searching}>
                  <RefreshCw className={`w-4 h-4 mr-1 ${searching ? "animate-spin" : ""}`} /> Refresh
                </Button>
              </div>
              
              {/* Job Cards */}
              <div className="grid md:grid-cols-2 gap-4">
                {matchingJobs.map((job) => (
                  <JobCard
                    key={job.id}
                    job={job}
                    onApply={applyToJob}
                    applied={appliedJobIds.has(job.id)}
                    onOpenApplyModal={openApplyModal}
                  />
                ))}
              </div>

              {matchingJobs.length === 0 && !searching && (
                <div className="glass rounded-xl p-8 text-center">
                  <Search className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-muted-foreground">No jobs found</p>
                  <p className="text-sm text-muted-foreground mt-1">Try different keywords or adjust your filters</p>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === "applications" && (
            <motion.div
              key="applications"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-4"
            >
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold">Your Applications ({applications.length})</h2>
                <p className="text-sm text-muted-foreground">Click status badge to update</p>
              </div>
              
              {applications.length === 0 ? (
                <div className="glass rounded-xl p-8 text-center">
                  <Briefcase className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                  <p className="text-muted-foreground">No applications yet</p>
                  <p className="text-sm text-muted-foreground">Start applying to jobs to track them here</p>
                </div>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {applications.map((app) => (
                    <ApplicationCard 
                      key={app.id} 
                      application={app} 
                      onUpdateStatus={updateApplicationStatus}
                    />
                  ))}
                </div>
              )}
            </motion.div>
          )}

          {activeTab === "notifications" && (
            <motion.div
              key="notifications"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Notification Preferences */}
              <div className="glass rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <BellRing className="w-5 h-5 text-rose-400" />
                  Email Notification Settings
                </h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
                    <div>
                      <div className="font-medium">Interview Alerts</div>
                      <div className="text-sm text-muted-foreground">Get notified when you receive interview requests</div>
                    </div>
                    <Switch
                      checked={notificationPrefs.email_interview_alerts}
                      onCheckedChange={(checked) => saveNotificationPrefs({
                        ...notificationPrefs,
                        email_interview_alerts: checked
                      })}
                      data-testid="switch-interview-alerts"
                    />
                  </div>
                  <div className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
                    <div>
                      <div className="font-medium">Status Updates</div>
                      <div className="text-sm text-muted-foreground">Get notified when your application status changes</div>
                    </div>
                    <Switch
                      checked={notificationPrefs.email_status_updates}
                      onCheckedChange={(checked) => saveNotificationPrefs({
                        ...notificationPrefs,
                        email_status_updates: checked
                      })}
                      data-testid="switch-status-updates"
                    />
                  </div>
                  <div className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
                    <div>
                      <div className="font-medium">Weekly Summary</div>
                      <div className="text-sm text-muted-foreground">Get a weekly summary of your job search progress</div>
                    </div>
                    <Switch
                      checked={notificationPrefs.email_weekly_summary}
                      onCheckedChange={(checked) => saveNotificationPrefs({
                        ...notificationPrefs,
                        email_weekly_summary: checked
                      })}
                      data-testid="switch-weekly-summary"
                    />
                  </div>
                </div>
                
                {/* Test Notification Button */}
                <div className="mt-6 pt-4 border-t border-white/10">
                  <Button
                    variant="outline"
                    onClick={sendTestNotification}
                    className="w-full"
                    data-testid="send-test-notification-btn"
                  >
                    <Mail className="w-4 h-4 mr-2" />
                    Send Test Interview Notification
                  </Button>
                  <p className="text-xs text-muted-foreground mt-2 text-center">
                    Sends a sample interview notification email to test your settings
                  </p>
                </div>
              </div>

              {/* Notification History */}
              <div className="glass rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold flex items-center gap-2">
                    <Bell className="w-5 h-5 text-indigo-400" />
                    Notification History
                  </h3>
                  <Button variant="outline" size="sm" onClick={fetchNotifications}>
                    <RefreshCw className="w-4 h-4 mr-1" /> Refresh
                  </Button>
                </div>
                
                {notifications.length === 0 ? (
                  <div className="text-center py-8">
                    <Bell className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                    <p className="text-muted-foreground">No notifications yet</p>
                    <p className="text-sm text-muted-foreground">Interview notifications will appear here</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {notifications.map((notif, index) => (
                      <div key={notif.id || index} className="p-4 bg-black/20 rounded-lg">
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex items-start gap-3">
                            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                              notif.type === "interview_scheduled" 
                                ? "bg-emerald-500/20 text-emerald-400" 
                                : "bg-indigo-500/20 text-indigo-400"
                            }`}>
                              {notif.type === "interview_scheduled" ? "🎉" : "📬"}
                            </div>
                            <div>
                              <div className="font-medium">
                                {notif.type === "interview_scheduled" ? "Interview Request" : "Status Update"}
                              </div>
                              <div className="text-sm text-muted-foreground">
                                {notif.job_title} at {notif.company}
                              </div>
                              <div className="text-xs text-muted-foreground mt-1">
                                {new Date(notif.sent_at).toLocaleString()}
                              </div>
                            </div>
                          </div>
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            notif.status === "sent" 
                              ? "bg-emerald-500/20 text-emerald-300" 
                              : "bg-amber-500/20 text-amber-300"
                          }`}>
                            {notif.status === "sent" ? "Sent" : "Pending"}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {activeTab === "settings" && (
            <motion.div
              key="settings"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Target Roles */}
              <div className="glass rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <Briefcase className="w-5 h-5 text-indigo-400" />
                  Target Roles
                </h3>
                <div className="flex flex-wrap gap-2">
                  {ROLE_OPTIONS.map((role) => (
                    <button
                      key={role}
                      onClick={() => toggleRole(role)}
                      className={`px-3 py-1.5 rounded-lg text-sm transition-all ${
                        (preferences.target_roles || []).includes(role)
                          ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/50"
                          : "bg-white/5 text-muted-foreground hover:bg-white/10"
                      }`}
                      data-testid={`role-${role.replace(/\s+/g, '-').toLowerCase()}`}
                    >
                      {role}
                    </button>
                  ))}
                </div>
              </div>

              {/* Locations */}
              <div className="glass rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <MapPin className="w-5 h-5 text-emerald-400" />
                  Preferred Locations
                </h3>
                <div className="flex flex-wrap gap-2">
                  {LOCATION_OPTIONS.map((location) => (
                    <button
                      key={location}
                      onClick={() => toggleLocation(location)}
                      className={`px-3 py-1.5 rounded-lg text-sm transition-all ${
                        (preferences.locations || []).includes(location)
                          ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/50"
                          : "bg-white/5 text-muted-foreground hover:bg-white/10"
                      }`}
                    >
                      {location}
                    </button>
                  ))}
                </div>
              </div>

              {/* Company Types */}
              <div className="glass rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <Building2 className="w-5 h-5 text-amber-400" />
                  Company Types
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {COMPANY_TYPE_OPTIONS.map((type) => (
                    <button
                      key={type.id}
                      onClick={() => toggleCompanyType(type.id)}
                      className={`p-3 rounded-lg text-left transition-all ${
                        (preferences.company_types || []).includes(type.id)
                          ? "bg-amber-500/20 border border-amber-500/50"
                          : "bg-white/5 hover:bg-white/10"
                      }`}
                    >
                      <div className="font-medium text-sm">{type.name}</div>
                      <div className="text-xs text-muted-foreground">{type.description}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Salary Range */}
              <div className="glass rounded-xl p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <DollarSign className="w-5 h-5 text-emerald-400" />
                  Salary Range (USD)
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Minimum</Label>
                    <Input
                      type="number"
                      value={preferences.min_salary || ""}
                      onChange={(e) => setPreferences(prev => ({
                        ...prev,
                        min_salary: e.target.value ? parseInt(e.target.value) : null
                      }))}
                      placeholder="e.g., 150000"
                      className="bg-black/20"
                      data-testid="min-salary-input"
                    />
                  </div>
                  <div>
                    <Label>Maximum</Label>
                    <Input
                      type="number"
                      value={preferences.max_salary || ""}
                      onChange={(e) => setPreferences(prev => ({
                        ...prev,
                        max_salary: e.target.value ? parseInt(e.target.value) : null
                      }))}
                      placeholder="e.g., 300000"
                      className="bg-black/20"
                      data-testid="max-salary-input"
                    />
                  </div>
                </div>
              </div>

              {/* Save Button */}
              <Button
                onClick={savePreferences}
                disabled={saving}
                className="w-full btn-primary h-12"
                data-testid="save-preferences-btn"
              >
                {saving ? (
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                ) : (
                  <CheckCircle2 className="w-5 h-5 mr-2" />
                )}
                Save Preferences
              </Button>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
      
      {/* Apply Preparation Modal */}
      <ApplyModal
        job={selectedJob}
        isOpen={showApplyModal}
        onClose={closeApplyModal}
        onApplyComplete={applyToJob}
      />
    </div>
  );
}
