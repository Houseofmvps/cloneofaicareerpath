import { Link, useLocation, useNavigate } from "react-router-dom";
import { Brain, FileText, BookOpen, BarChart3, User, LogOut, Crown, FileEdit, Zap, MessageSquare, Search, FileSearch } from "lucide-react";
import { Button } from "./ui/button";
import { useAuth } from "../context/AuthContext";
import { toast } from "sonner";

const NAV_ITEMS = [
  { path: "/resume-scanner", label: "Scanner", icon: FileSearch },
  { path: "/analyze", label: "Analysis", icon: BarChart3 },
  { path: "/learning-path", label: "Learning", icon: BookOpen },
  { path: "/cv-generator", label: "Resume", icon: FileText },
  { path: "/cover-letter", label: "Cover Letter", icon: FileEdit },
  { path: "/interview-prep", label: "Interview", icon: MessageSquare },
  { path: "/smart-jobs", label: "Jobs", icon: Search },
];

export default function AppNavigation() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/");
    toast.success("Logged out successfully");
  };

  return (
    <header className="glass-heavy border-b border-white/5 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold gradient-text hidden sm:block">CareerLift</span>
          </Link>

          {/* Main Navigation Tabs */}
          <nav className="flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`
                    flex items-center gap-2 px-4 py-2 rounded-lg transition-all text-sm font-medium
                    ${isActive 
                      ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' 
                      : 'text-muted-foreground hover:text-foreground hover:bg-white/5'
                    }
                  `}
                  data-testid={`nav-${item.path.slice(1)}`}
                >
                  <item.icon className="w-4 h-4" />
                  <span className="hidden md:inline">{item.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* User Menu */}
          <div className="flex items-center gap-3">
            <Link
              to="/profile"
              className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 transition-colors"
            >
              <User className="w-4 h-4" />
              <span className="text-sm hidden sm:block">{user?.name?.split(" ")[0]}</span>
              {user?.subscription_tier === "pro" && (
                <Crown className="w-4 h-4 text-amber-400" />
              )}
            </Link>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={handleLogout}
              data-testid="nav-logout-btn"
            >
              <LogOut className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
