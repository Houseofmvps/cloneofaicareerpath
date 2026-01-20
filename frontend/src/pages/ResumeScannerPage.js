import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import api from "../lib/api";
import {
  FileSearch, Upload, Sparkles, Target, AlertCircle, CheckCircle2,
  XCircle, Loader2, ArrowRight, TrendingUp, AlertTriangle, Zap,
  FileText, Star
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Textarea } from "../components/ui/textarea";
import { Label } from "../components/ui/label";
import { Progress } from "../components/ui/progress";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import AppNavigation from "../components/AppNavigation";

// API base URL configured in lib/api.js

// Grade color mapping
const getGradeColor = (grade) => {
  if (!grade) return "text-gray-400";
  const g = grade.toUpperCase();
  if (g.startsWith("A")) return "text-emerald-400";
  if (g.startsWith("B")) return "text-blue-400";
  if (g.startsWith("C")) return "text-yellow-400";
  return "text-red-400";
};

const getScoreColor = (score) => {
  if (score >= 80) return "text-emerald-400";
  if (score >= 60) return "text-blue-400";
  if (score >= 40) return "text-yellow-400";
  return "text-red-400";
};

const getScoreBg = (score) => {
  if (score >= 80) return "bg-emerald-500/20 border-emerald-500/30";
  if (score >= 60) return "bg-blue-500/20 border-blue-500/30";
  if (score >= 40) return "bg-yellow-500/20 border-yellow-500/30";
  return "bg-red-500/20 border-red-500/30";
};

