import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../lib/api";
import { saveAs } from "file-saver";
import {
  FileText, Upload, Sparkles, Copy, Download, Loader2,
  CheckCircle2, AlertCircle, Briefcase, Building2, Zap,
  FileEdit, ChevronDown, ChevronUp, Star
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Textarea } from "../components/ui/textarea";
import { Label } from "../components/ui/label";
import { Input } from "../components/ui/input";
import { Progress } from "../components/ui/progress";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import AppNavigation from "../components/AppNavigation";

// API base URL configured in lib/api.js

const TONE_OPTIONS = [
  {
    id: "professional",
    name: "Professional",
    description: "Corporate tone for big tech (Google, Meta, Microsoft)",
    icon: "👔"
  },
  {
    id: "confident",
    name: "Confident",
    description: "Bold, assertive for startups and growth companies",
    icon: "💪"
  },
  {
    id: "story-driven",
    name: "Story-Driven",
    description: "Personal narrative for mission-driven companies",
    icon: "📖"
  }
];

// Generation Status Component
const GenerationStatus = ({ stage, progress }) => {
  const stages = [
    { id: 1, name: "Analyzing Resume", icon: "📄" },
    { id: 2, name: "Parsing Job Description", icon: "🔍" },
    { id: 3, name: "Matching Skills", icon: "🎯" },
    { id: 4, name: "Generating Versions", icon: "✍️" },
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
          <Loader2 className="w-5 h-5 animate-spin text-amber-400" />
          Generating Your Cover Letters...
        </h3>
        <span className="text-sm text-muted-foreground">{Math.round(progress)}%</span>
      </div>

      <Progress value={progress} className="h-2" />

      <div className="grid grid-cols-5 gap-2 mt-4">
        {stages.map((s) => (
          <div
            key={s.id}
            className={`text-center p-2 rounded-lg transition-all ${s.id < stage ? "bg-amber-500/20 text-amber-300" :
              s.id === stage ? "bg-indigo-500/30 text-indigo-300 animate-pulse" :
                "bg-white/5 text-muted-foreground"
              }`}
          >
            <div className="text-lg mb-1">{s.icon}</div>
            <div className="text-xs">{s.name}</div>
          </div>
        ))}
      </div>

      <p className="text-center text-sm text-muted-foreground mt-2">
        Creating your optimized cover letter...
      </p>
    </motion.div>
  );
};

