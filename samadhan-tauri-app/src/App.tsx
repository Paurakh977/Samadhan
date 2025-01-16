import { useState } from "react";
import { AnimatePresence } from "framer-motion";
import LoginSignupForm from "./components/LoginSignupForm";
import { LoadingAnimation } from "./components/LoadingAnimation";
import "./styles/login-signup-form.css";

function App() {
  const [isLoading, setIsLoading] = useState(true);

  const handleLoadingComplete = () => {
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#fafafa]">
      <AnimatePresence mode="wait">
        {isLoading ? (
          <LoadingAnimation onComplete={handleLoadingComplete} />
        ) : (
          <LoginSignupForm />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
