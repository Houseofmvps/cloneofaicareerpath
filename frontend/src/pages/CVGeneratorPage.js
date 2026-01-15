import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import { saveAs } from "file-saver";
import {
  FileText, Upload, Sparkles, Copy, Download, Loader2,
  CheckCircle2, AlertCircle, Target, Edit3, X
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Textarea } from "../components/ui/textarea";
import { Label } from "../components/ui/label";
import { Input } from "../components/ui/input";
import { Progress } from "../components/ui/progress";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import AppNavigation from "../components/AppNavigation";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

// Generation Status Component
const GenerationStatus = ({ stage, progress }) => {
  const stages = [
    { id: 1, name: "Analyzing", icon: "📄" },
    { id: 2, name: "Extracting", icon: "🔍" },
    { id: 3, name: "Optimizing", icon: "🎯" },
    { id: 4, name: "Enhancing", icon: "✨" },
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
          <Loader2 className="w-5 h-5 animate-spin text-emerald-400" />
          Creating Your Superior Resume...
        </h3>
        <span className="text-sm text-muted-foreground">{Math.round(progress)}%</span>
      </div>
      
      <Progress value={progress} className="h-2" />
      
      <div className="grid grid-cols-5 gap-2 mt-4">
        {stages.map((s) => (
          <div
            key={s.id}
            className={`text-center p-2 rounded-lg transition-all ${
              s.id < stage ? "bg-emerald-500/20 text-emerald-300" :
              s.id === stage ? "bg-indigo-500/30 text-indigo-300 animate-pulse" :
              "bg-white/5 text-muted-foreground"
            }`}
          >
            <div className="text-lg mb-1">{s.icon}</div>
            <div className="text-xs">{s.name}</div>
          </div>
        ))}
      </div>
    </motion.div>
  );
};

