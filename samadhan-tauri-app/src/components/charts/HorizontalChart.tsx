import React, { useState, useEffect } from 'react';
import { Settings } from 'lucide-react';
import { motion, useInView, AnimatePresence } from 'framer-motion';
import { invoke } from '@tauri-apps/api/core';
import '../../styles/horizontal-chart.css';
import UltraModernDropdown from '../UltraModernDropdown';

interface Props {
  email: string;
}

interface AppUsageData {
  name: string;
  used_time: number;
  percentage?: number;
  logo_url?: string;
}

interface PeriodData {
  apps: AppUsageData[];
  total_time: number;
}

interface BackendData {
  today: PeriodData;
  yesterday: PeriodData;
  this_week: PeriodData;
}

interface BackendResponse {
  success: boolean;
  data: {
    data: BackendData;
  };
  error?: string;
}

const HorizontalChart: React.FC<Props> = ({ email }) => {
  const ref = React.useRef(null);
  const isInView = useInView(ref, {
    once: true,
    amount: 0.5
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<'today' | 'yesterday' | 'this_week'>('today');
  const [cachedData, setCachedData] = useState<BackendData | null>(null);
  const [totalTime, setTotalTime] = useState(0);
  const [appData, setAppData] = useState<AppUsageData[]>([]);
  const [comparisonText, setComparisonText] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching data for email:', email);
        setIsLoading(true);
        setError(null);

        // Check if we have cached data
        const cachedDataStr = sessionStorage.getItem(`app_usage_all_${email}`);
        let responseData;

        if (cachedDataStr) {
          console.log('Found cached data');
          responseData = JSON.parse(cachedDataStr);
        } else {
          console.log('Fetching fresh data from backend');
          const response = await invoke<any>('fetch_all_app_usage', { email });
          console.log('Backend response:', response);
          
          if (!response.success) {
            throw new Error(response.error || 'Failed to fetch data');
          }

          responseData = response;
          sessionStorage.setItem(`app_usage_all_${email}`, JSON.stringify(responseData));
        }

        const data = responseData.data.data;
        console.log('Extracted data:', data);

        const emptyData = { apps: [], total_time: 0 };
        const periodData = data[selectedPeriod] || emptyData;
        console.log(`Setting data for ${selectedPeriod}:`, periodData);
        
        setCachedData(data);
        setTotalTime(periodData.total_time || 0);
        
        // Process and set app data with percentages (top 5 only)
        const apps = periodData.apps
          .map((app: AppUsageData) => ({
            name: app.name,
            used_time: app.used_time,
            logo_url: app.logo_url
          }))
          .sort((a: AppUsageData, b: AppUsageData) => b.used_time - a.used_time)
          .slice(0, 5); // Take top 5 apps
        
        console.log('Processed app data:', apps);
        setAppData(apps);

        // Set comparison text
        if (selectedPeriod === 'today') {
          const yesterdayTotal = data.yesterday?.total_time || 0;
          const diff = periodData.total_time - yesterdayTotal;
          const diffMinutes = Math.abs(Math.floor(diff / 60));
          setComparisonText(
            diff > 0 
              ? `${Math.floor(diffMinutes / 60)}h ${diffMinutes % 60}m more than yesterday`
              : `${Math.floor(diffMinutes / 60)}h ${diffMinutes % 60}m less than yesterday`
          );
        } else if (selectedPeriod === 'yesterday') {
          setComparisonText('Compared to the day before');
        } else {
          setComparisonText('Weekly usage summary');
        }

      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [email, selectedPeriod]);

  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours === 0) return `${minutes}m`;
    if (minutes === 0) return `${hours}h`;
    return `${hours}h ${minutes}m`;
  };

  if (!isInView) return <div ref={ref} className="h-full" />;

  if (isLoading) {
    return (
      <div ref={ref} className="h-full flex flex-col animate-pulse">
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
      </div>
    );
  }

  if (error) {
    return (
      <div ref={ref} className="h-full flex items-center justify-center text-red-500">
        {error}
      </div>
    );
  }

  return (
    <div ref={ref} className="h-full flex flex-col">
      {/* Time Display with Dropdown */}
      <div className="mb-3 flex items-center justify-between">
        <div>
          <AnimatePresence mode="wait">
            <motion.h1 
              key={totalTime}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="text-[22px] font-semibold tracking-tight text-gray-900"
            >
              {formatTime(totalTime)}
            </motion.h1>
          </AnimatePresence>
          <AnimatePresence mode="wait">
            <motion.p 
              key={comparisonText}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="text-gray-500 text-xs font-medium"
            >
              {comparisonText}
            </motion.p>
          </AnimatePresence>
        </div>
        <UltraModernDropdown 
          value={selectedPeriod}
          onChange={(value) => setSelectedPeriod(value as 'today' | 'yesterday' | 'this_week')}
        />
      </div>

      {/* Enhanced 3D Progress Bar */}
      <div className="relative h-5 bg-blue-50/80 backdrop-blur-xl rounded-full progress-bar-3d mb-4">
        <AnimatePresence mode="wait">
          <motion.div 
            key={selectedPeriod + totalTime}
            initial={{ width: 0 }}
            animate={{ 
              width: `${(() => {
                const dailyLimitInSeconds = 7 * 60 * 60;
                const weeklyLimitInSeconds = 45 * 60 * 60;
                const maxSeconds = selectedPeriod === 'this_week' ? weeklyLimitInSeconds : dailyLimitInSeconds;
                const percentage = (totalTime / maxSeconds) * 100;
                return Math.min(100, percentage);
              })()}%`
            }}
            exit={{ width: 0 }}
            transition={{ duration: 0.4, ease: "easeInOut" }}
            className="absolute inset-y-0 left-0 flex overflow-hidden rounded-full"
          >
            <div className="flex h-full w-full">
              {appData.map((app, index) => {
                const relativePercentage = (app.used_time / totalTime) * 100;
                return (
                  <motion.div 
                    key={index}
                    initial={{ width: 0 }}
                    animate={{ width: `${relativePercentage}%` }}
                    transition={{ duration: 0.4, ease: "easeInOut", delay: 0.1 }}
                    className={`h-full progress-segment bg-gradient-to-r ${
                      index === 0 ? 'from-[#1E3A8A] via-[#1E40AF] to-[#2563EB] rounded-l-full' :
                      index === 1 ? 'from-[#3B82F6] via-[#60A5FA] to-[#93C5FD]' :
                      index === 2 ? 'from-[#60A5FA] via-[#93C5FD] to-[#BFDBFE]' :
                      index === 3 ? 'from-[#93C5FD] via-[#BFDBFE] to-[#DBEAFE]' :
                      'from-[#BFDBFE] via-[#DBEAFE] to-[#EFF6FF] rounded-r-full'
                    }`}
                  />
                );
              })}
            </div>
          </motion.div>
        </AnimatePresence>
        <div className="absolute inset-0 w-full h-full rounded-full opacity-60 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.9),rgba(255,255,255,0))]" />
      </div>

      {/* App List */}
      <div className="space-y-2.5 flex-1">
        <AnimatePresence mode="wait">
          {appData.map((app, index) => (
            <motion.div 
              key={app.name + index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="flex items-center justify-between group hover:bg-blue-50/80 p-2 rounded-xl transition-all duration-300"
            >
              <div className="flex items-center gap-3">
                <div 
                  className={`w-9 h-9 ${
                    index === 0 ? 'bg-[#1E293B]' :
                    index === 1 ? 'bg-[#faf1f0] border border-blue-100' :
                    index === 2 ? 'bg-[#faf1f0]' :
                    index === 3 ? 'bg-[#faf1f0]' :
                    'bg-[#faf1f0]'
                  } rounded-xl flex items-center justify-center shadow-[0_4px_8px_rgba(0,0,0,0.1)] transform group-hover:scale-105 transition-transform duration-300`}
                >
                  {app.logo_url ? (
                    <img 
                      src={app.logo_url}
                      alt={app.name}
                      className="w-5 h-5 object-contain"
                      onError={(e) => {
                        console.log(`Error loading logo for ${app.name}`);
                        e.currentTarget.style.display = 'none';
                      }}
                    />
                  ) : (
                    <Settings className="w-4 h-4 text-gray-400" />
                  )}
                </div>
                <span className="font-medium text-[#1E293B] text-sm tracking-tight">{app.name}</span>
              </div>
              <div className="flex items-center gap-2">
                <motion.span 
                  key={app.used_time}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-[#64748B] font-medium group-hover:text-[#2563EB] transition-colors duration-300 text-sm"
                >
                  {formatTime(app.used_time)}
                </motion.span>
                <div 
                  className={`w-2 h-2 rounded-full bg-gradient-to-r ${
                    index === 0 ? 'from-[#1E3A8A] to-[#2563EB]' :
                    index === 1 ? 'from-[#3B82F6] to-[#93C5FD]' :
                    index === 2 ? 'from-[#60A5FA] to-[#BFDBFE]' :
                    index === 3 ? 'from-[#93C5FD] to-[#DBEAFE]' :
                    'from-[#BFDBFE] to-[#EFF6FF]'
                  } shadow-[0_2px_4px_rgba(37,99,235,0.3)]`}
                />
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default HorizontalChart; 