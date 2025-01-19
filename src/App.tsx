import React, { useState } from 'react';
import { motion } from 'framer-motion';
import AppUsageLineChart from './AppUsageLineChart';

const App = () => {
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(false);

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <motion.div
        className={`fixed left-0 top-0 h-full bg-indigo-600 text-white z-50 ${
          isSidebarExpanded ? 'w-[240px]' : 'w-[78px]'
        }`}
        animate={{ width: isSidebarExpanded ? 240 : 78 }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
      >
        {/* Sidebar content */}
      </motion.div>

      {/* Main content */}
      <motion.div
        className="flex-1 relative"
        animate={{ 
          marginLeft: isSidebarExpanded ? '240px' : '78px',
        }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
      >
        <div className="absolute inset-0 overflow-auto">
          <div className="min-h-full p-8">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h1 className="text-2xl font-semibold text-slate-900">App Usage Analytics</h1>
                <p className="mt-1 text-slate-500">Track and analyze your application usage patterns</p>
              </div>
              <select className="w-full sm:w-auto px-3 py-2 bg-white border border-slate-200 rounded-lg text-slate-600 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option>Last week</option>
              </select>
            </div>

            {/* Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column */}
              <div className="bg-white rounded-2xl p-6 shadow-sm shadow-slate-200/50 h-[calc(100vh-12rem)]">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900">Top Applications</h2>
                  <p className="text-sm text-slate-500 mt-1">Most used apps this week</p>
                </div>
                <div className="mt-6 h-[calc(100%-5rem)] overflow-auto">
                  {/* Add your top applications content */}
                </div>
              </div>

              {/* Right Column (Spans 2 columns) */}
              <div className="lg:col-span-2 bg-white rounded-2xl p-6 shadow-sm shadow-slate-200/50 h-[calc(100vh-12rem)]">
                <AppUsageLineChart data={appUsageData} />
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default App; 