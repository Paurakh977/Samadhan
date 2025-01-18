import { useState } from "react";
import { AnimatePresence } from "framer-motion";
import LoginSignupForm from "./components/LoginSignupForm";
import { LoadingAnimation } from "./components/LoadingAnimation";
import Sidebar from "./components/Sidebar";
import ScreenTimeProgress from "./components/ScreenTimeProgress";
import DailyActivityChart from "./components/DailyActivityChart";
import "./styles/login-signup-form.css";

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [showSidebar, setShowSidebar] = useState(false);

  const handleLoadingComplete = () => {
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#fafafa]">
      <AnimatePresence mode="wait">
        {isLoading ? (
          <LoadingAnimation onComplete={handleLoadingComplete} />
        ) : showSidebar ? (
          <div className="flex h-screen">
            <Sidebar />
            <div className="flex-1">
              <div className="h-full flex pl-6 pt-16 pb-8 gap-6">
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
          </div>
        ) : (
          <LoginSignupForm setShowSidebar={setShowSidebar} />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
