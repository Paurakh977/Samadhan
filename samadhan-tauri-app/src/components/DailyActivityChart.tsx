import React from 'react';
import { motion } from 'framer-motion';

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
  const mins = minutes % 60;
  if (hours === 0) {
    return `${mins}m`;
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

const DailyActivityChart: React.FC = () => {
  const data = generateRandomData();
  
  const totalSocial = Math.floor(73);
  const totalEntertainment = Math.floor(50);
  const totalProductivity = Math.floor(18);
  const totalOther = Math.floor(24);
  const totalTime = totalSocial + totalEntertainment + totalProductivity + totalOther;

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="flex-1 min-h-[480px] mt-[60px] bg-white/80 backdrop-blur-sm rounded-[32px] shadow-[0_15px_40px_-15px_rgba(0,0,0,0.1)] border border-gray-100/50 p-6"
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
            <span className="text-sm text-gray-500 transition-colors duration-200 group-hover:text-gray-700">{formatTime(totalSocial)}</span>
          </motion.div>
          <motion.div variants={itemVariants} className="flex items-center group">
            <span className="text-sm font-medium text-[#40b7ff] mr-2 transition-colors duration-200 group-hover:text-[#2e8bc0]">Entertainment</span>
            <span className="text-sm text-gray-500 transition-colors duration-200 group-hover:text-gray-700">{formatTime(totalEntertainment)}</span>
          </motion.div>
          <motion.div variants={itemVariants} className="flex items-center group">
            <span className="text-sm font-medium text-[#ff9f40] mr-2 transition-colors duration-200 group-hover:text-[#e68a2e]">Productivity</span>
            <span className="text-sm text-gray-500 transition-colors duration-200 group-hover:text-gray-700">{formatTime(totalProductivity)}</span>
          </motion.div>
          <motion.div variants={itemVariants} className="flex items-center group">
            <span className="text-sm font-medium text-[#9CA3AF] mr-2 transition-colors duration-200 group-hover:text-[#6B7280]">Other</span>
            <span className="text-sm text-gray-500 transition-colors duration-200 group-hover:text-gray-700">{formatTime(totalOther)}</span>
          </motion.div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default DailyActivityChart; 