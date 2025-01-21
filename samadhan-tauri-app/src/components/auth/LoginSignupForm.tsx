import { useState } from 'react';
import { motion } from 'framer-motion';
import '../../styles/login-signup-form.css';
import { invoke } from '@tauri-apps/api/core';

interface ManualLoginResponse {
  success: boolean;
  email: string;
  username: string;
}

interface GoogleLoginResponse {
  email: string;
  username?: string;
}

interface FormData {
  email: string;
  password: string;
  username: string;
}

interface LoginSignupFormProps {
  setUserEmail: (email: string) => void;
  setUsername: (username: string) => void;
  setShowSidebar: (show: boolean) => void;
}

const LoginSignupForm: React.FC<LoginSignupFormProps> = ({ setUserEmail, setUsername, setShowSidebar }) => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
    username: ''
  });
  const [messageType, setMessageType] = useState<'success' | 'error'>('error');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');

    try {
      if (isSignUp) {
        // Handle signup
        await invoke('handle_manual_signup', {
          email: formData.email,
          password: formData.password,
          username: formData.username
        });
        setMessageType('success');
        setErrorMessage('Signup successful! Please login to continue.');
        setTimeout(() => {
          handleModeSwitch(false); // Switch to login mode after 2 seconds
        }, 2000);
      } else {
        // Handle login
        const serial_id = await invoke<string>('get_serial_number');
        const response = await invoke<ManualLoginResponse>('handle_manual_login', {
          email: formData.email,
          password: formData.password,
          serial_id
        });
        
        if (response.success) {
          setUserEmail(response.email);
          setUsername(response.username);
          setShowSidebar(true); // Immediately show sidebar on success, no delay
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setMessageType('error');
      
      if (typeof error === 'object' && error !== null) {
        const errorDetail = (error as any).detail;
        if (errorDetail === 'LOGIN_FAILED') {
          setErrorMessage('Incorrect email or password. Please try again.');
        } else if (errorDetail === 'Incorrect email or password') {
          setErrorMessage('Incorrect email or password. Please try again.');
        } else if (errorDetail === 'Email already registered') {
          setErrorMessage('This email is already registered. Please try logging in instead.');
        } else {
          setErrorMessage('An error occurred. Please try again later.');
        }
      } else {
        setErrorMessage('An error occurred. Please try again later.');
      }
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setErrorMessage(''); // Clear error when user types
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleModeSwitch = (mode: boolean) => {
    setIsSignUp(mode);
    setShowPassword(false);
    setErrorMessage('');
    setFormData({
      email: '',
      password: '',
      username: ''
    });
  };

  const handleGoogleLogin = async () => {
    try {
      const serial_id = await invoke<string>('get_serial_number');
      const response = await invoke<GoogleLoginResponse>('handle_google_login', { 
        serialId: serial_id
      });
      
      if (response.email) {
        setUserEmail(response.email);
        setUsername(response.username || '');
        setShowSidebar(true);
      }
    } catch (error) {
      console.error('Google login error:', error);
      setMessageType('error');
      
      if (typeof error === 'object' && error !== null) {
        const errorDetail = (error as any).detail;
        if (errorDetail === 'GOOGLE_USER_NOT_FOUND') {
          setErrorMessage('No account found with this Google account. Please sign up first.');
        } else {
          setErrorMessage('Failed to login with Google. Please try again.');
        }
      } else {
        setErrorMessage('Failed to login with Google. Please try again.');
      }
    }
  };

  const handleGoogleSignup = async () => {
    try {
      const serial_id = await invoke<string>('get_serial_number');
      const response = await invoke<GoogleLoginResponse>('handle_google_signup', { 
        serialId: serial_id
      });
      
      if (response.email) {
        setMessageType('success');
        setUserEmail(response.email);
        setUsername(response.username || '');
        setShowSidebar(true);
      }
    } catch (error) {
      console.error('Google signup error:', error);
      setMessageType('error');
      
      if (typeof error === 'object' && error !== null) {
        const errorDetail = (error as any).detail;
        if (errorDetail === 'GOOGLE_USER_EXISTS') {
          setErrorMessage('An account with this Google email already exists. Please login instead.');
        } else {
          setErrorMessage('Failed to sign up with Google. Please try again.');
        }
      } else {
        setErrorMessage('Failed to sign up with Google. Please try again.');
      }
    }
  };

  const handleGoogleButtonClick = () => {
    if (isSignUp) {
      handleGoogleSignup();
    } else {
      handleGoogleLogin();
    }
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
              {errorMessage && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`message-box ${messageType === 'success' ? 'success-message' : 'error-message'}`}
                >
                  {errorMessage}
                </motion.div>
              )}
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
              <div className="forgot-password">
                <a href="#">Forgot Password?</a>
              </div>
              <button type="submit" className="btn">
                {isSignUp ? 'Sign Up' : 'Login'}
              </button>
              <div className="divider">
                <div className="line"></div>
                <span>or continue with</span>
                <div className="line"></div>
              </div>
              <div className="social-buttons">
                <button 
                  type="button" 
                  className="social-btn google"
                  onClick={handleGoogleButtonClick}
                >
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
              {errorMessage && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`message-box ${messageType === 'success' ? 'success-message' : 'error-message'}`}
                >
                  {errorMessage}
                </motion.div>
              )}
              <div className="input-field">
                <i className="fas fa-user"></i>
                <input
                  type="text"
                  name="username"
                  placeholder="Full Name"
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
              <button type="submit" className="btn">
                {isSignUp ? 'Sign Up' : 'Login'}
              </button>
              <div className="divider">
                <div className="line"></div>
                <span>or continue with</span>
                <div className="line"></div>
              </div>
              <div className="social-buttons">
                <button 
                  type="button" 
                  className="social-btn google"
                  onClick={handleGoogleButtonClick}
                >
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