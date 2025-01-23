import React, { useState } from 'react';
import { motion } from 'framer-motion';

const Settings: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [emailNotifications, setEmailNotifications] = useState(false);
  const [generalNotifications, setGeneralNotifications] = useState(false);
  const [emailFrequency, setEmailFrequency] = useState('daily');
  const [focusMode, setFocusMode] = useState(false);

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

  return (
    <motion.div
      className="h-screen flex flex-col bg-[#fafafa] p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <div className="bg-white rounded-lg shadow-md p-6 space-y-8 overflow-y-auto" style={{ maxHeight: 'calc(100vh - 3rem)' }}>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Settings</h2>
        <p className="text-sm text-gray-500 mb-6">Manage your application settings and preferences.</p>
        
        {/* Profile Settings */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-800">Profile Settings</h3>
          {infoRow("Username", currentUsername)}
        </div>

        {/* Password Settings */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-800">Password Settings</h3>
          <div className="flex items-center justify-between">
            <span className="text-gray-700">Change Password</span>
            <button className="btn">Change</button>
          </div>
        </div>

        {/* Email Settings */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-800">Email Settings</h3>
          {infoRow("Email Address", currentEmail)}
          <div className="flex items-center justify-between">
            <span className="text-gray-700">Email Notifications</span>
            {toggleButton(emailNotifications, toggleEmailNotifications)}
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-700">Email Frequency</span>
            <select
              value={emailFrequency}
              onChange={(e) => setEmailFrequency(e.target.value)}
              className="border border-gray-300 rounded-md p-1 text-gray-700"
            >
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
            </select>
          </div>
        </div>

        {/* General Settings */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-gray-800">General Settings</h3>
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
    </motion.div>
  );
};

export default Settings; 