import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { invoke } from '@tauri-apps/api/core';

interface ActivityData {
  hour: number;
  social: number;
  entertainment: number;
  productivity: number;
  other: number;
}

const generateRandomData = (): ActivityData[] => {
  return Array.from({ length: 24 }, (_, i) => ({
    hour: i,
    social: Math.random() * 0.3,
    entertainment: Math.random() * 0.25,
    productivity: Math.random() * 0.2,
    other: Math.random() * 0.15,
  }));
};

const formatTime = (minutes: number): string => {
  const hours = Math.floor(minutes / 60);
  const mins = Math.floor(minutes % 60);
  if (hours === 0) {
    return `${mins}m`;
  }
  if (mins === 0) {
    return `${hours}h`;
  }
  return `${hours}h ${mins}m`;
};

const formatHour = (hour: number): string => {
  if (hour === 0) return '12a';
  if (hour === 12) return '12p';
  return hour < 12 ? `${hour}a` : `${hour - 12}p`;
};

const containerVariants = {
  hidden: { 
    opacity: 0,
    y: 20,
    scale: 0.95
  },
  visible: { 
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      duration: 0.6,
      ease: [0.22, 1, 0.36, 1],
      staggerChildren: 0.15,
      delayChildren: 0.3,
      when: "beforeChildren"
    }
  }
};

const itemVariants = {
  hidden: { 
    opacity: 0,
    y: 10,
    scale: 0.95
  },
  visible: { 
    opacity: 1, 
    y: 0,
    scale: 1,
    transition: {
      duration: 0.5,
      ease: [0.22, 1, 0.36, 1]
    }
  }
};

const barVariants = {
  hidden: { 
    scaleY: 0,
    opacity: 0
  },
  visible: (custom: number) => ({
    scaleY: 1,
    opacity: 1,
    transition: {
      delay: 0.8 + (custom * 0.03),
      duration: 0.6,
      ease: [0.22, 1, 0.36, 1]
    }
  })
};

const legendVariants = {
  hidden: { 
    opacity: 0,
    y: 15
  },
  visible: { 
    opacity: 1,
    y: 0,
    transition: {
      delay: 1.2,
      duration: 0.4,
      ease: [0.22, 1, 0.36, 1]
    }
  }
};

