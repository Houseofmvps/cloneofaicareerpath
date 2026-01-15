import { useState, useEffect, useCallback } from "react";
import { useNavigate, Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
import {
  Brain, Upload, FileText, ChevronLeft, ChevronRight, Loader2,
  Search, Briefcase, GraduationCap, Code, Clock, DollarSign,
  CheckCircle2, AlertCircle, Sparkles
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Textarea } from "../components/ui/textarea";
import { Progress } from "../components/ui/progress";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const STEPS = [
  { id: 1, title: "Upload Resume", icon: FileText },
  { id: 2, title: "Your Background", icon: Briefcase },
  { id: 3, title: "Target Role", icon: Brain },
  { id: 4, title: "Analysis", icon: Sparkles }
];

const LOCATIONS = [
  { id: "us", name: "United States", flag: "🇺🇸" },
  { id: "india", name: "India", flag: "🇮🇳" },
  { id: "europe", name: "Europe", flag: "🇪🇺" },
  { id: "brazil", name: "Brazil", flag: "🇧🇷" },
  { id: "se_asia", name: "Southeast Asia", flag: "🌏" }
];

// Analysis Generation Status Bar
const AnalysisStatus = ({ stage, progress }) => {
  const stages = [
    { id: 1, name: "Parsing Resume", icon: "📄" },
    { id: 2, name: "Analyzing Skills", icon: "🔍" },
    { id: 3, name: "Matching Role", icon: "🎯" },
    { id: 4, name: "Calculating Fit", icon: "📊" },
    { id: 5, name: "Generating Report", icon: "✅" }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass rounded-2xl p-8 max-w-2xl mx-auto space-y-6"
    >
      <div className="text-center mb-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 mb-4">
          <Loader2 className="w-8 h-8 animate-spin text-white" />
        </div>
        <h3 className="text-xl font-bold">Analyzing Your Career Fit...</h3>
        <p className="text-muted-foreground mt-1">Powered by Claude AI</p>
      </div>
      
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span>Progress</span>
          <span className="text-indigo-400">{Math.round(progress)}%</span>
        </div>
        <Progress value={progress} className="h-3" />
      </div>
      
      <div className="grid grid-cols-5 gap-2">
        {stages.map((s) => (
          <div
            key={s.id}
            className={`text-center p-3 rounded-xl transition-all ${
              s.id < stage ? "bg-emerald-500/20 text-emerald-300" :
              s.id === stage ? "bg-indigo-500/30 text-indigo-300 animate-pulse" :
              "bg-white/5 text-muted-foreground"
            }`}
          >
            <div className="text-2xl mb-1">{s.icon}</div>
            <div className="text-xs font-medium">{s.name}</div>
          </div>
        ))}
      </div>
      
      <p className="text-center text-sm text-muted-foreground">
        This takes about 30-60 seconds. We're analyzing your skills, career trajectory, and ATS compatibility...
      </p>
    </motion.div>
  );
};

export default function AnalyzerPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [analysisStage, setAnalysisStage] = useState(0);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [roles, setRoles] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedLocation, setSelectedLocation] = useState("us");
  
  // Form data
  const [resumeData, setResumeData] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [backgroundContext, setBackgroundContext] = useState({
    current_role: "",
    years_experience: 0,
    education_level: "",
    primary_skills: [],
    career_goals: "",
    location: "us"
  });
  const [selectedRole, setSelectedRole] = useState(null);
  const [skillInput, setSkillInput] = useState("");
  
  // Upload progress state
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadFileName, setUploadFileName] = useState("");

  useEffect(() => {
    fetchRoles();
  }, [selectedLocation]);

  const fetchRoles = async () => {
    try {
      const response = await axios.get(`${API}/roles?location=${selectedLocation}`);
      setRoles(response.data.roles || []);
    } catch (error) {
      console.error("Failed to fetch roles:", error);
    }
  };

  const handleFileUpload = async (file) => {
    if (!file) return;
    
    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      toast.error("File too large. Maximum size is 10MB.");
      return;
    }
    
    // Start upload with progress tracking
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
      
      // Show 100% briefly before completing
      setUploadProgress(100);
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setResumeData(response.data.resume_data);
      setResumeText(response.data.resume_data.raw_text);
      
      // Auto-fill background context from parsed resume
      if (response.data.resume_data.current_role) {
        setBackgroundContext(prev => ({
          ...prev,
          current_role: response.data.resume_data.current_role || prev.current_role
        }));
      }
      if (response.data.resume_data.years_experience) {
        setBackgroundContext(prev => ({
          ...prev,
          years_experience: response.data.resume_data.years_experience || prev.years_experience
        }));
      }
      if (response.data.resume_data.skills?.length) {
        setBackgroundContext(prev => ({
          ...prev,
          primary_skills: response.data.resume_data.skills.slice(0, 10)
        }));
      }
      
      setUploading(false);
      setUploadProgress(0);
      toast.success(`"${file.name}" parsed successfully!`);
    } catch (error) {
      setUploading(false);
      setUploadProgress(0);
      
      if (error.response?.status === 400) {
        toast.error("Unsupported file format. Please upload PDF, DOCX, or TXT files.");
      } else {
        toast.error("Failed to parse resume. Try a different format or paste your resume text directly.");
      }
    }
  };

  const handleTextSubmit = async () => {
    if (!resumeText.trim()) {
      toast.error("Please paste your resume text");
      return;
    }
    
    const formData = new FormData();
    formData.append("text", resumeText);
    
    setLoading(true);
    try {
      const response = await axios.post(`${API}/resume/parse`, formData);
      setResumeData(response.data.resume_data);
      
      // Auto-fill from parsed data
      if (response.data.resume_data.skills?.length) {
        setBackgroundContext(prev => ({
          ...prev,
          primary_skills: response.data.resume_data.skills.slice(0, 10)
        }));
      }
      
      toast.success("Resume parsed successfully!");
      setCurrentStep(2);
    } catch (error) {
      toast.error("Failed to parse resume. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileUpload(file);
    }
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
  }, []);

  const addSkill = () => {
    if (skillInput.trim() && !backgroundContext.primary_skills.includes(skillInput.trim())) {
      setBackgroundContext(prev => ({
        ...prev,
        primary_skills: [...prev.primary_skills, skillInput.trim()]
      }));
      setSkillInput("");
    }
  };

  const removeSkill = (skill) => {
    setBackgroundContext(prev => ({
      ...prev,
      primary_skills: prev.primary_skills.filter(s => s !== skill)
    }));
  };

  const handleAnalyze = async () => {
    if (!resumeData || !selectedRole) {
      toast.error("Please complete all steps");
      return;
    }
    
    setLoading(true);
    setCurrentStep(4);
    setAnalysisStage(1);
    setAnalysisProgress(10);
    
    // Simulate progress stages
    const progressInterval = setInterval(() => {
      setAnalysisProgress(prev => {
        if (prev >= 90) return prev;
        const newProgress = prev + Math.random() * 10;
        
        // Update stage based on progress
        if (newProgress > 20 && newProgress <= 40) setAnalysisStage(2);
        else if (newProgress > 40 && newProgress <= 60) setAnalysisStage(3);
        else if (newProgress > 60 && newProgress <= 80) setAnalysisStage(4);
        else if (newProgress > 80) setAnalysisStage(5);
        
        return Math.min(newProgress, 90);
      });
    }, 1200);
    
    try {
      const response = await axios.post(`${API}/analyze`, {
        resume_data: resumeData,
        target_role_id: selectedRole.id,
        background_context: backgroundContext
      });
      
      clearInterval(progressInterval);
      setAnalysisProgress(100);
      setAnalysisStage(5);
      
      setTimeout(() => {
        toast.success("Analysis complete!");
        navigate(`/results/${response.data.analysis_id}`);
      }, 500);
      
    } catch (error) {
      clearInterval(progressInterval);
      const message = error.response?.data?.detail || "Analysis failed. Please try again.";
      toast.error(message);
      setCurrentStep(3);
      setLoading(false);
      setAnalysisStage(0);
      setAnalysisProgress(0);
    }
  };

  const filteredRoles = roles.filter(role =>
    role.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    role.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const canProceed = () => {
    switch (currentStep) {
      case 1: return resumeData !== null;
      case 2: return backgroundContext.current_role && backgroundContext.years_experience > 0;
      case 3: return selectedRole !== null;
      default: return false;
    }
  };

  return (
    <div className="min-h-screen bg-background noise-bg">
      {/* Header */}
      <header className="glass-heavy border-b border-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">CareerLift</span>
            </Link>
            
            <Button variant="ghost" onClick={() => navigate("/dashboard")} data-testid="analyzer-back-btn">
              <ChevronLeft className="w-4 h-4 mr-1" />
              Back to Dashboard
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Progress Steps */}
        <div className="flex items-center justify-between mb-12">
          {STEPS.map((step, index) => (
            <div key={step.id} className="flex items-center">
              <div className="flex flex-col items-center">
                <div className={`
                  w-12 h-12 rounded-xl flex items-center justify-center transition-all
                  ${currentStep >= step.id 
                    ? 'bg-gradient-to-br from-indigo-500 to-purple-600 text-white' 
                    : 'bg-gray-800 text-muted-foreground'
                  }
                `}>
                  {currentStep > step.id ? (
                    <CheckCircle2 className="w-6 h-6" />
                  ) : (
                    <step.icon className="w-6 h-6" />
                  )}
                </div>
                <span className={`text-xs mt-2 ${currentStep >= step.id ? 'text-foreground' : 'text-muted-foreground'}`}>
                  {step.title}
                </span>
              </div>
              {index < STEPS.length - 1 && (
                <div className={`w-16 sm:w-24 h-0.5 mx-2 ${currentStep > step.id ? 'bg-indigo-500' : 'bg-gray-800'}`} />
              )}
            </div>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {/* Step 1: Resume Upload */}
          {currentStep === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold mb-2">Upload Your Resume</h1>
                <p className="text-muted-foreground">
                  Upload a PDF/DOCX file or paste your resume text
                </p>
              </div>

              {/* File Upload Zone */}
              {uploading ? (
                <div className="drop-zone border-indigo-500/50 bg-indigo-500/10">
                  <div className="w-full max-w-md mx-auto">
                    <div className="flex items-center gap-3 mb-4">
                      <Loader2 className="w-8 h-8 text-indigo-400 animate-spin" />
                      <div className="flex-1">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium text-indigo-300">
                            Uploading {uploadFileName}
                          </span>
                          <span className="text-lg font-bold text-indigo-400">{Math.round(uploadProgress)}%</span>
                        </div>
                        <Progress value={uploadProgress} className="h-3" />
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground text-center">
                      {uploadProgress < 100 ? "Uploading file..." : "Processing and parsing resume..."}
                    </p>
                  </div>
                </div>
              ) : (
                <div
                  className="drop-zone"
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                  data-testid="resume-dropzone"
                >
                  <input
                    type="file"
                    accept=".pdf,.doc,.docx,.txt"
                    className="hidden"
                    id="resume-upload"
                    onChange={(e) => handleFileUpload(e.target.files[0])}
                    data-testid="resume-file-input"
                  />
                  <label htmlFor="resume-upload" className="cursor-pointer">
                    <Upload className="w-12 h-12 text-indigo-400 mx-auto mb-4" />
                    <p className="text-lg font-medium mb-2">
                      Drop your resume here or click to upload
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Supports PDF, DOCX, TXT (max 10MB)
                    </p>
                  </label>
                </div>
              )}

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-white/10"></div>
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background px-2 text-muted-foreground">Or paste text</span>
                </div>
              </div>

              {/* Text Input */}
              <Textarea
                placeholder="Paste your resume text here..."
                className="min-h-[200px] input-dark"
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                data-testid="resume-text-input"
              />

              {resumeData && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="glass rounded-xl p-4"
                >
                  <div className="flex items-center gap-2 text-emerald-400 mb-3">
                    <CheckCircle2 className="w-5 h-5" />
                    <span className="font-medium">Resume Parsed Successfully</span>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    {resumeData.years_experience && (
                      <div>
                        <span className="text-muted-foreground">Experience:</span>
                        <span className="ml-2">{resumeData.years_experience} years</span>
                      </div>
                    )}
                    {resumeData.education && (
                      <div>
                        <span className="text-muted-foreground">Education:</span>
                        <span className="ml-2">{resumeData.education}</span>
                      </div>
                    )}
                    {resumeData.skills?.length > 0 && (
                      <div className="col-span-2">
                        <span className="text-muted-foreground">Skills detected:</span>
                        <span className="ml-2">{resumeData.skills.slice(0, 5).join(", ")}...</span>
                      </div>
                    )}
                  </div>
                </motion.div>
              )}

              <div className="flex justify-between pt-4">
                <Button variant="ghost" onClick={() => navigate("/dashboard")}>
                  Cancel
                </Button>
                <div className="flex gap-3">
                  {!resumeData && resumeText && (
                    <Button
                      onClick={handleTextSubmit}
                      disabled={loading}
                      className="btn-secondary"
                      data-testid="parse-text-btn"
                    >
                      {loading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
                      Parse Text
                    </Button>
                  )}
                  <Button
                    onClick={() => setCurrentStep(2)}
                    disabled={!canProceed() || loading}
                    className="btn-primary"
                    data-testid="step1-next-btn"
                  >
                    Next
                    <ChevronRight className="w-4 h-4 ml-1" />
                  </Button>
                </div>
              </div>
            </motion.div>
          )}

          {/* Step 2: Background Context */}
          {currentStep === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold mb-2">Tell Us About Yourself</h1>
                <p className="text-muted-foreground">
                  Help us personalize your career analysis
                </p>
              </div>

              <div className="glass rounded-2xl p-6 space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="current_role">Current Role *</Label>
                    <div className="relative">
                      <Briefcase className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                      <Input
                        id="current_role"
                        placeholder="e.g., Software Engineer"
                        className="pl-10 input-dark"
                        value={backgroundContext.current_role}
                        onChange={(e) => setBackgroundContext(prev => ({ ...prev, current_role: e.target.value }))}
                        data-testid="background-role-input"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="years_experience">Years of Experience *</Label>
                    <div className="relative">
                      <Clock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                      <Input
                        id="years_experience"
                        type="number"
                        min="0"
                        placeholder="e.g., 5"
                        className="pl-10 input-dark"
                        value={backgroundContext.years_experience || ""}
                        onChange={(e) => setBackgroundContext(prev => ({ ...prev, years_experience: parseInt(e.target.value) || 0 }))}
                        data-testid="background-experience-input"
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="education_level">Highest Education</Label>
                  <div className="relative">
                    <GraduationCap className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                    <Input
                      id="education_level"
                      placeholder="e.g., Bachelor's in Computer Science"
                      className="pl-10 input-dark"
                      value={backgroundContext.education_level}
                      onChange={(e) => setBackgroundContext(prev => ({ ...prev, education_level: e.target.value }))}
                      data-testid="background-education-input"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Primary Skills</Label>
                  <div className="flex gap-2">
                    <div className="relative flex-1">
                      <Code className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                      <Input
                        placeholder="Add a skill and press Enter"
                        className="pl-10 input-dark"
                        value={skillInput}
                        onChange={(e) => setSkillInput(e.target.value)}
                        onKeyPress={(e) => e.key === "Enter" && (e.preventDefault(), addSkill())}
                        data-testid="background-skill-input"
                      />
                    </div>
                    <Button onClick={addSkill} className="btn-secondary" data-testid="add-skill-btn">
                      Add
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {backgroundContext.primary_skills.map((skill, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-sm flex items-center gap-2"
                      >
                        {skill}
                        <button
                          onClick={() => removeSkill(skill)}
                          className="hover:text-red-400"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="career_goals">Career Goals (Optional)</Label>
                  <Textarea
                    id="career_goals"
                    placeholder="What do you hope to achieve in your AI career?"
                    className="input-dark"
                    value={backgroundContext.career_goals}
                    onChange={(e) => setBackgroundContext(prev => ({ ...prev, career_goals: e.target.value }))}
                    data-testid="background-goals-input"
                  />
                </div>

                {/* Location Selector */}
                <div className="space-y-2">
                  <Label>Your Location (for salary data)</Label>
                  <div className="grid grid-cols-5 gap-2">
                    {LOCATIONS.map((loc) => (
                      <button
                        key={loc.id}
                        type="button"
                        onClick={() => {
                          setSelectedLocation(loc.id);
                          setBackgroundContext(prev => ({ ...prev, location: loc.id }));
                        }}
                        className={`
                          p-3 rounded-xl text-center transition-all
                          ${selectedLocation === loc.id
                            ? 'bg-indigo-500/20 border-2 border-indigo-500 text-indigo-300'
                            : 'bg-white/5 border border-white/10 hover:border-indigo-500/50'
                          }
                        `}
                        data-testid={`location-${loc.id}`}
                      >
                        <div className="text-2xl mb-1">{loc.flag}</div>
                        <div className="text-xs">{loc.name}</div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex justify-between pt-4">
                <Button variant="ghost" onClick={() => setCurrentStep(1)} data-testid="step2-back-btn">
                  <ChevronLeft className="w-4 h-4 mr-1" />
                  Back
                </Button>
                <Button
                  onClick={() => setCurrentStep(3)}
                  disabled={!canProceed()}
                  className="btn-primary"
                  data-testid="step2-next-btn"
                >
                  Next
                  <ChevronRight className="w-4 h-4 ml-1" />
                </Button>
              </div>
            </motion.div>
          )}

          {/* Step 3: Role Selection */}
          {currentStep === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold mb-2">Select Your Target AI Role</h1>
                <p className="text-muted-foreground">
                  Choose the AI role you want to transition into
                </p>
              </div>

              {/* Search */}
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <Input
                  placeholder="Search AI roles..."
                  className="pl-12 h-14 input-dark text-lg"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  data-testid="role-search-input"
                />
              </div>

              {/* Role Grid */}
              <div className="grid md:grid-cols-2 gap-4 max-h-[500px] overflow-y-auto pr-2">
                {filteredRoles.map((role) => (
                  <motion.div
                    key={role.id}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className={`
                      glass rounded-xl p-5 cursor-pointer transition-all
                      ${selectedRole?.id === role.id 
                        ? 'border-2 border-indigo-500 glow-primary' 
                        : 'border border-white/10 hover:border-indigo-500/50'
                      }
                      ${role.fastest_path ? 'ring-2 ring-amber-500/50' : ''}
                    `}
                    onClick={() => setSelectedRole(role)}
                    data-testid={`role-card-${role.id}`}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="font-semibold text-lg">{role.name}</h3>
                        {role.fastest_path && (
                          <span className="text-xs px-2 py-0.5 bg-amber-500/20 text-amber-400 rounded-full">
                            Fastest Path to AI
                          </span>
                        )}
                      </div>
                      {selectedRole?.id === role.id && (
                        <CheckCircle2 className="w-5 h-5 text-indigo-400" />
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground mb-4">{role.description}</p>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 text-sm">
                        <DollarSign className="w-4 h-4 text-emerald-400" />
                        <span className="text-emerald-400">
                          {role.local_salary || role.salary_range}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-sm">
                        <Clock className="w-4 h-4 text-amber-400" />
                        <span className="text-amber-400">{role.transition_weeks} weeks to transition</span>
                      </div>
                      {role.companies && (
                        <div className="text-xs text-muted-foreground">
                          Top companies: {role.companies.slice(0, 3).join(", ")}
                        </div>
                      )}
                      <div className="flex flex-wrap gap-1 mt-2">
                        {role.top_skills.slice(0, 4).map((skill) => (
                          <span key={skill} className="px-2 py-0.5 rounded-full bg-white/5 text-xs">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>

              <div className="flex justify-between pt-4">
                <Button variant="ghost" onClick={() => setCurrentStep(2)} data-testid="step3-back-btn">
                  <ChevronLeft className="w-4 h-4 mr-1" />
                  Back
                </Button>
                <Button
                  onClick={handleAnalyze}
                  disabled={!canProceed() || loading}
                  className="btn-primary"
                  data-testid="analyze-btn"
                >
                  {loading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Sparkles className="w-4 h-4 mr-2" />}
                  Analyze My Career Fit
                </Button>
              </div>
            </motion.div>
          )}

          {/* Step 4: Loading with Status Bar */}
          {currentStep === 4 && loading && (
            <motion.div
              key="step4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="py-12"
            >
              <AnalysisStatus stage={analysisStage} progress={Math.round(analysisProgress)} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
