import React, { useState } from 'react';
import { motion } from 'framer-motion';

const Settings: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [emailNotifications, setEmailNotifications] = useState(false);
  const [generalNotifications, setGeneralNotifications] = useState(false);
  const [emailFrequency, setEmailFrequency] = useState('daily');
  const [focusMode, setFocusMode] = useState(false);
  const [showFrequencyOptions, setShowFrequencyOptions] = useState(false);

  // Example current values
  const currentUsername = "JohnDoe";
  const currentEmail = "john.doe@example.com";

  const toggleDarkMode = () => setDarkMode(!darkMode);
  const toggleEmailNotifications = () => setEmailNotifications(!emailNotifications);
  const toggleGeneralNotifications = () => setGeneralNotifications(!generalNotifications);
  const toggleFocusMode = () => setFocusMode(!focusMode);

  const toggleButton = (isActive: boolean, toggleFunction: () => void) => (
    <button
      onClick={toggleFunction}
      className={`w-10 h-5 flex items-center rounded-full p-1 transition-colors duration-300 ${isActive ? 'bg-indigo-600' : 'bg-gray-300'}`}
    >
      <div
        className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300 ${isActive ? 'translate-x-5' : ''}`}
      />
    </button>
  );

  const infoRow = (label: string, value: string) => (
    <div className="flex items-center justify-between">
      <span className="text-gray-700">{label}</span>
      <div className="flex items-center">
        <span className="text-gray-500 mr-2">{value}</span>
        <button className="text-gray-500">{'>'}</button>
      </div>
    </div>
  );

  const frequencyOptions = {
    daily: 'Daily',
    weekly: 'Weekly'
  };

  return (
    <motion.div
      className="h-full flex flex-col bg-[#fafafa] pt-2 px-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <div className="bg-white rounded-lg shadow-md p-5">
        <h2 className="text-xl font-semibold text-gray-900 mb-1">Settings</h2>
        <p className="text-sm text-gray-500 mb-4">Manage your application settings and preferences.</p>
        
        <div className="space-y-5">
          {/* Profile Settings */}
          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-2">Profile Settings</h3>
            {infoRow("Username", currentUsername)}
          </div>

          {/* Password Settings */}
          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-2">Password Settings</h3>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Change Password</span>
              <button className="text-indigo-600 hover:text-indigo-700 font-medium">
                Change
              </button>
            </div>
          </div>

          {/* Email Settings */}
          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-2">Email Settings</h3>
            {infoRow("Email Address", currentEmail)}
            <div className="flex items-center justify-between mt-2">
              <span className="text-gray-700">Email Notifications</span>
              {toggleButton(emailNotifications, toggleEmailNotifications)}
            </div>
            <div className="flex items-center justify-between mt-2 relative">
              <span className="text-gray-700">Email Frequency</span>
              <div className="relative">
                <button
                  onClick={() => setShowFrequencyOptions(!showFrequencyOptions)}
                  className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  {frequencyOptions[emailFrequency as keyof typeof frequencyOptions]}
                  <svg 
                    className={`w-4 h-4 transition-transform duration-200 ${showFrequencyOptions ? 'rotate-180' : ''}`}
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2"
                  >
                    <path d="M6 9l6 6 6-6" />
                  </svg>
                </button>
                
                {showFrequencyOptions && (
                  <motion.div 
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 mt-1 py-1 bg-white rounded-md shadow-lg border border-gray-100 min-w-[100px] z-10"
                  >
                    {Object.entries(frequencyOptions).map(([value, label]) => (
                      <button
                        key={value}
                        onClick={() => {
                          setEmailFrequency(value);
                          setShowFrequencyOptions(false);
                        }}
                        className={`w-full px-3 py-1.5 text-left hover:bg-gray-50 ${
                          emailFrequency === value ? 'text-indigo-600' : 'text-gray-600'
                        }`}
                      >
                        {label}
                      </button>
                    ))}
                  </motion.div>
                )}
              </div>
            </div>
          </div>

          {/* General Settings */}
          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-2">General Settings</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-gray-700">Dark Mode</span>
                {toggleButton(darkMode, toggleDarkMode)}
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-700">Notifications</span>
                {toggleButton(generalNotifications, toggleGeneralNotifications)}
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-700">Focus Mode</span>
                {toggleButton(focusMode, toggleFocusMode)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default Settings; 