export default function ResumeScannerPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [scanResult, setScanResult] = useState(null);
  const [usage, setUsage] = useState({ used: 0, limit: 2, canScan: true });
  const [scanHistory, setScanHistory] = useState([]);
  const [uploading, setUploading] = useState(false);

  const fetchRoles = async () => {
    try {
      const response = await api.get(`/roles`);
      setRoles(response.data.roles || []);
    } catch (error) {
      console.error("Failed to fetch roles:", error);
    }
  };

  const fetchUsage = async () => {
    try {
      const response = await api.get(`/resume/scan/usage`);
      setUsage({
        used: response.data.scans_used,
        limit: response.data.scans_limit,
        canScan: response.data.can_scan
      });
    } catch (error) {
      console.error("Failed to fetch usage:", error);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await api.get(`/resume/scan/history`);
      setScanHistory(response.data.scans || []);
    } catch (error) {
      console.error("Failed to fetch history:", error);
    }
  };

  useEffect(() => {
    fetchRoles();
    fetchUsage();
    fetchHistory();
  }, []);

  const handleFileUpload = async (file) => {
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post(`/resume/parse`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResumeText(response.data.text || "");
      toast.success(`"${file.name}" uploaded successfully!`);
    } catch (error) {
      toast.error("Failed to parse file. Please paste text instead.");
    } finally {
      setUploading(false);
    }
  };

  const handleScan = async () => {
    if (!resumeText.trim() || !selectedRole) {
      toast.error("Please provide resume text and select a target role");
      return;
    }

    if (!usage.canScan) {
      toast.error("Monthly scan limit reached. Upgrade to Pro for unlimited scans.");
      return;
    }

    setLoading(true);
    setScanResult(null);

    try {
      const response = await api.post(`/resume/scan`, {
        resume_text: resumeText,
        target_role_id: selectedRole
      });

      setScanResult(response.data);
      setUsage({
        used: response.data.usage.scans_used,
        limit: response.data.usage.scans_limit,
        canScan: response.data.usage.scans_used < response.data.usage.scans_limit
      });
      fetchHistory();
      toast.success("Resume scan complete!");
    } catch (error) {
      const detail = error.response?.data?.detail;
      let errorMessage = "Failed to scan resume";

      if (typeof detail === "string") {
        errorMessage = detail;
      } else if (Array.isArray(detail) && detail.length > 0) {
        // Handle Pydantic validation errors array
        errorMessage = detail.map(err => err.msg || err.message || "Validation error").join(", ");
      } else if (typeof detail === "object" && detail?.message) {
        errorMessage = detail.message;
      }

      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const isPro = user?.subscription_tier === "pro";

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
                <FileSearch className="w-8 h-8 text-indigo-400" />
                Resume Scanner
              </h1>
              <p className="text-muted-foreground">
                Get instant ATS score and actionable improvements
              </p>
            </div>

            <div className="glass rounded-xl px-6 py-4 text-center">
              <div className="text-sm text-muted-foreground mb-1">FREE Scans</div>
              <div className="text-2xl font-bold">
                <span className={usage.used >= usage.limit && !isPro ? "text-red-400" : "text-emerald-400"}>
                  {usage.used}
                </span>
                <span className="text-muted-foreground">/{isPro ? "∞" : usage.limit}</span>
              </div>
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
                  id="scanner-file-upload"
                  onChange={(e) => handleFileUpload(e.target.files[0])}
                  disabled={uploading}
                />

                <label
                  htmlFor="scanner-file-upload"
                  className={`flex items-center justify-center gap-2 p-4 border-2 border-dashed border-white/20 rounded-xl cursor-pointer hover:border-indigo-500/50 transition-colors ${uploading ? "opacity-50" : ""}`}
                >
                  {uploading ? (
                    <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
                  ) : (
                    <Upload className="w-5 h-5 text-indigo-400" />
                  )}
                  <span>{uploading ? "Processing..." : "Upload PDF/DOCX or paste below"}</span>
                </label>
              </div>

              <Textarea
                placeholder="Paste your resume text here..."
                className="min-h-[200px] input-dark"
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
              />
              <div className="text-xs text-muted-foreground mt-2 text-right">
                {resumeText.length} characters
              </div>
            </div>

            {/* Target Role */}
            <div className="glass rounded-2xl p-6">
              <Label className="text-lg font-semibold mb-4 block">
                <Target className="w-5 h-5 inline mr-2 text-indigo-400" />
                Target Role
              </Label>

              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="w-full h-12 px-4 rounded-lg bg-black/20 border border-white/10 text-foreground focus:border-indigo-500"
              >
                <option value="">Select a role to optimize for...</option>
                {roles.map((role) => (
                  <option key={role.id} value={role.id}>
                    {role.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Scan Button */}
            <Button
              onClick={handleScan}
              disabled={loading || !usage.canScan || !resumeText.trim() || !selectedRole}
              className="w-full btn-primary py-6 text-lg"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                  Analyzing Resume...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 mr-2" />
                  Scan My Resume
                </>
              )}
            </Button>

            {!usage.canScan && (
              <div className="glass rounded-xl p-4 border border-amber-500/30">
                <div className="flex items-center gap-2 text-amber-400 mb-2">
                  <AlertCircle className="w-5 h-5" />
                  <span className="font-medium">Free scans used up</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Upgrade to Pro for unlimited scans and full features
                </p>
              </div>
            )}

            {/* Recent Scans */}
            {scanHistory.length > 0 && (
              <div className="glass rounded-2xl p-6">
                <h3 className="font-semibold mb-4">Recent Scans</h3>
                <div className="space-y-2">
                  {scanHistory.slice(0, 3).map((scan) => (
                    <div
                      key={scan.id}
                      className="flex items-center justify-between p-3 rounded-lg bg-white/5"
                    >
                      <div>
                        <div className="font-medium text-sm">{scan.target_role}</div>
                        <div className="text-xs text-muted-foreground">
                          {new Date(scan.created_at).toLocaleDateString()}
                        </div>
                      </div>
                      <div className={`text-lg font-bold ${getGradeColor(scan.overall_grade)}`}>
                        {scan.overall_grade}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>

          {/* Results Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-6"
          >
            {loading && (
              <div className="glass rounded-2xl p-8 text-center">
                <Loader2 className="w-12 h-12 text-indigo-400 animate-spin mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">Analyzing Your Resume...</h3>
                <p className="text-muted-foreground text-sm">
                  Checking ATS compatibility, keywords, and formatting
                </p>
              </div>
            )}

            {!loading && scanResult ? (
              <>
                {/* Overall Grade */}
                <div className={`glass rounded-2xl p-6 border-2 ${getScoreBg(scanResult.ats_score)}`}>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Overall Grade</h3>
                    <div className={`text-5xl font-bold ${getGradeColor(scanResult.overall_grade)}`}>
                      {scanResult.overall_grade}
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    for {scanResult.target_role}
                  </p>
                </div>

                {/* Score Cards */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="glass rounded-xl p-4 text-center">
                    <div className={`text-2xl font-bold ${getScoreColor(scanResult.ats_score)}`}>
                      {scanResult.ats_score}
                    </div>
                    <div className="text-xs text-muted-foreground">ATS Score</div>
                    <Progress value={scanResult.ats_score} className="h-1 mt-2" />
                  </div>
                  <div className="glass rounded-xl p-4 text-center">
                    <div className={`text-2xl font-bold ${getScoreColor(scanResult.human_appeal_score)}`}>
                      {scanResult.human_appeal_score}
                    </div>
                    <div className="text-xs text-muted-foreground">Human Appeal</div>
                    <Progress value={scanResult.human_appeal_score} className="h-1 mt-2" />
                  </div>
                  <div className="glass rounded-xl p-4 text-center">
                    <div className={`text-2xl font-bold ${getScoreColor(scanResult.keyword_match_percent)}`}>
                      {scanResult.keyword_match_percent}%
                    </div>
                    <div className="text-xs text-muted-foreground">Keyword Match</div>
                    <Progress value={scanResult.keyword_match_percent} className="h-1 mt-2" />
                  </div>
                </div>

                {/* Quick Wins */}
                {scanResult.quick_wins?.length > 0 && (
                  <div className="glass rounded-2xl p-6 border border-amber-500/30">
                    <h3 className="font-semibold mb-3 flex items-center gap-2 text-amber-400">
                      <Zap className="w-5 h-5" />
                      Quick Wins (Easy Fixes)
                    </h3>
                    <ul className="space-y-2">
                      {scanResult.quick_wins.map((win, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm">
                          <Star className="w-4 h-4 text-amber-400 mt-0.5 shrink-0" />
                          <span>{win}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Keywords */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="glass rounded-xl p-4">
                    <h4 className="font-medium text-sm mb-3 flex items-center gap-2 text-emerald-400">
                      <CheckCircle2 className="w-4 h-4" />
                      Keywords Found ({scanResult.keywords_found?.length || 0})
                    </h4>
                    <div className="flex flex-wrap gap-1">
                      {scanResult.keywords_found?.slice(0, 8).map((kw, i) => (
                        <span key={i} className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-xs">
                          {kw}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="glass rounded-xl p-4">
                    <h4 className="font-medium text-sm mb-3 flex items-center gap-2 text-red-400">
                      <XCircle className="w-4 h-4" />
                      Missing Keywords ({scanResult.keywords_missing?.length || 0})
                    </h4>
                    <div className="flex flex-wrap gap-1">
                      {scanResult.keywords_missing?.slice(0, 8).map((kw, i) => (
                        <span key={i} className="px-2 py-0.5 rounded-full bg-red-500/20 text-red-300 text-xs">
                          {kw}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Strengths */}
                {scanResult.strengths?.length > 0 && (
                  <div className="glass rounded-xl p-4">
                    <h4 className="font-medium text-sm mb-3 flex items-center gap-2 text-emerald-400">
                      <TrendingUp className="w-4 h-4" />
                      Strengths
                    </h4>
                    <ul className="space-y-1">
                      {scanResult.strengths.map((s, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                          <CheckCircle2 className="w-3 h-3 text-emerald-400 mt-1 shrink-0" />
                          <span>{s}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Improvements */}
                {scanResult.improvements?.length > 0 && (
                  <div className="glass rounded-xl p-4">
                    <h4 className="font-medium text-sm mb-3 flex items-center gap-2 text-blue-400">
                      <AlertTriangle className="w-4 h-4" />
                      Areas to Improve
                    </h4>
                    <ul className="space-y-1">
                      {scanResult.improvements.map((imp, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                          <span className="text-blue-400 shrink-0">→</span>
                          <span>{imp}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Formatting Issues */}
                {scanResult.formatting_issues?.length > 0 && (
                  <div className="glass rounded-xl p-4">
                    <h4 className="font-medium text-sm mb-3 flex items-center gap-2 text-yellow-400">
                      <AlertCircle className="w-4 h-4" />
                      Formatting Issues
                    </h4>
                    <ul className="space-y-1">
                      {scanResult.formatting_issues.map((issue, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                          <span className="text-yellow-400 shrink-0">!</span>
                          <span>{issue}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* CTA */}
                <div className="glass rounded-2xl p-6 border border-indigo-500/30 bg-indigo-500/10">
                  <h3 className="font-semibold mb-2">Want an Optimized Resume?</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Generate an ATS-optimized, professionally written resume that addresses all these issues.
                  </p>
                  <Button
                    onClick={() => navigate("/cv-generator")}
                    className="w-full btn-primary"
                  >
                    <FileText className="w-4 h-4 mr-2" />
                    Generate Optimized Resume
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </div>
              </>
            ) : !loading ? (
              <div className="glass rounded-2xl p-12 text-center">
                <FileSearch className="w-16 h-16 text-muted-foreground mx-auto mb-4 opacity-50" />
                <h3 className="text-lg font-semibold mb-2">No Scan Yet</h3>
                <p className="text-muted-foreground">
                  Upload your resume and select a target role to get instant feedback
                </p>
              </div>
            ) : null}
          </motion.div>
        </div>
      </main>
    </div>
  );
}
