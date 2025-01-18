import { useState } from 'react';
import { motion } from 'framer-motion';
import '../../styles/login-signup-form.css';

interface FormData {
  username: string;
  email?: string;
  password: string;
}

interface LoginSignupFormProps {
  setShowSidebar: (show: boolean) => void;
}

const LoginSignupForm: React.FC<LoginSignupFormProps> = ({ setShowSidebar }) => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    username: '',
    email: '',
    password: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isSignUp && formData.username.trim() && formData.password.trim()) {
      setShowSidebar(true);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleModeSwitch = (mode: boolean) => {
    setIsSignUp(mode);
    setShowPassword(false);
    setFormData({
      username: '',
      email: '',
      password: '',
    });
  };

  return (
    <motion.div 
      className="flex items-center justify-center min-h-screen w-full"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{
        duration: 0.4,
        ease: "easeOut"
      }}
    >
      <div className={`container ${isSignUp ? 'sign-up-mode' : ''}`}>
        <div className="forms-container">
          <div className="signin-signup">
            {/* Sign In Form */}
            <form className="sign-in-form" onSubmit={handleSubmit}>
              <h2 className="title">Sign In</h2>
              <div className="input-field">
                <i className="fas fa-user"></i>
                <input
                  type="text"
                  name="username"
                  placeholder="Username"
                  required
                  value={formData.username}
                  onChange={handleInputChange}
                />
              </div>
              <div className="input-field">
                <i className="fas fa-lock"></i>
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Password"
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                />
                <button 
                  type="button" 
                  className="password-toggle"
                  onClick={togglePasswordVisibility}
                  tabIndex={-1}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  <i className={`far ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`}></i>
                </button>
              </div>
              <div className="forgot-password">
                <a href="#">Forgot Password?</a>
              </div>
              <button type="submit" className="btn">Login</button>
              <div className="divider">
                <div className="line"></div>
                <span>or continue with</span>
                <div className="line"></div>
              </div>
              <div className="social-buttons">
                <button type="button" className="social-btn google">
                  <i className="fab fa-google"></i>
                  <span>Google</span>
                </button>
                <button type="button" className="social-btn facebook">
                  <i className="fab fa-facebook-f"></i>
                  <span>Facebook</span>
                </button>
              </div>
            </form>

            {/* Sign Up Form */}
            <form className="sign-up-form" onSubmit={handleSubmit}>
              <h2 className="title">Create Account</h2>
              <div className="input-field">
                <i className="fas fa-user"></i>
                <input
                  type="text"
                  name="username"
                  placeholder="Username"
                  required
                  value={formData.username}
                  onChange={handleInputChange}
                />
              </div>
              <div className="input-field">
                <i className="fas fa-envelope"></i>
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  required
                  value={formData.email}
                  onChange={handleInputChange}
                />
              </div>
              <div className="input-field">
                <i className="fas fa-lock"></i>
                <input
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Password"
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                />
                <button 
                  type="button" 
                  className="password-toggle"
                  onClick={togglePasswordVisibility}
                  tabIndex={-1}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  <i className={`far ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`}></i>
                </button>
              </div>
              <button type="submit" className="btn">Sign Up</button>
              <div className="divider">
                <div className="line"></div>
                <span>or continue with</span>
                <div className="line"></div>
              </div>
              <div className="social-buttons">
                <button type="button" className="social-btn google">
                  <i className="fab fa-google"></i>
                  <span>Google</span>
                </button>
                <button type="button" className="social-btn facebook">
                  <i className="fab fa-facebook-f"></i>
                  <span>Facebook</span>
                </button>
              </div>
            </form>
          </div>
        </div>

        <div className="panels-container">
          {/* Left Panel - For Sign In */}
          <div className="panel left-panel">
            <div className="content">
              <h3>New here?</h3>
              <p>Join us and start your journey with Samadhan!</p>
              <button className="btn transparent" onClick={() => handleModeSwitch(true)}>
                Sign Up
              </button>
            </div>
            <img src="/signin.svg" className="image" alt="" />
          </div>

          {/* Right Panel - For Sign Up */}
          <div className="panel right-panel">
            <div className="content">
              <h3>Already a member?</h3>
              <p>Sign in to continue your journey with us!</p>
              <button className="btn transparent" onClick={() => handleModeSwitch(false)}>
                Sign In
              </button>
            </div>
            <img src="/signup.svg" className="image" alt="" />
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default LoginSignupForm; 