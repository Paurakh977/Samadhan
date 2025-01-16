import { useState } from "react";
import { AnimatePresence } from "framer-motion";
import LoginSignupForm from "./components/LoginSignupForm";
import { LoadingAnimation } from "./components/LoadingAnimation";
import Sidebar from "./components/Sidebar";
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
          <Sidebar />
        ) : (
          <LoginSignupForm setShowSidebar={setShowSidebar} />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
