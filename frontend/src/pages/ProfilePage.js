import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import {
  User, Crown, Zap, FileText, BookOpen, BarChart3,
  CreditCard, Settings, ChevronRight, Check
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Progress } from "../components/ui/progress";
import { toast } from "sonner";
import { useAuth } from "../context/AuthContext";
import AppNavigation from "../components/AppNavigation";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function ProfilePage() {
  const { user, refreshUser } = useAuth();
  const [usage, setUsage] = useState(null);
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [usageRes, subRes] = await Promise.all([
        axios.get(`${API}/usage`),
        axios.get(`${API}/payments/subscription`)
      ]);
      setUsage(usageRes.data);
      setSubscription(subRes.data);
    } catch (error) {
      console.error("Failed to fetch data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleMockUpgrade = async () => {
    try {
      await axios.post(`${API}/payments/mock-upgrade`);
      toast.success("Upgraded to Pro! (Mock)");
      await refreshUser();
      fetchData();
    } catch (error) {
      toast.error("Upgrade failed");
    }
  };

  const handleMockPurchase = async (productType) => {
    try {
      await axios.post(`${API}/payments/mock-purchase?product_type=${productType}`);
      toast.success(`Purchased ${productType}! (Mock)`);
      fetchData();
    } catch (error) {
      toast.error("Purchase failed");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <AppNavigation />
        <div className="flex items-center justify-center h-[calc(100vh-64px)]">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      </div>
    );
  }

  const isPro = user?.subscription_tier === "pro";

  return (
    <div className="min-h-screen bg-background noise-bg">
      <AppNavigation />

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Profile Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-2xl p-8 mb-8"
        >
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <User className="w-10 h-10 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">{user?.name}</h1>
              <p className="text-muted-foreground">{user?.email}</p>
              <div className="flex items-center gap-2 mt-2">
                {isPro ? (
                  <span className="flex items-center gap-1 px-3 py-1 rounded-full bg-amber-500/20 text-amber-400 text-sm">
                    <Crown className="w-4 h-4" /> Pro Member
                  </span>
                ) : (
                  <span className="flex items-center gap-1 px-3 py-1 rounded-full bg-white/10 text-muted-foreground text-sm">
                    Free Plan
                  </span>
                )}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Usage Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid md:grid-cols-3 gap-6 mb-8"
        >
          {/* Career Analyses */}
          <div className="glass rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg bg-indigo-500/20 flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-indigo-400" />
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Career Analyses</div>
                <div className="text-xl font-bold">
                  {usage?.analyses_used || 0}/{isPro ? "∞" : usage?.analyses_limit || 1}
                </div>
              </div>
            </div>
            <Progress 
              value={isPro ? 0 : ((usage?.analyses_used || 0) / (usage?.analyses_limit || 1)) * 100} 
              className="h-2" 
            />
            <div className="text-xs text-muted-foreground mt-2">
              {isPro ? "Unlimited" : `${(usage?.analyses_limit || 1) - (usage?.analyses_used || 0)} remaining this month`}
            </div>
          </div>

          {/* Resume Generations */}
          <div className="glass rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg bg-emerald-500/20 flex items-center justify-center">
                <FileText className="w-5 h-5 text-emerald-400" />
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Resume Generations</div>
                <div className="text-xl font-bold">
                  {usage?.cv_generations_used || 0}/{isPro ? "∞" : usage?.cv_generations_limit || 2}
                </div>
              </div>
            </div>
            <Progress 
              value={isPro ? 0 : ((usage?.cv_generations_used || 0) / (usage?.cv_generations_limit || 2)) * 100} 
              className="h-2" 
            />
            <div className="text-xs text-muted-foreground mt-2">
              {subscription?.cv_credits > 0 && (
                <span className="text-amber-400">+{subscription.cv_credits} bonus credits</span>
              )}
            </div>
          </div>

          {/* Learning Paths */}
          <div className="glass rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-purple-400" />
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Learning Paths</div>
                <div className="text-xl font-bold">
                  {usage?.learning_paths_used || 0}/{isPro ? "∞" : usage?.learning_paths_limit || 1}
                </div>
              </div>
            </div>
            <Progress 
              value={isPro ? 0 : ((usage?.learning_paths_used || 0) / (usage?.learning_paths_limit || 1)) * 100} 
              className="h-2" 
            />
            <div className="text-xs text-muted-foreground mt-2">
              {subscription?.learning_path_credits > 0 && (
                <span className="text-amber-400">+{subscription.learning_path_credits} bonus credits</span>
              )}
            </div>
          </div>
        </motion.div>

        {/* Subscription Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <h2 className="text-xl font-bold mb-4">Subscription</h2>
          
          {isPro ? (
            <div className="glass rounded-xl p-6 border-2 border-amber-500/30">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center">
                    <Crown className="w-6 h-6 text-amber-400" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold">Pro Plan</h3>
                    <p className="text-muted-foreground">$29/month • Unlimited everything</p>
                  </div>
                </div>
                <Button variant="outline" className="btn-secondary">
                  Manage Subscription
                </Button>
              </div>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 gap-6">
              {/* Pro Plan */}
              <div className="glass rounded-xl p-6 border-2 border-indigo-500/50 relative overflow-hidden">
                <div className="absolute top-0 right-0 px-3 py-1 bg-indigo-500 text-xs font-medium rounded-bl-lg">
                  RECOMMENDED
                </div>
                <div className="flex items-center gap-3 mb-4">
                  <Crown className="w-6 h-6 text-amber-400" />
                  <div>
                    <h3 className="font-bold">Pro Plan</h3>
                    <p className="text-2xl font-bold">$29<span className="text-sm text-muted-foreground">/month</span></p>
                  </div>
                </div>
                <ul className="space-y-2 mb-6">
                  {[
                    "Unlimited career analyses",
                    "Unlimited Resume generations",
                    "Unlimited learning paths",
                    "Priority AI responses",
                    "Email support"
                  ].map((feature) => (
                    <li key={feature} className="flex items-center gap-2 text-sm">
                      <Check className="w-4 h-4 text-emerald-400" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Button 
                  className="w-full btn-primary"
                  onClick={handleMockUpgrade}
                  data-testid="profile-upgrade-btn"
                >
                  <Zap className="w-4 h-4 mr-2" />
                  Upgrade to Pro
                </Button>
              </div>

              {/* Buy Credits */}
              <div className="glass rounded-xl p-6">
                <h3 className="font-bold mb-4">Buy Credits</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
                    <div>
                      <div className="font-medium">1 Resume Generation</div>
                      <div className="text-sm text-muted-foreground">$0.49</div>
                    </div>
                    <Button 
                      size="sm" 
                      className="btn-secondary"
                      onClick={() => handleMockPurchase("cv_single")}
                    >
                      Buy
                    </Button>
                  </div>
                  <div className="flex items-center justify-between p-3 rounded-lg bg-white/5">
                    <div>
                      <div className="font-medium">50 Resumes + 3 Paths + 3 Analyses</div>
                      <div className="text-sm text-muted-foreground">$13.99 (best value)</div>
                    </div>
                    <Button 
                      size="sm" 
                      className="btn-primary"
                      onClick={() => handleMockPurchase("cv_bulk_50")}
                    >
                      Buy
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
          <div className="glass rounded-xl divide-y divide-white/10">
            {[
              { icon: BarChart3, label: "Start Career Analysis", href: "/analyze", color: "text-indigo-400" },
              { icon: FileText, label: "Build Resume", href: "/cv-generator", color: "text-emerald-400" },
              { icon: BookOpen, label: "Create Learning Path", href: "/learning-path", color: "text-purple-400" }
            ].map((action) => (
              <a
                key={action.label}
                href={action.href}
                className="flex items-center justify-between p-4 hover:bg-white/5 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <action.icon className={`w-5 h-5 ${action.color}`} />
                  <span>{action.label}</span>
                </div>
                <ChevronRight className="w-5 h-5 text-muted-foreground" />
              </a>
            ))}
          </div>
        </motion.div>
      </main>
    </div>
  );
}