// Cover Letter Version Card
const VersionCard = ({ version, index, coverLetterId, onCopy }) => {
  const [expanded, setExpanded] = useState(index === 0);
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async (format) => {
    setDownloading(true);
    try {
      const formData = new FormData();
      formData.append("cover_letter_id", coverLetterId);
      formData.append("version_index", index);
      formData.append("format", format);

      const response = await api.post(`/cover-letter/download`, formData, {
        responseType: "blob"
      });

      const filename = `cover_letter_${version.version_name.toLowerCase().replace(/\s+/g, '_')}.${format}`;
      saveAs(response.data, filename);
      toast.success(`Downloaded ${filename}`);
    } catch (error) {
      toast.error("Download failed");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="glass rounded-xl overflow-hidden"
    >
      <div
        className="p-4 flex items-center justify-between cursor-pointer hover:bg-white/5 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-amber-500/20 flex items-center justify-center">
            <span className="text-lg">✨</span>
          </div>
          <div>
            <h3 className="font-semibold">{version.version_name || "Optimized Cover Letter"}</h3>
            <p className="text-sm text-muted-foreground">{version.word_count} words • ATS Score: {version.ats_score || 90}%</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {version.keywords_used && (
            <span className="text-xs bg-indigo-500/20 text-indigo-300 px-2 py-1 rounded-full">
              {version.keywords_used.length} keywords
            </span>
          )}
          {expanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </div>
      </div>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-white/10"
          >
            <div className="p-4 space-y-4">
              {/* Key Highlights */}
              {version.key_highlights && (
                <div>
                  <h4 className="text-sm font-semibold text-amber-400 mb-2">Key Highlights</h4>
                  <div className="flex flex-wrap gap-2">
                    {version.key_highlights.map((highlight, i) => (
                      <span key={i} className="text-xs bg-amber-500/10 text-amber-300 px-2 py-1 rounded">
                        {highlight}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Cover Letter Text */}
              <div className="bg-black/20 rounded-lg p-4">
                <pre className="whitespace-pre-wrap text-sm text-gray-300 font-sans leading-relaxed">
                  {version.cover_letter}
                </pre>
              </div>

              {/* Actions */}
              <div className="flex flex-wrap gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => {
                    navigator.clipboard.writeText(version.cover_letter);
                    toast.success("Copied to clipboard!");
                  }}
                  data-testid={`copy-version-${index}`}
                >
                  <Copy className="w-4 h-4 mr-1" /> Copy
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleDownload("pdf")}
                  disabled={downloading}
                  data-testid={`download-pdf-${index}`}
                >
                  <Download className="w-4 h-4 mr-1" /> PDF
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => handleDownload("docx")}
                  disabled={downloading}
                  data-testid={`download-docx-${index}`}
                >
                  <Download className="w-4 h-4 mr-1" /> DOCX
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default function CoverLetterPage() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [generationStage, setGenerationStage] = useState(0);
  const [generationProgress, setGenerationProgress] = useState(0);

  // Form state
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [targetRole, setTargetRole] = useState("");
  const [selectedTone, setSelectedTone] = useState("professional");

  // Results
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  // Upload state
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await api.get(`/cover-letter/history`);
      setHistory(response.data.cover_letters || []);
    } catch (error) {
      console.error("Failed to fetch history:", error);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
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

      if (response.data.text) {
        setResumeText(response.data.text);
        toast.success("Resume uploaded successfully!");
      }
    } catch (error) {
      toast.error("Failed to parse resume");
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleGenerate = async () => {
    if (!resumeText.trim() || !jobDescription.trim()) {
      toast.error("Please provide both resume and job description");
      return;
    }

    setLoading(true);
    setResult(null);
    setGenerationStage(1);
    setGenerationProgress(10);

    // Simulate progress
    const progressInterval = setInterval(() => {
      setGenerationProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return prev;
        }
        const newProgress = prev + Math.random() * 15;
        setGenerationStage(Math.ceil(newProgress / 20));
        return Math.min(newProgress, 90);
      });
    }, 500);

    try {
      const response = await api.post(
        `/cover-letter/generate`,
        {
          resume_text: resumeText,
          job_description: jobDescription,
          company_name: companyName,
          target_role: targetRole,
          tone: selectedTone
        }
      );

      clearInterval(progressInterval);
      setGenerationProgress(100);
      setGenerationStage(5);

      setTimeout(() => {
        setResult(response.data);
        setLoading(false);
        fetchHistory();
        toast.success("Cover letters generated successfully!");
      }, 500);
    } catch (error) {
      clearInterval(progressInterval);
      setLoading(false);

      if (error.response?.status === 403) {
        toast.error("Monthly limit reached. Upgrade to Pro for unlimited cover letters.");
      } else {
        const detail = error.response?.data?.detail;
        let errorMessage = "Generation failed";

        if (typeof detail === "string") {
          errorMessage = detail;
        } else if (Array.isArray(detail) && detail.length > 0) {
          errorMessage = detail.map(err => err.msg || err.message || "Validation error").join(", ");
        } else if (typeof detail === "object" && detail?.message) {
          errorMessage = detail.message;
        }

        toast.error(errorMessage);
      }
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <AppNavigation />

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/30 mb-4">
            <FileEdit className="w-4 h-4 text-amber-400" />
            <span className="text-sm text-amber-300">Cover Letter Generator</span>
          </div>
          <h1 className="text-3xl font-bold mb-2">AI Cover Letter That Gets Interviews</h1>
          <p className="text-muted-foreground">
            Paste a job description. Get 3 unique variations of a personalized cover letter in seconds.
          </p>
        </motion.div>

        {loading ? (
          <GenerationStatus stage={generationStage} progress={generationProgress} />
        ) : result ? (
          /* Results View */
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            {/* Match Analysis */}
            {result.job_match_analysis && (
              <div className="glass rounded-2xl p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                  <Zap className="w-5 h-5 text-amber-400" />
                  Job Match Analysis
                </h2>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="bg-black/20 rounded-lg p-4 text-center">
                    <div className="text-3xl font-bold text-amber-400">
                      {result.job_match_analysis.match_score || 85}%
                    </div>
                    <div className="text-sm text-muted-foreground">Match Score</div>
                  </div>
                  <div className="bg-black/20 rounded-lg p-4">
                    <div className="text-sm font-semibold text-emerald-400 mb-2">Matching Skills</div>
                    <div className="flex flex-wrap gap-1">
                      {(result.job_match_analysis.matching_skills || []).slice(0, 5).map((skill, i) => (
                        <span key={i} className="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="bg-black/20 rounded-lg p-4">
                    <div className="text-sm font-semibold text-indigo-400 mb-2">Skills to Emphasize</div>
                    <div className="flex flex-wrap gap-1">
                      {(result.job_match_analysis.skills_to_emphasize || []).slice(0, 5).map((skill, i) => (
                        <span key={i} className="text-xs bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Cover Letter Versions */}
            <div className="space-y-4">
              <h2 className="text-xl font-bold flex items-center gap-2">
                <FileText className="w-5 h-5 text-amber-400" />
                Your 3 Cover Letter Versions
              </h2>
              {(result.versions || []).map((version, index) => (
                <VersionCard
                  key={index}
                  version={version}
                  index={index}
                  coverLetterId={result.cover_letter_id}
                />
              ))}
            </div>

            {/* Generate Another */}
            <div className="text-center">
              <Button
                onClick={() => setResult(null)}
                className="btn-primary"
                data-testid="generate-another-btn"
              >
                Generate Another Cover Letter
              </Button>
            </div>
          </motion.div>
        ) : (
          /* Input Form */
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Left: Resume Input */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="glass rounded-2xl p-6 space-y-4"
            >
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <FileText className="w-5 h-5 text-indigo-400" />
                Your Resume
              </h2>

              {/* File Upload */}
              <div className="border-2 border-dashed border-white/20 rounded-xl p-6 text-center hover:border-indigo-500/50 transition-colors">
                <input
                  type="file"
                  accept=".pdf,.docx,.doc,.txt"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="resume-upload"
                  data-testid="resume-upload-input"
                />
                <label htmlFor="resume-upload" className="cursor-pointer">
                  {uploading ? (
                    <div className="space-y-2">
                      <Loader2 className="w-8 h-8 mx-auto animate-spin text-indigo-400" />
                      <Progress value={uploadProgress} className="h-2 max-w-xs mx-auto" />
                      <p className="text-sm text-muted-foreground">Uploading... {Math.round(uploadProgress)}%</p>
                    </div>
                  ) : (
                    <>
                      <Upload className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
                      <p className="text-sm text-muted-foreground">
                        Drop PDF/DOCX or click to upload
                      </p>
                    </>
                  )}
                </label>
              </div>

              {/* Or Paste */}
              <div className="text-center text-sm text-muted-foreground">or paste your resume</div>

              <Textarea
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Paste your resume text here..."
                className="min-h-[200px] bg-black/20"
                data-testid="resume-textarea"
              />
            </motion.div>

            {/* Right: Job Description & Options */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="glass rounded-2xl p-6 space-y-4"
            >
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <Briefcase className="w-5 h-5 text-amber-400" />
                Job Details
              </h2>

              {/* Company & Role */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Company Name</Label>
                  <Input
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    placeholder="e.g., OpenAI"
                    className="bg-black/20"
                    data-testid="company-name-input"
                  />
                </div>
                <div>
                  <Label>Target Role</Label>
                  <Input
                    value={targetRole}
                    onChange={(e) => setTargetRole(e.target.value)}
                    placeholder="e.g., ML Engineer"
                    className="bg-black/20"
                    data-testid="target-role-input"
                  />
                </div>
              </div>

              {/* Job Description */}
              <div>
                <Label>Job Description *</Label>
                <Textarea
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Paste the full job description here..."
                  className="min-h-[150px] bg-black/20"
                  data-testid="job-description-textarea"
                />
              </div>

              {/* Tone Selection */}
              <div>
                <Label className="mb-2 block">Select Tone</Label>
                <div className="grid grid-cols-3 gap-2">
                  {TONE_OPTIONS.map((tone) => (
                    <button
                      key={tone.id}
                      onClick={() => setSelectedTone(tone.id)}
                      className={`p-3 rounded-lg border transition-all text-left ${selectedTone === tone.id
                        ? "border-amber-500 bg-amber-500/10"
                        : "border-white/10 hover:border-white/20"
                        }`}
                      data-testid={`tone-${tone.id}`}
                    >
                      <div className="text-lg mb-1">{tone.icon}</div>
                      <div className="text-sm font-medium">{tone.name}</div>
                      <div className="text-xs text-muted-foreground">{tone.description}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Generate Button */}
              <Button
                onClick={handleGenerate}
                disabled={loading || !resumeText.trim() || !jobDescription.trim()}
                className="w-full btn-primary h-12"
                data-testid="generate-cover-letter-btn"
              >
                <Sparkles className="w-5 h-5 mr-2" />
                Generate Cover Letter
              </Button>

              <p className="text-xs text-center text-muted-foreground">
                Free tier: 1 cover letter/month • Pro: Unlimited
              </p>
            </motion.div>
          </div>
        )}

        {/* History Section */}
        {history.length > 0 && !result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8"
          >
            <h2 className="text-xl font-bold mb-4">Recent Cover Letters</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {history.slice(0, 6).map((cl) => (
                <div
                  key={cl.id}
                  className="glass rounded-xl p-4 cursor-pointer hover:bg-white/5 transition-colors"
                  onClick={() => setResult(cl)}
                >
                  <div className="flex items-center gap-3 mb-2">
                    <Building2 className="w-5 h-5 text-amber-400" />
                    <span className="font-medium">{cl.company_name || "Company"}</span>
                  </div>
                  <div className="text-sm text-muted-foreground">{cl.target_role || "Role"}</div>
                  <div className="text-xs text-muted-foreground mt-2">
                    {new Date(cl.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </main>
    </div>
  );
}
