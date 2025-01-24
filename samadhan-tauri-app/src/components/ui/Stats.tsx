import { Smartphone, Layout, BrainCircuit, Zap } from 'lucide-react';
import { formatNumber, formatTime } from '../../lib/utils';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { invoke } from '@tauri-apps/api/core';

interface StatCardProps {
  className?: string;
  children: React.ReactNode;
}

function StatCard({ className, children }: StatCardProps) {
  return (
    <div className={`bg-white rounded-[20px] shadow-[0_8px_24px_-12px_rgba(0,0,0,0.06)] border border-[#f5f5f5] p-4 ${className}`}>
      {children}
    </div>
  );
}

interface AppUsageData {
  name: string;
  used_time: number;
  color?: string;
}

interface UsageData {
  apps: AppUsageData[];
  total_time: number;
}

const containerVariants = {
  hidden: { 
    opacity: 0,
    y: -10,
  },
  visible: { 
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: [0.22, 1, 0.36, 1],
      staggerChildren: 0.15,
      delayChildren: 0.2
    }
  }
};

const cardVariants = {
  hidden: { 
    opacity: 0,
    y: -8,
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

interface StatsProps {
  email?: string;
}

export function Stats({ email }: StatsProps) {
  const [screenTime, setScreenTime] = useState<number>(0);
  const [focusTime, setFocusTime] = useState<number>(85);
  const [pickups, setPickups] = useState<number>(4);
  const [productivityScore, setProductivityScore] = useState<number>(78);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [changePercentage, setChangePercentage] = useState<string>('+12.5%');
  const [changeType, setChangeType] = useState<'increase' | 'decrease'>('increase');

  useEffect(() => {
    const fetchScreenTime = async () => {
      if (!email) {
        setIsLoading(false);
        return;
      }

      try {
        const response = await invoke<{
          success: boolean;
          data: {
            data: {
              today: UsageData;
              yesterday: UsageData;
              this_week: UsageData;
            };
          };
          error?: string;
        }>('fetch_all_app_usage', { email });

        if (response.success && response.data) {
          // Convert seconds to minutes and round to nearest integer
          const totalMinutes = Math.round(response.data.data.today.total_time / 60);
          setScreenTime(totalMinutes);
          
          // Calculate the percentage change
          const todayTime = response.data.data.today.total_time;
          const yesterdayTime = response.data.data.yesterday.total_time;
          const percentageChange = yesterdayTime > 0 
            ? ((todayTime - yesterdayTime) / yesterdayTime) * 100 
            : 0;

          // Update the change percentage and type
          const formattedChange = `${percentageChange >= 0 ? '+' : ''}${percentageChange.toFixed(1)}%`;
          setChangePercentage(formattedChange);
          setChangeType(percentageChange >= 0 ? 'increase' : 'decrease');
        } else {
          setError(response.error || 'Failed to fetch data');
        }
      } catch (error) {
        console.error('Error fetching screen time:', error);
        setError('Failed to fetch data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchScreenTime();
  }, [email]);

  const stats = [
    {
      name: 'Total Screen Time',
      value: screenTime,
      icon: Smartphone,
      change: changePercentage,
      changeType: changeType,
      format: 'time' as const,
      isLoading: isLoading,
    },
    {
      name: 'Focus Time',
      value: focusTime,
      icon: BrainCircuit,
      change: '+28.2%',
      changeType: 'increase' as const,
      format: 'time' as const,
    },
    {
      name: 'Pickups',
      value: pickups,
      icon: Layout,
      change: '-4.1%',
      changeType: 'decrease' as const,
      format: 'number' as const,
    },
    {
      name: 'Productivity Score',
      value: productivityScore,
      icon: Zap,
      change: '+15.5%',
      changeType: 'increase' as const,
      format: 'score' as const,
    },
  ];

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="grid grid-cols-4 gap-4"
    >
      {stats.map((stat, index) => (
        <motion.div
          key={stat.name}
          variants={cardVariants}
          className="bg-white rounded-2xl p-4 shadow-[0_8px_30px_-12px_rgba(0,0,0,0.05)] border border-[#f5f5f5]"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="p-2 rounded-xl bg-[#fafafa]">
              <stat.icon className="h-4 w-4 text-gray-600" />
            </div>
            <div className={`text-xs font-medium ${stat.changeType === 'increase' ? 'text-emerald-600' : 'text-rose-600'}`}>
              {stat.change}
            </div>
          </div>
          <div className="text-2xl font-bold text-gray-900 mb-1">
            {stat.isLoading ? (
              <div className="animate-pulse bg-gray-200 h-8 w-24 rounded"></div>
            ) : stat.format === 'time' 
              ? formatTime(stat.value)
              : stat.format === 'score'
              ? `${stat.value}%`
              : formatNumber(stat.value)}
          </div>
          <div className="text-sm text-gray-500 font-medium">
            {stat.name}
          </div>
        </motion.div>
      ))}
    </motion.div>
  );
} 