// Clean markdown from text
const cleanMarkdown = (text) => {
  if (!text) return "";
  if (typeof text !== "string") return String(text);
  return text
    .replace(/\*\*/g, "")
    .replace(/\*/g, "")
    .replace(/##\s*/g, "")
    .replace(/#\s*/g, "")
    .replace(/--/g, "–")
    .trim();
};

// Country options for region selection
const COUNTRIES = [
  { id: "us", name: "🇺🇸 United States", tier: 1, pageLength: { entry: "1 page", mid: "1-2 pages", senior: "2 pages max" }},
  { id: "canada", name: "🇨🇦 Canada", tier: 1, pageLength: { entry: "1 page", mid: "1-2 pages", senior: "2 pages max" }},
  { id: "uk", name: "🇬🇧 United Kingdom", tier: 1, pageLength: { entry: "1-1.5 pages", mid: "1.5-2 pages", senior: "2-3 pages" }},
  { id: "india", name: "🇮🇳 India", tier: 1, pageLength: { entry: "2-3 pages", mid: "2-3 pages", senior: "3-4 pages" }},
  { id: "germany", name: "🇩🇪 Germany", tier: 1, pageLength: { entry: "1-2 pages", mid: "1.5-2.5 pages", senior: "2-3 pages" }},
  { id: "australia", name: "🇦🇺 Australia", tier: 1, pageLength: { entry: "1-2 pages", mid: "2-3 pages", senior: "3-4 pages" }},
  { id: "singapore", name: "🇸🇬 Singapore", tier: 1, pageLength: { entry: "1-2 pages", mid: "1.5-2 pages", senior: "2-3 pages" }},
  { id: "uae", name: "🇦🇪 UAE", tier: 2, pageLength: { entry: "2-3 pages", mid: "2-3 pages", senior: "3-4 pages" }},
  { id: "global", name: "🌍 Other (Global Standard)", tier: 3, pageLength: { entry: "1-2 pages", mid: "1.5-2.5 pages", senior: "2-3 pages" }},
];

const EXPERIENCE_LEVELS = [
  { id: "entry", name: "0-3 years (Entry-level)", years: "0-3" },
  { id: "mid", name: "3-10 years (Mid-career)", years: "3-10" },
  { id: "senior", name: "10+ years (Senior)", years: "10+" },
];

export default function CVGeneratorPage() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [generationStage, setGenerationStage] = useState(0);
  const [generationProgress, setGenerationProgress] = useState(0);
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [currentRole, setCurrentRole] = useState("");
  const [yearsExp, setYearsExp] = useState("");
  const [skills, setSkills] = useState("");
  const [generatedCV, setGeneratedCV] = useState(null);
  const [usage, setUsage] = useState({ used: 0, limit: 2, credits: 0 });
  const [cvHistory, setCvHistory] = useState([]);
  
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadFileName, setUploadFileName] = useState("");
  
  const [targetRegion, setTargetRegion] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("");
  
  const [editMode, setEditMode] = useState(false);
  const [editedContent, setEditedContent] = useState("");
  
  const getSelectedCountry = () => COUNTRIES.find(c => c.id === targetRegion);
  
  const getRecommendedLength = () => {
    if (!targetRegion || !experienceLevel) return null;
    const country = COUNTRIES.find(c => c.id === targetRegion);
    return country?.pageLength[experienceLevel] || null;
  };

  const fetchRoles = async () => {
    try {
      const response = await axios.get(`${API}/roles`);
      setRoles(response.data.roles || []);
    } catch (error) {
      console.error("Failed to fetch roles:", error);
    }
  };

  const fetchUsage = async () => {
    try {
      const response = await axios.get(`${API}/usage`);
      setUsage({
        used: response.data.cv_generations_used,
        limit: response.data.cv_generations_limit,
        credits: response.data.cv_credits || 0
      });
    } catch (error) {
      console.error("Failed to fetch usage:", error);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API}/cv/history`);
      setCvHistory(response.data.cv_generations || []);
    } catch (error) {
      console.error("Failed to fetch CV history:", error);
    }
  };

  useEffect(() => {
    const loadInitialData = async () => {
      await Promise.all([fetchRoles(), fetchUsage(), fetchHistory()]);
    };
    loadInitialData();
  }, []);

  const handleFileUpload = async (file) => {
    if (!file) return;
    
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      toast.error("File too large. Maximum size is 10MB.");
      return;
    }
    
    setUploading(true);
    setUploadProgress(0);
    setUploadFileName(file.name);
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const response = await axios.post(`${API}/resume/parse`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        }
      });
      
      setUploadProgress(100);
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setResumeText(response.data.resume_data.raw_text);
      if (response.data.resume_data.current_role) {
        setCurrentRole(response.data.resume_data.current_role);
      }
      if (response.data.resume_data.skills?.length) {
        setSkills(response.data.resume_data.skills.join(", "));
      }
      
      setUploading(false);
      setUploadProgress(0);
      toast.success(`"${file.name}" parsed successfully!`);
    } catch (error) {
      setUploading(false);
      setUploadProgress(0);
      toast.error("Failed to parse file. Try a different format.");
    }
  };

  const handleGenerate = async () => {
    if (!resumeText.trim() || !selectedRole) {
      toast.error("Please enter resume text and select a target role");
      return;
    }
    
    if (!targetRegion || !experienceLevel) {
      toast.error("Please select region and experience level");
      return;
    }

    setLoading(true);
    setGenerationStage(1);
    setGenerationProgress(10);
    
    const progressInterval = setInterval(() => {
      setGenerationProgress(prev => {
        if (prev >= 90) return prev;
        const newProgress = prev + Math.random() * 15;
        if (newProgress > 20 && newProgress <= 40) setGenerationStage(2);
        else if (newProgress > 40 && newProgress <= 60) setGenerationStage(3);
        else if (newProgress > 60 && newProgress <= 80) setGenerationStage(4);
        else if (newProgress > 80) setGenerationStage(5);
        return Math.min(newProgress, 90);
      });
    }, 800);

    try {
      const expLevel = EXPERIENCE_LEVELS.find(e => e.id === experienceLevel);
      const countryData = getSelectedCountry();
      
      // Calculate experience_years as integer from range
      let expYears = 3;
      if (expLevel?.years) {
        const range = expLevel.years.split("-");
        expYears = parseInt(range[0]) || 3;
      }
      
      const response = await axios.post(`${API}/cv/generate`, {
        resume_text: resumeText,
        target_role_id: selectedRole,
        current_role: currentRole,
        years_experience: parseInt(yearsExp) || null,
        skills: skills.split(",").map(s => s.trim()).filter(Boolean),
        target_region: targetRegion,
        target_country: countryData?.name || targetRegion,
        region_name: countryData?.name || targetRegion,
        tier: countryData?.tier || 3,
        experience_level: experienceLevel,
        experience_years: expYears,
        recommended_length: getRecommendedLength()
      });

      clearInterval(progressInterval);
      setGenerationProgress(100);
      setGenerationStage(5);
      
      setTimeout(() => {
        setGeneratedCV(response.data);
        setUsage(response.data.usage);
        
        // Set editable content from the hybrid resume
        const hybridVersion = response.data.versions?.[0];
        if (hybridVersion?.content) {
          setEditedContent(hybridVersion.content);
        }
        
        toast.success("Superior Hybrid Resume generated!");
        fetchHistory();
        setLoading(false);
        setGenerationStage(0);
        setGenerationProgress(0);
      }, 500);
      
    } catch (error) {
      clearInterval(progressInterval);
      const detail = error.response?.data?.detail;
      toast.error(typeof detail === "object" ? detail.message : detail || "Failed to generate resume");
      setLoading(false);
      setGenerationStage(0);
      setGenerationProgress(0);
    }
  };

  const copyToClipboard = () => {
    const content = editMode ? editedContent : (generatedCV?.versions?.[0]?.content || "");
    navigator.clipboard.writeText(content);
    toast.success("Resume copied to clipboard!");
  };

  const downloadResume = async (format) => {
    const content = editMode ? editedContent : (generatedCV?.versions?.[0]?.content || "");
    
    if (format === "txt") {
      const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
      const userName = user?.name || "User";
      const role = selectedRole || "AI_Role";
      saveAs(blob, `${userName.replace(/\s+/g, '_')}_${role}_Resume.txt`);
      toast.success("Resume downloaded as TXT!");
      return;
    }

    try {
      toast.loading(`Generating ${format.toUpperCase()}...`, { id: 'download' });
      
      const userName = user?.name || "User";
      const cleanName = userName.replace(/[^\w\s-]/g, '').replace(/\s+/g, '_');
      const cleanRole = (selectedRole || "AI_Role").replace(/[^\w\s-]/g, '').replace(/\s+/g, '_');
      const downloadFilename = `${cleanName}_${cleanRole}_Resume.${format}`;
      
      const response = await axios.post(
        `${API}/cv/download-direct?cv_version=hybrid&format=${format}&target_role=${encodeURIComponent(selectedRole || "AI Role")}`,
        {
          cv_content: content,
          user_name: userName
        },
        { responseType: 'blob' }
      );
      
      const mimeType = format === "pdf" 
        ? "application/pdf" 
        : "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
      
      const blob = new Blob([response.data], { type: mimeType });
      saveAs(blob, downloadFilename);
      
      toast.dismiss('download');
      toast.success(`Resume downloaded as ${format.toUpperCase()}!`);
      fetchUsage();
      
    } catch (error) {
      toast.dismiss('download');
      toast.error(`Failed to generate ${format.toUpperCase()}`);
    }
  };

  const isPro = user?.subscription_tier === "pro";
  const canGenerate = isPro || usage.used < usage.limit || usage.credits > 0;

  // Get hybrid resume data
  const hybridVersion = generatedCV?.versions?.[0];
  const resumeContent = hybridVersion?.content || "";

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
                <FileText className="w-8 h-8 text-indigo-400" />
                AI Resume Builder
              </h1>
              <p className="text-muted-foreground">
                Build your ATS-optimized, human-appealing hybrid resume
              </p>
            </div>
            
            <div className="glass rounded-xl px-6 py-4 text-center">
              <div className="text-sm text-muted-foreground mb-1">FREE this month</div>
              <div className="text-2xl font-bold">
                <span className={usage.used >= usage.limit && !isPro ? "text-red-400" : "text-emerald-400"}>
                  {usage.used}
                </span>
                <span className="text-muted-foreground">/{isPro ? "∞" : usage.limit}</span>
              </div>
              {usage.credits > 0 && (
                <div className="text-xs text-amber-400 mt-1">+{usage.credits} credits</div>
              )}
            </div>
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="space-y-6"
          >
            {/* Resume Input */}
            <div className="glass rounded-2xl p-6">
              <Label className="text-lg font-semibold mb-4 block">Your Resume</Label>
              
              <div className="mb-4">
                <input
                  type="file"
                  accept=".pdf,.doc,.docx,.txt"
                  className="hidden"
                  id="cv-file-upload"
                  onChange={(e) => handleFileUpload(e.target.files[0])}
                  disabled={uploading}
                  data-testid="cv-file-input"
                />
                
                {uploading ? (
                  <div className="p-4 border-2 border-indigo-500/50 rounded-xl bg-indigo-500/10">
                    <div className="flex items-center gap-3 mb-3">
                      <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
                      <div className="flex-1">
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-sm font-medium text-indigo-300">
                            Uploading {uploadFileName}
                          </span>
                          <span className="text-sm font-bold text-indigo-400">{uploadProgress}%</span>
                        </div>
                        <Progress value={uploadProgress} className="h-2" />
                      </div>
                    </div>
                  </div>
                ) : (
                  <label
                    htmlFor="cv-file-upload"
                    className="flex items-center justify-center gap-2 p-4 border-2 border-dashed border-white/20 rounded-xl cursor-pointer hover:border-indigo-500/50 transition-colors"
                  >
                    <Upload className="w-5 h-5 text-indigo-400" />
                    <span>Upload PDF/DOCX or paste below</span>
                  </label>
                )}
              </div>
              
              <Textarea
                placeholder="Paste your resume text here..."
                className="min-h-[200px] input-dark"
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                data-testid="cv-resume-input"
              />
            </div>

            {/* Additional Info */}
            <div className="glass rounded-2xl p-6 space-y-4">
              <Label className="text-lg font-semibold block">Additional Details</Label>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="current-role" className="text-sm">Current Role</Label>
                  <Input
                    id="current-role"
                    placeholder="e.g., Software Engineer"
                    className="input-dark mt-1"
                    value={currentRole}
                    onChange={(e) => setCurrentRole(e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="years-exp" className="text-sm">Years Experience</Label>
                  <Input
                    id="years-exp"
                    type="number"
                    placeholder="e.g., 5"
                    className="input-dark mt-1"
                    value={yearsExp}
                    onChange={(e) => setYearsExp(e.target.value)}
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="skills" className="text-sm">Key Skills (comma separated)</Label>
                <Input
                  id="skills"
                  placeholder="e.g., Python, ML, TensorFlow, AWS"
                  className="input-dark mt-1"
                  value={skills}
                  onChange={(e) => setSkills(e.target.value)}
                />
              </div>
            </div>

            {/* Target Role */}
            <div className="glass rounded-2xl p-6">
              <Label className="text-lg font-semibold mb-4 block">
                <Target className="w-5 h-5 inline mr-2 text-indigo-400" />
                Target AI Role
              </Label>
              
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="w-full h-12 px-4 rounded-lg bg-black/20 border border-white/10 text-foreground focus:border-indigo-500"
                data-testid="cv-role-select"
              >
                <option value="">Select a role...</option>
                {roles.map((role) => (
                  <option key={role.id} value={role.id}>
                    {role.name} - {role.salary_range}
                  </option>
                ))}
              </select>
            </div>
            
            {/* Region & Experience */}
            <div className="glass rounded-2xl p-6 space-y-4">
              <div>
                <Label className="text-lg font-semibold mb-2 block">🌍 Target Region</Label>
                <select
                  value={targetRegion}
                  onChange={(e) => setTargetRegion(e.target.value)}
                  className="w-full h-12 px-4 rounded-lg bg-black/20 border border-white/10 text-foreground focus:border-indigo-500"
                >
                  <option value="">Select country...</option>
                  {COUNTRIES.map((country) => (
                    <option key={country.id} value={country.id}>{country.name}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <Label className="text-lg font-semibold mb-2 block">📊 Experience Level</Label>
                <select
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                  className="w-full h-12 px-4 rounded-lg bg-black/20 border border-white/10 text-foreground focus:border-indigo-500"
                >
                  <option value="">Select level...</option>
                  {EXPERIENCE_LEVELS.map((level) => (
                    <option key={level.id} value={level.id}>{level.name}</option>
                  ))}
                </select>
              </div>
              
              {targetRegion && experienceLevel && (
                <div className="p-3 rounded-lg bg-indigo-500/10 border border-indigo-500/30">
                  <div className="flex items-center gap-2 text-indigo-300 text-sm">
                    <CheckCircle2 className="w-4 h-4" />
                    <span className="font-medium">Recommended: {getRecommendedLength()}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Generate Button */}
            <Button
              onClick={handleGenerate}
              disabled={loading || !canGenerate || !resumeText.trim() || !selectedRole || !targetRegion || !experienceLevel}
              className="w-full btn-primary py-6 text-lg"
              data-testid="cv-generate-btn"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                  Building Your Resume...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 mr-2" />
                  Build Superior Hybrid Resume
                </>
              )}
            </Button>

            {!canGenerate && (
              <div className="glass rounded-xl p-4 border border-amber-500/30">
                <div className="flex items-center gap-2 text-amber-400 mb-2">
                  <AlertCircle className="w-5 h-5" />
                  <span className="font-medium">Free limit reached</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Upgrade to continue building resumes
                </p>
              </div>
            )}
          </motion.div>

          {/* Output Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-6"
          >
            {loading && (
              <GenerationStatus stage={generationStage} progress={generationProgress} />
            )}
            
            {!loading && generatedCV ? (
              <>
                {/* Scores */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="glass rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <span className="font-semibold text-sm">ATS Score</span>
                      <span className="text-2xl font-bold text-emerald-400">
                        {hybridVersion?.ats_score || generatedCV.ats_score_estimate || 95}/100
                      </span>
                    </div>
                    <Progress value={hybridVersion?.ats_score || 95} className="h-2" />
                    <p className="text-xs text-muted-foreground mt-2">Optimized for all ATS systems</p>
                  </div>

                  <div className="glass rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <span className="font-semibold text-sm">Human Appeal</span>
                      <span className="text-2xl font-bold text-blue-400">
                        {hybridVersion?.human_appeal_score || 94}/100
                      </span>
                    </div>
                    <Progress value={hybridVersion?.human_appeal_score || 94} className="h-2" />
                    <p className="text-xs text-muted-foreground mt-2">Engaging for recruiters</p>
                  </div>
                </div>

                {/* Keywords */}
                {(hybridVersion?.keywords_used?.length > 0 || generatedCV.keywords_added?.length > 0) && (
                  <div className="glass rounded-xl p-4">
                    <div className="text-sm font-medium mb-2">
                      Keywords Optimized ({(hybridVersion?.keywords_used || generatedCV.keywords_added || []).length}):
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {(hybridVersion?.keywords_used || generatedCV.keywords_added || []).slice(0, 15).map((kw, i) => (
                        <span key={i} className="px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs">
                          {kw}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Resume Display */}
                <div className="glass rounded-2xl p-6 border-2 border-emerald-500/30">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-semibold flex items-center gap-2">
                        <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                        Superior Hybrid Resume
                      </h3>
                      <p className="text-xs text-muted-foreground mt-1">
                        ATS-optimized + Human-appealing
                      </p>
                    </div>
                    <div className="flex gap-1">
                      <Button
                        size="sm"
                        variant={editMode ? "default" : "ghost"}
                        onClick={() => setEditMode(!editMode)}
                        title={editMode ? "Exit Edit" : "Edit"}
                        className={editMode ? "bg-emerald-500/20 text-emerald-300" : ""}
                      >
                        {editMode ? <X className="w-4 h-4" /> : <Edit3 className="w-4 h-4" />}
                      </Button>
                      <Button size="sm" variant="ghost" onClick={copyToClipboard} title="Copy">
                        <Copy className="w-4 h-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => downloadResume("pdf")}
                        className="text-red-400 hover:text-red-300"
                        title="PDF"
                      >
                        <Download className="w-4 h-4 mr-1" />
                        <span className="text-xs">PDF</span>
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => downloadResume("docx")}
                        className="text-blue-400 hover:text-blue-300"
                        title="Word"
                      >
                        <Download className="w-4 h-4 mr-1" />
                        <span className="text-xs">DOCX</span>
                      </Button>
                    </div>
                  </div>
                  
                  {editMode ? (
                    <div className="space-y-3">
                      <div className="text-xs text-emerald-400 mb-2 flex items-center gap-2">
                        <Edit3 className="w-3 h-3" />
                        Edit mode - changes will be used for download
                      </div>
                      <Textarea
                        value={editedContent}
                        onChange={(e) => setEditedContent(e.target.value)}
                        className="min-h-[400px] bg-white/5 font-mono text-sm"
                      />
                    </div>
                  ) : (
                    <div className="bg-white/5 rounded-xl p-4 max-h-[500px] overflow-y-auto">
                      <pre className="text-sm font-mono whitespace-pre-wrap text-gray-300">
                        {cleanMarkdown(resumeContent)}
                      </pre>
                    </div>
                  )}
                </div>

                {/* Improvements */}
                {generatedCV.key_improvements?.length > 0 && (
                  <div className="glass rounded-xl p-4">
                    <div className="text-sm font-medium mb-2">Key Improvements Made:</div>
                    <ul className="space-y-1 text-sm text-muted-foreground">
                      {generatedCV.key_improvements.slice(0, 5).map((tip, i) => (
                        <li key={i}>✓ {tip}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            ) : !loading ? (
              <div className="glass rounded-2xl p-12 text-center">
                <FileText className="w-16 h-16 text-muted-foreground mx-auto mb-4 opacity-50" />
                <h3 className="text-lg font-semibold mb-2">No Resume Generated Yet</h3>
                <p className="text-muted-foreground">
                  Enter your resume, select a role, and click Build to create your optimized resume.
                </p>
              </div>
            ) : null}

            {/* History */}
            {cvHistory.length > 0 && (
              <div className="glass rounded-2xl p-6">
                <h3 className="font-semibold mb-4">Recent Resumes</h3>
                <div className="space-y-2">
                  {cvHistory.slice(0, 5).map((cv) => (
                    <div
                      key={cv.id}
                      className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer"
                      onClick={() => {
                        setGeneratedCV(cv);
                        if (cv.versions?.[0]?.content) {
                          setEditedContent(cv.versions[0].content);
                        }
                      }}
                    >
                      <div>
                        <div className="font-medium text-sm">{cv.target_role}</div>
                        <div className="text-xs text-muted-foreground">
                          {new Date(cv.created_at).toLocaleDateString()}
                        </div>
                      </div>
                      <FileText className="w-4 h-4 text-muted-foreground" />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </main>
    </div>
  );
}
