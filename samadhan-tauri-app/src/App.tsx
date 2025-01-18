import { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";
import LoginSignupForm from "./components/auth/LoginSignupForm";
import { LoadingAnimation } from "./components/LoadingAnimation";
import Sidebar from "./components/ui/Sidebar";
import ScreenTimeProgress from "./components/charts/ScreenTimeProgress";
import DailyActivityChart from "./components/charts/DailyActivityChart";
import HorizontalChart from "./components/charts/HorizontalChart";
import { Stats } from "./components/ui/Stats";
import "./styles/login-signup-form.css";

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [showSidebar, setShowSidebar] = useState(false);
  const [currentView, setCurrentView] = useState('home');

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
      return <HorizontalChart />;
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
            <div className="flex-1">
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
