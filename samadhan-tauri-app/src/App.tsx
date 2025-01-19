import { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";
import LoginSignupForm from "./components/auth/LoginSignupForm";
import { LoadingAnimation } from "./components/LoadingAnimation";
import Sidebar from "./components/ui/Sidebar";
import ScreenTimeProgress from "./components/charts/ScreenTimeProgress";
import DailyActivityChart from "./components/charts/DailyActivityChart";
import HorizontalChart from "./components/charts/HorizontalChart";
import AppUsageLineChart from "./components/charts/AppUsageLineChart";
import { Stats } from "./components/ui/Stats";
import "./styles/login-signup-form.css";

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [showSidebar, setShowSidebar] = useState(false);
  const [currentView, setCurrentView] = useState('home');

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

  useEffect(() => {
    const handleViewChange = (e: CustomEvent) => {
      const newView = e.detail;
      setCurrentView(newView);
    };
    window.addEventListener('viewChange', handleViewChange as EventListener);
    return () => window.removeEventListener('viewChange', handleViewChange as EventListener);
  }, []);

  const handleLoadingComplete = () => {
    setIsLoading(false);
  };

  const renderContent = () => {
    if (currentView === 'analytics') {
      return (
        <div className="h-full flex flex-col px-8 py-8 overflow-x-hidden">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-1">App Usage Analytics</h2>
              <p className="text-sm text-gray-500">Track and analyze your application usage patterns</p>
            </div>
            <select className="bg-white border border-gray-200 rounded-xl px-4 py-2 text-sm text-gray-600 font-medium hover:border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500 transition-all">
              <option value="lastweek">Last week</option>
              <option value="lastmonth">Last month</option>
              <option value="last3months">Last 3 months</option>
              <option value="last6months">Last 6 months</option>
            </select>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-[minmax(300px,320px)_1fr] gap-6 flex-1 min-w-0 max-h-[calc(100vh-12rem)]">
            <div className="bg-white rounded-2xl shadow-sm p-7 hover:shadow-md transition-all h-full overflow-hidden">
              <div className="space-y-1 mb-8">
                <h3 className="text-[15px] font-semibold text-gray-900">Top Applications</h3>
                <p className="text-sm text-gray-500">Most used apps this week</p>
              </div>
              <div className="h-[calc(100%-6rem)]">
                <HorizontalChart />
              </div>
            </div>
            
            <div className="bg-white rounded-2xl shadow-sm p-7 hover:shadow-md transition-all h-full overflow-hidden">
              <div className="space-y-1 mb-8">
                <h3 className="text-[15px] font-semibold text-gray-900">Usage Trends</h3>
                <p className="text-sm text-gray-500">Daily app usage patterns</p>
              </div>
              <div className="h-[calc(100%-6rem)]">
                <AppUsageLineChart data={appUsageData} />
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
          <DailyActivityChart />
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
          <div className="flex h-screen">
            <Sidebar currentView={currentView} />
            <div className="flex-1 overflow-hidden">
              {renderContent()}
            </div>
          </div>
        ) : (
          <LoginSignupForm setShowSidebar={setShowSidebar} />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
