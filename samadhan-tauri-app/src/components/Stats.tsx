import { Clock, Smartphone, Layout, BrainCircuit, Zap } from 'lucide-react';
import { formatNumber, formatTime } from '../lib/utils';
import { motion } from 'framer-motion';

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

const stats = [
  {
    name: 'Total Screen Time',
    value: 165, // in minutes
    icon: Smartphone,
    change: '+12.5%',
    changeType: 'increase',
    format: 'time',
  },
  {
    name: 'Focus Time',
    value: 85, // in minutes
    icon: BrainCircuit,
    change: '+28.2%',
    changeType: 'increase',
    format: 'time',
  },
  {
    name: 'App Openings',
    value: 124,
    icon: Layout,
    change: '-4.1%',
    changeType: 'decrease',
    format: 'number',
  },
  {
    name: 'Productivity Score',
    value: 78,
    icon: Zap,
    change: '+15.5%',
    changeType: 'increase',
    format: 'score',
  },
];

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

export function Stats() {
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
            {stat.format === 'time' 
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