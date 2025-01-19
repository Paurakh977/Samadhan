import React from 'react';
import { Settings } from 'lucide-react';
import { motion } from 'framer-motion';
import '../../styles/horizontal-chart.css';

const HorizontalChart: React.FC = () => {
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

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="h-full flex flex-col"
    >
      {/* Time Display */}
      <motion.div variants={timeVariants} className="mb-3">
        <motion.h1 
          className="text-[22px] font-semibold tracking-tight text-gray-900"
          layoutId="timeDisplay"
        >
          2 h 20 m
        </motion.h1>
        <motion.p 
          className="text-gray-500 text-xs font-medium"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          1 h 31 m less than yesterday
        </motion.p>
      </motion.div>

      {/* Enhanced 3D Progress Bar */}
      <div className="relative h-3 bg-blue-50/80 backdrop-blur-xl rounded-full progress-bar-3d mb-4">
        <div className="absolute inset-0 flex overflow-hidden rounded-full">
          <motion.div 
            variants={progressVariants}
            style={{ width: '50%' }} 
            className="progress-segment bg-gradient-to-r from-[#1E3A8A] via-[#1E40AF] to-[#2563EB] rounded-l-full"
          />
          <motion.div 
            variants={progressVariants}
            style={{ width: '20%' }} 
            className="progress-segment bg-gradient-to-r from-[#3B82F6] via-[#60A5FA] to-[#93C5FD]"
          />
          <motion.div 
            variants={progressVariants}
            style={{ width: '10%' }} 
            className="progress-segment bg-gradient-to-r from-[#60A5FA] via-[#93C5FD] to-[#BFDBFE] rounded-r-full"
          />
        </div>
        <div className="absolute inset-0 w-full h-full rounded-full opacity-60 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.9),rgba(255,255,255,0))]" />
      </div>

      {/* App List */}
      <div className="space-y-2.5 flex-1">
        {/* TikTok */}
        <motion.div 
          variants={appItemVariants}
          whileHover={{ x: 4 }}
          className="flex items-center justify-between group hover:bg-blue-50/80 p-2 rounded-xl transition-all duration-300"
        >
          <div className="flex items-center gap-3">
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="w-9 h-9 bg-[#1E293B] rounded-xl flex items-center justify-center shadow-[0_4px_8px_rgba(0,0,0,0.1)] transform group-hover:scale-105 transition-transform duration-300"
            >
              <img 
                src="https://images.unsplash.com/photo-1611605698335-8b1569810432?auto=format&fit=crop&q=80&w=100&h=100" 
                alt="TikTok"
                className="w-5 h-5 object-contain"
              />
            </motion.div>
            <span className="font-medium text-[#1E293B] text-sm tracking-tight">TikTok</span>
          </div>
          <div className="flex items-center gap-2">
            <motion.span 
              whileHover={{ color: "#2563EB" }}
              className="text-[#64748B] font-medium group-hover:text-[#2563EB] transition-colors duration-300 text-sm"
            >
              58 m
            </motion.span>
            <motion.div 
              whileHover={{ scale: 1.2 }}
              className="w-2 h-2 rounded-full bg-gradient-to-r from-[#1E3A8A] to-[#2563EB] shadow-[0_2px_4px_rgba(37,99,235,0.3)]"
            />
          </div>
        </motion.div>

        {/* Three */}
        <motion.div 
          variants={appItemVariants}
          whileHover={{ x: 4 }}
          className="flex items-center justify-between group hover:bg-blue-50/80 p-2 rounded-xl transition-all duration-300"
        >
          <div className="flex items-center gap-3">
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="w-9 h-9 bg-white border border-blue-100 rounded-xl flex items-center justify-center shadow-[0_4px_8px_rgba(0,0,0,0.05)] transform group-hover:scale-105 transition-transform duration-300"
            >
              <span className="text-base font-bold bg-gradient-to-r from-[#3B82F6] to-[#60A5FA] bg-clip-text text-transparent">3</span>
            </motion.div>
            <span className="font-medium text-[#1E293B] text-sm tracking-tight">Three</span>
          </div>
          <div className="flex items-center gap-2">
            <motion.span 
              whileHover={{ color: "#2563EB" }}
              className="text-[#64748B] font-medium group-hover:text-[#2563EB] transition-colors duration-300 text-sm"
            >
              27 m
            </motion.span>
            <motion.div 
              whileHover={{ scale: 1.2 }}
              className="w-2 h-2 rounded-full bg-gradient-to-r from-[#3B82F6] to-[#93C5FD] shadow-[0_2px_4px_rgba(37,99,235,0.3)]"
            />
          </div>
        </motion.div>

        {/* Settings */}
        <motion.div 
          variants={appItemVariants}
          whileHover={{ x: 4 }}
          className="flex items-center justify-between group hover:bg-blue-50/80 p-2 rounded-xl transition-all duration-300"
        >
          <div className="flex items-center gap-3">
            <motion.div 
              whileHover={{ scale: 1.05 }}
              className="w-9 h-9 bg-gradient-to-br from-[#1E293B] to-[#334155] rounded-xl flex items-center justify-center shadow-[0_4px_8px_rgba(0,0,0,0.1)] transform group-hover:scale-105 transition-transform duration-300"
            >
              <Settings className="w-4 h-4 text-white" />
            </motion.div>
            <span className="font-medium text-[#1E293B] text-sm tracking-tight">Settings</span>
          </div>
          <div className="flex items-center gap-2">
            <motion.span 
              whileHover={{ color: "#2563EB" }}
              className="text-[#64748B] font-medium group-hover:text-[#2563EB] transition-colors duration-300 text-sm"
            >
              15 m
            </motion.span>
            <motion.div 
              whileHover={{ scale: 1.2 }}
              className="w-2 h-2 rounded-full bg-gradient-to-r from-[#60A5FA] to-[#BFDBFE] shadow-[0_2px_4px_rgba(37,99,235,0.3)]"
            />
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default HorizontalChart; 