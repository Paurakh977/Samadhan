import { useState } from "react";
import LoginSignupForm from "./components/LoginSignupForm";
import { LoadingAnimation } from "./components/LoadingAnimation";
import "./styles/login-signup-form.css";
import "./styles/loading-animation.css";

function App() {
  const [isLoading, setIsLoading] = useState(true);

  const handleLoadingComplete = () => {
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen">
      {isLoading ? (
        <LoadingAnimation onComplete={handleLoadingComplete} />
      ) : (
        <div className="flex items-center justify-center min-h-screen">
          <LoginSignupForm />
        </div>
      )}
    </div>
  );
}

export default App;