const DailyActivityChart: React.FC<{ email: string }> = ({ email }) => {
  const [data, setData] = useState<ActivityData[]>(Array.from({ length: 24 }, (_, i) => ({
    hour: i,
    social: 0,
    entertainment: 0,
    productivity: 0,
    other: 0
  })));
  const [isLoading, setIsLoading] = useState(true);
  const [totalTime, setTotalTime] = useState(0);
  const [categoryTotals, setCategoryTotals] = useState({
    social: 0,
    entertainment: 0,
    productivity: 0,
    other: 0
  });

  // Cache key for sessionStorage
  const CACHE_KEY = `activity_data_${email}`;

  useEffect(() => {
    const fetchData = async () => {
      if (!email) return;
      
      // Try to get cached data first
      const cachedData = sessionStorage.getItem(CACHE_KEY);
      if (cachedData) {
        const cached = JSON.parse(cachedData);
        // Use cached data immediately while fetching fresh data
        processRawData(cached);
        setIsLoading(false);
      }

      try {
        // Then fetch categorized data
        const response = await invoke<{
          success: boolean;
          data?: {
            'Social Networking': { [key: string]: number };
            'Entertainment': { [key: string]: number };
            'Productivity': { [key: string]: number };
            'Others': { [key: string]: number };
          };
          error?: string;
        }>('fetch_activity_data', { email });

        if (response.success && response.data) {
          // Cache the new data
          sessionStorage.setItem(CACHE_KEY, JSON.stringify(response.data));
          processRawData(response.data);
        }
      } catch (error) {
        console.error('Error fetching activity data:', error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, [email]);

  // Separate data processing function
  const processRawData = (rawData: any) => {
    const maxMinutes = Math.max(
      ...Object.values(rawData).flatMap(category => 
        Object.values(category as {[key: string]: number}).map(minutes => minutes || 0)
      )
    );

    const normalizer = Math.max(maxMinutes, 60);
    
    const processedData = Array.from({ length: 24 }, (_, hour) => {
      const hourStr = hour.toString();
      return {
        hour,
        social: Math.max(0, ((rawData['Social Networking']?.[hourStr] || 0) / normalizer) * 0.7),
        entertainment: Math.max(0, ((rawData['Entertainment']?.[hourStr] || 0) / normalizer) * 0.7),
        productivity: Math.max(0, ((rawData['Productivity']?.[hourStr] || 0) / normalizer) * 0.7),
        other: Math.max(0, ((rawData['Others']?.[hourStr] || 0) / normalizer) * 0.7)
      };
    });

    const social = Math.floor(Object.values(rawData['Social Networking'] || {}).map(v => Number(v)).reduce((sum, val) => sum + (val || 0), 0));
    const entertainment = Math.floor(Object.values(rawData['Entertainment'] || {}).map(v => Number(v)).reduce((sum, val) => sum + (val || 0), 0));
    const productivity = Math.floor(Object.values(rawData['Productivity'] || {}).map(v => Number(v)).reduce((sum, val) => sum + (val || 0), 0));
    const other = Math.floor(Object.values(rawData['Others'] || {}).map(v => Number(v)).reduce((sum, val) => sum + (val || 0), 0));

    setData(processedData);
    setCategoryTotals({
      social,
      entertainment,
      productivity,
      other
    });
    setTotalTime(social + entertainment + productivity + other);
  };

  // Loading skeleton component
  if (isLoading && !data.some(d => d.social || d.entertainment || d.productivity || d.other)) {
    return (
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="flex-1 min-h-[480px] bg-white rounded-[28px] shadow-[0_12px_36px_-12px_rgba(0,0,0,0.06)] border border-[#f5f5f5] p-6"
      >
        <div className="flex flex-col h-full animate-pulse">
          <div className="h-12 bg-gray-200 rounded-lg w-32 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-24 mb-8"></div>
          
          <div className="flex-1 flex items-end gap-[2px]">
            {Array.from({ length: 24 }).map((_, i) => (
              <div key={i} className="flex-1 flex flex-col items-center">
                <div className="w-full bg-gray-200 rounded-t" style={{ height: `${Math.random() * 100 + 20}px` }}></div>
                <div className="h-2 w-4 bg-gray-200 rounded mt-2"></div>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-2 gap-4 mt-6">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="flex items-center">
                <div className="h-4 bg-gray-200 rounded w-24"></div>
                <div className="h-4 bg-gray-200 rounded w-12 ml-2"></div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="flex-1 min-h-[480px] bg-white rounded-[28px] shadow-[0_12px_36px_-12px_rgba(0,0,0,0.06)] border border-[#f5f5f5] p-6"
    >
      <div className="flex flex-col h-full">
        <motion.div 
          variants={itemVariants} 
          className="flex justify-between items-start mb-8"
        >
          <div>
            <motion.div 
              variants={itemVariants}
              className="text-5xl font-bold text-gray-900 tracking-tight mb-1"
            >
              {formatTime(totalTime)}
            </motion.div>
            <motion.div 
              variants={itemVariants}
              className="flex items-center text-[#40B7FF] font-medium"
            >
              <svg className="w-4 h-4 mr-1 transform -translate-y-[1px]" viewBox="0 0 20 20" fill="currentColor">
                <path d="M5 10l5-5 5 5H5z" />
              </svg>
              <span className="text-base">42m above average</span>
            </motion.div>
          </div>
        </motion.div>

        <div className="flex-1 flex flex-col">
          <motion.div 
            variants={itemVariants}
            className="grid grid-cols-4 mb-3"
          >
            <div className="text-gray-300 text-xs font-medium tracking-wide">12A</div>
            <div className="text-gray-300 text-xs font-medium tracking-wide">6A</div>
            <div className="text-gray-300 text-xs font-medium tracking-wide">12P</div>
            <div className="text-gray-300 text-xs font-medium tracking-wide">6P</div>
          </motion.div>

          <motion.div 
            variants={itemVariants}
            className="flex-1 relative"
          >
            <div className="absolute inset-0">
              <div className="h-full w-full grid grid-cols-4">
                <div className="border-r border-gray-50"></div>
                <div className="border-r border-gray-50"></div>
                <div className="border-r border-gray-50"></div>
                <div></div>
              </div>
            </div>

            <div className="relative h-full flex items-end" style={{ gap: '2px' }}>
              {data.map((hour, index) => (
                <div key={index} className="group flex-1 flex flex-col justify-end min-w-0">
                  <div className="relative origin-bottom">
                    {hour.other > 0 && (
                      <motion.div 
                        custom={index}
                        variants={barVariants}
                        style={{ height: `${hour.other * 280}px` }}
                        className="overflow-hidden rounded-t-[3px]"
                      >
                        <div className="w-full h-full bg-[#E5E7EB] transition-all duration-300 group-hover:opacity-90 group-hover:filter group-hover:brightness-95" />
                      </motion.div>
                    )}
                    {hour.productivity > 0 && !hour.other && (
                      <motion.div 
                        custom={index}
                        variants={barVariants}
                        style={{ height: `${hour.productivity * 280}px` }}
                        className="overflow-hidden rounded-t-[3px]"
                      >
                        <div className="w-full h-full bg-[#ff9f40] transition-all duration-300 group-hover:opacity-90 group-hover:filter group-hover:brightness-95" />
                      </motion.div>
                    )}
                    {hour.entertainment > 0 && !hour.other && !hour.productivity && (
                      <motion.div 
                        custom={index}
                        variants={barVariants}
                        style={{ height: `${hour.entertainment * 280}px` }}
                        className="overflow-hidden rounded-t-[3px]"
                      >
                        <div className="w-full h-full bg-[#40b7ff] transition-all duration-300 group-hover:opacity-90 group-hover:filter group-hover:brightness-95" />
                      </motion.div>
                    )}
                    {hour.social > 0 && !hour.other && !hour.productivity && !hour.entertainment && (
                      <motion.div 
                        custom={index}
                        variants={barVariants}
                        style={{ height: `${hour.social * 280}px` }}
                        className="overflow-hidden rounded-t-[3px]"
                      >
                        <div className="w-full h-full bg-[#0066ff] transition-all duration-300 group-hover:opacity-90 group-hover:filter group-hover:brightness-95" />
                      </motion.div>
                    )}
                    {/* Non-rounded sections with animations */}
                    {hour.productivity > 0 && hour.other && (
                      <motion.div 
                        custom={index}
                        variants={barVariants}
                        style={{ height: `${hour.productivity * 280}px` }}
                      >
                        <div className="w-full h-full bg-[#ff9f40] transition-all duration-300 group-hover:opacity-90 group-hover:filter group-hover:brightness-95" />
                      </motion.div>
                    )}
                    {hour.entertainment > 0 && (hour.other || hour.productivity) && (
                      <motion.div 
                        custom={index}
                        variants={barVariants}
                        style={{ height: `${hour.entertainment * 280}px` }}
                      >
                        <div className="w-full h-full bg-[#40b7ff] transition-all duration-300 group-hover:opacity-90 group-hover:filter group-hover:brightness-95" />
                      </motion.div>
                    )}
                    {hour.social > 0 && (hour.other || hour.productivity || hour.entertainment) && (
                      <motion.div 
                        custom={index}
                        variants={barVariants}
                        style={{ height: `${hour.social * 280}px` }}
                      >
                        <div className="w-full h-full bg-[#0066ff] transition-all duration-300 group-hover:opacity-90 group-hover:filter group-hover:brightness-95" />
                      </motion.div>
                    )}
                  </div>
                  <motion.div 
                    variants={itemVariants}
                    className="text-[10px] text-gray-400 text-center mt-2 font-medium tracking-wide transition-colors duration-200 group-hover:text-gray-600"
                  >
                    {formatHour(hour.hour)}
                  </motion.div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        <motion.div 
          variants={legendVariants}
          className="grid grid-cols-2 gap-x-8 gap-y-2 mt-6"
        >
          <motion.div variants={itemVariants} className="flex items-center group">
            <span className="text-sm font-medium text-[#0066ff] mr-2 transition-colors duration-200 group-hover:text-[#0052cc]">Social Networking</span>
            <span className="text-sm text-gray-500 transition-colors duration-200 group-hover:text-gray-700">{formatTime(categoryTotals.social)}</span>
          </motion.div>
          <motion.div variants={itemVariants} className="flex items-center group">
            <span className="text-sm font-medium text-[#40b7ff] mr-2 transition-colors duration-200 group-hover:text-[#2e8bc0]">Entertainment</span>
            <span className="text-sm text-gray-500 transition-colors duration-200 group-hover:text-gray-700">{formatTime(categoryTotals.entertainment)}</span>
          </motion.div>
          <motion.div variants={itemVariants} className="flex items-center group">
            <span className="text-sm font-medium text-[#ff9f40] mr-2 transition-colors duration-200 group-hover:text-[#e68a2e]">Productivity</span>
            <span className="text-sm text-gray-500 transition-colors duration-200 group-hover:text-gray-700">{formatTime(categoryTotals.productivity)}</span>
          </motion.div>
          <motion.div variants={itemVariants} className="flex items-center group">
            <span className="text-sm font-medium text-[#9CA3AF] mr-2 transition-colors duration-200 group-hover:text-[#6B7280]">Other</span>
            <span className="text-sm text-gray-500 transition-colors duration-200 group-hover:text-gray-700">{formatTime(categoryTotals.other)}</span>
          </motion.div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default DailyActivityChart; 