import { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";
import { invoke } from '@tauri-apps/api/core';
import LoginSignupForm from "./components/auth/LoginSignupForm";
import { LoadingAnimation } from "./components/LoadingAnimation";
import Sidebar from "./components/ui/Sidebar";
import ScreenTimeProgress from "./components/charts/ScreenTimeProgress";
import DailyActivityChart from "./components/charts/DailyActivityChart";
import HorizontalChart from "./components/charts/HorizontalChart";
import AppUsageLineChart from "./components/charts/AppUsageLineChart";
import { Stats } from "./components/ui/Stats";
import WeeklyUsageBarChart from "./components/charts/WeeklyUsageBarChart";
import AppUsageDoughnutChart from "./components/charts/AppUsageDoughnutChart";
import ActivityHeatmap from './components/charts/ActivityHeatmap';
import ScreenTimeBarChart from './components/charts/ScreenTimeBarChart';
import { heatmapData } from './data/heatmapData';
import "./styles/login-signup-form.css";
import "./styles/heatmap.css";
import "./styles/cal-heatmap.css";

interface LoginStatus {
  is_logged_in: boolean;
  email: string | null;
  username: string | null;
}

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [showSidebar, setShowSidebar] = useState(false);
  const [currentView, setCurrentView] = useState('home');
  const [userEmail, setUserEmail] = useState<string>('');
  const [username, setUsername] = useState<string>('');

  // Sample data for the app usage chart
  const appUsageData = [
    {
      appName: "Chrome",
      data: [4.2, 3.8, 5.1, 4.5, 3.9, 2.8, 3.5],
      color: "#059669"
    },
    {
      appName: "VS Code",
      data: [3.1, 3.5, 2.8, 3.9, 4.2, 2.5, 2.9],
      color: "#dc2626"
    },
    {
      appName: "Spotify",
      data: [1.8, 2.2, 1.9, 2.5, 2.1, 3.2, 2.8],
      color: "#2563eb"
    }
  ];

  // Sample data for weekly usage
  const weeklyUsageData = [
    { day: "Mon", hours: 6, minutes: 45 },
    { day: "Tue", hours: 5, minutes: 30 },
    { day: "Wed", hours: 7, minutes: 15 },
    { day: "Thu", hours: 4, minutes: 50 },
    { day: "Fri", hours: 6, minutes: 20 },
    { day: "Sat", hours: 3, minutes: 45 },
    { day: "Sun", hours: 5, minutes: 10 },
  ];

  // Sample data for the doughnut chart


  useEffect(() => {
    const handleViewChange = (event: CustomEvent) => {
      setCurrentView(event.detail);
    };

    window.addEventListener('viewChange', handleViewChange as EventListener);
    return () => {
      window.removeEventListener('viewChange', handleViewChange as EventListener);
    };
  }, []);

  // Check login status after loading animation completes
  const handleLoadingComplete = async () => {
    try {
      const status = await invoke<LoginStatus>('check_login_status');
      console.log('Login status:', status); // Debug log
      
      if (status.is_logged_in && status.email) {
        setShowSidebar(true);
        setUserEmail(status.email);
        if (status.username) {
          setUsername(status.username);
        }
        console.log('User logged in:', { email: status.email, username: status.username }); // Debug log
      } else {
        console.log('User not logged in'); // Debug log
      }
    } catch (error) {
      console.error('Failed to check login status:', error);
    }
    setIsLoading(false);
  };

  const handleLogout = () => {
    setShowSidebar(false);
    setUserEmail('');
    setUsername('');
  };

  const renderContent = () => {
    if (currentView === 'analytics') {
      return (
        <div className="h-screen flex flex-col bg-[#fafafa]">
          {/* Header - Fixed */}
          <div className="px-8 py-6 bg-[#fafafa] border-b border-zinc-100">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-1">App Usage Analytics</h2>
                <p className="text-sm text-gray-500">Track and analyze your application usage patterns</p>
              </div>
              <select className="w-full sm:w-auto bg-white border border-gray-200 rounded-xl px-4 py-2 text-sm text-gray-600 font-medium hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500 transition-all">
                <option value="lastweek">Last week</option>
                <option value="lastmonth">Last month</option>
                <option value="last3months">Last 3 months</option>
                <option value="last6months">Last 6 months</option>
              </select>
            </div>
          </div>
          
          {/* Main Content Area - Scrollable */}
          <div className="flex-1 overflow-y-auto">
            <div className="px-8 py-6">
              <div className="flex gap-6">
                {/* Left Column - Fixed Width */}
                <div className="w-[300px]">
                  {/* Screen Time Card */}
                  <div className="sticky top-6 bg-white rounded-lg shadow-sm border border-zinc-100 p-6">
                    <div className="flex flex-col gap-1.5 mb-6">
                      <h2 className="text-zinc-900 text-sm font-semibold">Screen Time</h2>
                      <p className="text-zinc-500 text-xs font-medium">Today's screen time usage</p>
                    </div>
                    {userEmail ? (
                      <HorizontalChart email={userEmail} />
                    ) : (
                      <div className="flex items-center justify-center h-[300px] text-gray-500">
                        Loading...
                      </div>
                    )}
                  </div>
                </div>

                {/* Right Column - Flexible Width */}
                <div className="flex-1 space-y-6">
                  {/* Bar Chart */}
                  <div className="bg-white rounded-lg shadow-sm border border-zinc-100 p-6">
                    <div className="flex flex-col gap-1.5 mb-4">
                      <h2 className="text-zinc-900 text-sm font-semibold">Daily Screen Time</h2>
                      <p className="text-zinc-500 text-xs font-medium">Screen time usage for the past week</p>
                    </div>
                    <div className="h-[400px]">
                      <WeeklyUsageBarChart data={weeklyUsageData} />
                    </div>
                  </div>

                  {/* Line Chart */}
                  <div className="bg-white rounded-lg shadow-sm border border-zinc-100 p-6">
                    <div className="flex flex-col gap-1.5 mb-4">
                      <h2 className="text-zinc-900 text-sm font-semibold">Usage Trends</h2>
                      <p className="text-zinc-500 text-xs font-medium">Screen time trends over the past month</p>
                    </div>
                    <div className="h-[500px]">
                      <AppUsageLineChart data={appUsageData} />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    }
    if (currentView === 'goals') {
      return (
        <div className="h-screen flex flex-col bg-[#fafafa]">
          {/* Header */}
          <div className="px-4 sm:px-8 py-6 bg-[#fafafa] border-b border-zinc-100">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-1">Goals & Progress</h2>
                <p className="text-sm text-gray-500">Track your daily goals and app usage limits</p>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1 overflow-y-auto px-4 sm:px-8 py-6">
            <div className="space-y-6 max-w-[1800px] mx-auto">
              {/* Activity Heatmap - Full Width */}
              <div className="bg-white rounded-lg shadow-sm border border-zinc-100 p-4 sm:p-6">
                <div className="flex flex-col gap-1.5 mb-6">
                  <h2 className="text-zinc-900 text-sm font-semibold">Activity Contributions</h2>
                  <p className="text-zinc-500 text-xs font-medium">Your daily app usage activity over the past year</p>
                </div>
                <ActivityHeatmap data={heatmapData} />
              </div>

              {/* App Usage Distribution */}
              <div className="max-w-2xl mx-auto">
                <div className="bg-white rounded-lg shadow-sm border border-zinc-100 p-4 sm:p-6">
                  <div className="flex flex-col gap-1.5 mb-4">
                    <h2 className="text-zinc-900 text-sm font-semibold">App Usage Distribution</h2>
                    <p className="text-zinc-500 text-xs font-medium">Your app usage breakdown</p>
                  </div>
                  <div className="h-[350px]">
                    <AppUsageDoughnutChart email={userEmail} />
                  </div>
                </div>
              </div>

              {/* Screen Time Bar Chart */}
              <div className="bg-white rounded-lg shadow-sm border border-zinc-100 p-4 sm:p-6">
                <div className="flex flex-col gap-1.5 mb-6">
                  <h2 className="text-zinc-900 text-sm font-semibold">Screen Time by Category</h2>
                  <p className="text-zinc-500 text-xs font-medium">Screen time usage for the past week</p>
                </div>
                <div className="w-full h-[300px]">
                  <ScreenTimeBarChart width={500} height={300} email={userEmail} />
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    }
    return (
      <div className="h-full flex flex-col px-6 pt-6">
        <Stats />
        <div className="flex gap-6 mt-2 flex-1">
          <ScreenTimeProgress
            startHour={3}
            startMinute={25}
            startPeriod="PM"
            endHour={1}
            endMinute={10}
            endPeriod="AM"
          />
          <DailyActivityChart email={userEmail} />
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-[#fafafa]">
      <AnimatePresence mode="wait">
        {isLoading ? (
          <LoadingAnimation onComplete={handleLoadingComplete} />
        ) : showSidebar ? (
          <div className="flex h-screen overflow-hidden">
            <div className="flex-shrink-0">
              <Sidebar 
                currentView={currentView} 
                userEmail={userEmail}
                username={username}
                onLogout={handleLogout}
              />
            </div>
            <div className="flex-1 min-w-0">
              {renderContent()}
            </div>
          </div>
        ) : (
          <LoginSignupForm 
            setShowSidebar={setShowSidebar} 
            setUserEmail={setUserEmail}
            setUsername={setUsername}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
