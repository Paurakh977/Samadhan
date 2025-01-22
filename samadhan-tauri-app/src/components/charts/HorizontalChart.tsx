import React, { useState, useEffect } from 'react';
import { Settings } from 'lucide-react';
import { motion } from 'framer-motion';
import { invoke } from '@tauri-apps/api/core';
import '../../styles/horizontal-chart.css';
import UltraModernDropdown from '../UltraModernDropdown';

interface Props {
  email: string;
}

interface AppUsageData {
  tab_name: string;
  used_time: string | number;
  percentage: number;
  logo_url?: string;
}

const HorizontalChart: React.FC<Props> = ({ email }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [totalTime, setTotalTime] = useState(0);
  const [appData, setAppData] = useState<AppUsageData[]>([]);
  const [comparisonText, setComparisonText] = useState('');
  const [error, setError] = useState<string | null>(null);

  // Cache key for sessionStorage
  const CACHE_KEY = `app_usage_${email}`;

  useEffect(() => {
    const fetchData = async () => {
      if (!email) {
        console.error('No email provided to HorizontalChart');
        setError('No email provided');
        setIsLoading(false);
        return;
      }
      
      console.log('HorizontalChart: Fetching data for email:', email);
      setError(null);

      // Try to get cached data first
      const cachedData = sessionStorage.getItem(CACHE_KEY);
      if (cachedData) {
        console.log('HorizontalChart: Found cached data');
        try {
          const { apps, total, comparison } = JSON.parse(cachedData);
          setAppData(apps);
          setTotalTime(total);
          setComparisonText(comparison);
          setIsLoading(false);
          return;
        } catch (e) {
          console.error('HorizontalChart: Error parsing cached data:', e);
          sessionStorage.removeItem(CACHE_KEY);
        }
      }
      
      try {
        console.log('HorizontalChart: Making API request...');
        const response = await invoke<{
          success: boolean;
          data?: {
            data: {
              apps: AppUsageData[];
              total_time: string;
              comparison: string;
            };
            success: boolean;
          };
          error?: string;
        }>('fetch_app_usage_info', { email });

        console.log('HorizontalChart: Raw API Response:', JSON.stringify(response, null, 2));

        if (response.success && response.data?.data) {
          const { apps, total_time, comparison } = response.data.data;
          
          console.log('HorizontalChart: Setting data:', {
            apps,
            total: total_time,
            comparison
          });
          
          if (!Array.isArray(apps)) {
            console.error('HorizontalChart: apps data is not an array:', apps);
            setError('Invalid data format');
            setIsLoading(false);
            return;
          }

          // Process the apps data
          const processedApps = apps.map(app => ({
            ...app,
            used_time: typeof app.used_time === 'string' ? parseInt(app.used_time, 10) : app.used_time
          }));

          setAppData(processedApps);
          const totalTimeNum = parseInt(total_time, 10);
          setTotalTime(totalTimeNum);
          setComparisonText(comparison);

          // Cache the processed data
          sessionStorage.setItem(CACHE_KEY, JSON.stringify({
            apps: processedApps,
            total: totalTimeNum,
            comparison
          }));
        } else if (response.error) {
          console.error('HorizontalChart: Error from API:', response.error);
          setError(response.error);
        } else {
          console.error('HorizontalChart: No data in response');
          setError('No data available');
        }
      } catch (error) {
        console.error('HorizontalChart: Error fetching app usage data:', error);
        setError('Failed to fetch data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [email]);

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: "easeOut",
        staggerChildren: 0.15
      }
    }
  };

  const timeVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.4, ease: "easeOut" }
    }
  };

  const progressVariants = {
    hidden: { scaleX: 0 },
    visible: {
      scaleX: 1,
      transition: { 
        duration: 1,
        ease: [0.165, 0.84, 0.44, 1],
        delay: 0.2
      }
    }
  };

  const appItemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.4, ease: "easeOut" }
    }
  };

  const formatTime = (minutes: string | number): string => {
    const mins = typeof minutes === 'string' ? parseInt(minutes, 10) : minutes;
    const hours = Math.floor(mins / 60);
    const remainingMins = mins % 60;
    if (hours === 0) {
      return `${remainingMins}m`;
    }
    if (remainingMins === 0) {
      return `${hours}h`;
    }
    return `${hours}h ${remainingMins}m`;
  };

  // Show error state
  if (error) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-red-500">
        <p>Error: {error}</p>
      </div>
    );
  }

  // Loading skeleton
  if (isLoading) {
    return (
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="h-full flex flex-col animate-pulse"
      >
        <div className="mb-3">
          <div className="h-8 bg-gray-200 rounded-lg w-32 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-40"></div>
        </div>
        <div className="h-3 bg-gray-200 rounded-full mb-4"></div>
        <div className="space-y-2.5 flex-1">
          {[1, 2, 3].map((_, i) => (
            <div key={i} className="flex items-center justify-between p-2">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 bg-gray-200 rounded-xl"></div>
                <div className="h-4 bg-gray-200 rounded w-20"></div>
              </div>
              <div className="h-4 bg-gray-200 rounded w-12"></div>
            </div>
          ))}
        </div>
      </motion.div>
    );
  }

  // Show empty state if no data
  if (!appData || appData.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-gray-500">
        <p>No app usage data available</p>
      </div>
    );
  }

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="h-full flex flex-col"
    >
      {/* Time Display with Dropdown */}
      <motion.div variants={timeVariants} className="mb-3 flex items-center justify-between">
        <div>
          <motion.h1 
            className="text-[22px] font-semibold tracking-tight text-gray-900"
            layoutId="timeDisplay"
          >
            {formatTime(totalTime)}
          </motion.h1>
          <motion.p 
            className="text-gray-500 text-xs font-medium"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            {comparisonText}
          </motion.p>
        </div>
        <UltraModernDropdown />
      </motion.div>

      {/* Enhanced 3D Progress Bar */}
      <div className="relative h-3 bg-blue-50/80 backdrop-blur-xl rounded-full progress-bar-3d mb-4">
        <div className="absolute inset-0 flex overflow-hidden rounded-full">
          {appData.map((app, index) => (
          <motion.div 
              key={index}
            variants={progressVariants}
              style={{ width: `${app.percentage}%` }} 
              className={`progress-segment bg-gradient-to-r ${
                index === 0 ? 'from-[#1E3A8A] via-[#1E40AF] to-[#2563EB] rounded-l-full' :
                index === 1 ? 'from-[#3B82F6] via-[#60A5FA] to-[#93C5FD]' :
                'from-[#60A5FA] via-[#93C5FD] to-[#BFDBFE] rounded-r-full'
              }`}
            />
          ))}
        </div>
        <div className="absolute inset-0 w-full h-full rounded-full opacity-60 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.9),rgba(255,255,255,0))]" />
      </div>

      {/* App List */}
      <div className="space-y-2.5 flex-1">
        {appData.map((app, index) => (
        <motion.div 
            key={index}
          variants={appItemVariants}
          whileHover={{ x: 4 }}
          className="flex items-center justify-between group hover:bg-blue-50/80 p-2 rounded-xl transition-all duration-300"
        >
          <div className="flex items-center gap-3">
            <motion.div 
              whileHover={{ scale: 1.05 }}
                className={`w-9 h-9 ${
                  index === 0 ? 'bg-[#1E293B]' :
                  index === 1 ? 'bg-white border border-blue-100' :
                  'bg-gradient-to-br from-[#1E293B] to-[#334155]'
                } rounded-xl flex items-center justify-center shadow-[0_4px_8px_rgba(0,0,0,0.1)] transform group-hover:scale-105 transition-transform duration-300`}
              >
                {app.logo_url ? (
                  <img 
                    src={app.logo_url}
                    alt={app.tab_name}
                className="w-5 h-5 object-contain"
                    onError={(e) => {
                      // Fallback icon if image fails to load
                      e.currentTarget.src = "https://images.unsplash.com/photo-1611605698335-8b1569810432?auto=format&fit=crop&q=80&w=100&h=100";
                    }}
                  />
                ) : (
              <Settings className="w-4 h-4 text-white" />
                )}
            </motion.div>
              <span className="font-medium text-[#1E293B] text-sm tracking-tight">{app.tab_name}</span>
          </div>
          <div className="flex items-center gap-2">
            <motion.span 
              whileHover={{ color: "#2563EB" }}
              className="text-[#64748B] font-medium group-hover:text-[#2563EB] transition-colors duration-300 text-sm"
            >
                {formatTime(app.used_time as number)}
            </motion.span>
            <motion.div 
              whileHover={{ scale: 1.2 }}
                className={`w-2 h-2 rounded-full bg-gradient-to-r ${
                  index === 0 ? 'from-[#1E3A8A] to-[#2563EB]' :
                  index === 1 ? 'from-[#3B82F6] to-[#93C5FD]' :
                  'from-[#60A5FA] to-[#BFDBFE]'
                } shadow-[0_2px_4px_rgba(37,99,235,0.3)]`}
            />
          </div>
        </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default HorizontalChart; 