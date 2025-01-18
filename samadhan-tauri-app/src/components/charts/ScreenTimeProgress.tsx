import React from 'react';
import { motion } from 'framer-motion';

interface ScreenTimeProgressProps {
  startHour: number;
  startMinute: number;
  startPeriod: 'AM' | 'PM';
  endHour: number;
  endMinute: number;
  endPeriod: 'AM' | 'PM';
}

const convertTo24Hour = (hour: number, period: string): number => {
  if (period === 'AM') {
    return hour === 12 ? 0 : hour;
  }
  return hour === 12 ? 12 : hour + 12;
};

const calculateTimeDifference = (
  startHour: number,
  startMinute: number,
  startPeriod: string,
  endHour: number,
  endMinute: number,
  endPeriod: string
): [number, number] => {
  const start24Hour = convertTo24Hour(startHour, startPeriod);
  const end24Hour = convertTo24Hour(endHour, endPeriod);

  const startTotalMinutes = start24Hour * 60 + startMinute;
  let endTotalMinutes = end24Hour * 60 + endMinute;

  if (endTotalMinutes < startTotalMinutes) {
    endTotalMinutes += 24 * 60;
  }

  const diffMinutes = endTotalMinutes - startTotalMinutes;
  return [Math.floor(diffMinutes / 60), diffMinutes % 60];
};

const getAngle = (hour: number, minute: number = 0): number => {
  hour = hour % 12;
  const angle = (hour * 30) + (minute * 0.5);
  return angle - 90;
};

const formatTime = (hour: number, minute: number, period: string): string => {
  return `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')} ${period}`;
};

const ScreenTimeProgress: React.FC<ScreenTimeProgressProps> = ({
  startHour,
  startMinute,
  startPeriod,
  endHour,
  endMinute,
  endPeriod,
}) => {
  const startAngle = getAngle(startHour, startMinute);
  const endAngle = getAngle(endHour, endMinute);
  const [diffHours, diffMinutes] = calculateTimeDifference(
    startHour,
    startMinute,
    startPeriod,
    endHour,
    endMinute,
    endPeriod
  );

  const size = 300;
  const progressWidth = 30;
  const width = size - progressWidth;
  const height = size - progressWidth;

  let angleLength = endAngle < startAngle 
    ? 360 - (startAngle - endAngle) 
    : endAngle - startAngle;

  // Calculate icon positions exactly like PyQt
  const startRad = (startAngle * Math.PI) / 180;
  const endRad = (endAngle * Math.PI) / 180;
  
  const iconSize = 24;
  const startX = size / 2 + (width / 2) * Math.cos(startRad) - iconSize / 2;
  const startY = size / 2 + (height / 2) * Math.sin(startRad) - iconSize / 2;
  const endX = size / 2 + (width / 2) * Math.cos(endRad) - iconSize / 2;
  const endY = size / 2 + (height / 2) * Math.sin(endRad) - iconSize / 2;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ 
        duration: 0.6,
        ease: [0.22, 1, 0.36, 1],
      }}
      className="relative w-[350px] h-auto min-h-[480px] bg-white/80 backdrop-blur-sm rounded-[32px] shadow-[0_15px_40px_-15px_rgba(0,0,0,0.1)] transition-all duration-300 hover:shadow-[0_20px_50px_-12px_rgba(0,0,0,0.12)] border border-gray-100/50 flex flex-col"
    >
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
        className="relative w-full flex-1 flex items-center justify-center p-6 pb-2"
      >
        <div className="relative" style={{ width: size, height: size }}>
          {/* Clock face background with entrance animation */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9, rotate: -10 }}
            animate={{ opacity: 0.85, scale: 1, rotate: 0 }}
            transition={{ delay: 0.4, duration: 0.6, ease: "easeOut" }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <div className="relative w-[240px] h-[240px] rounded-full">
              <img
                src="/Images/bg.png"
                alt="Clock face"
                className="w-full h-full mix-blend-multiply"
              />
            </div>
          </motion.div>

          <svg
            width={size}
            height={size}
            viewBox={`0 0 ${size} ${size}`}
            className="filter drop-shadow-[0_2px_6px_rgba(0,0,0,0.03)]"
          >
            {/* Background circle with ultra-subtle gradient */}
            <defs>
              {/* Refined gradient with modern colors */}
              <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style={{ stopColor: '#3B82F6', stopOpacity: 0.92 }} />
                <stop offset="100%" style={{ stopColor: '#2563EB', stopOpacity: 0.92 }} />
              </linearGradient>

              {/* Enhanced inner shadow for depth */}
              <filter id="innerShadow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur in="SourceAlpha" stdDeviation="2" result="blur" />
                <feOffset dx="1" dy="1" />
                <feComposite in2="SourceAlpha" operator="arithmetic" k2="-1" k3="1" result="shadowDiff" />
                <feFlood floodColor="#000000" floodOpacity="0.08" />
                <feComposite in2="shadowDiff" operator="in" />
                <feComposite in2="SourceGraphic" operator="over" />
              </filter>

              {/* Sophisticated elevation effect */}
              <filter id="elevation" x="-50%" y="-50%" width="200%" height="200%">
                <feOffset dx="0" dy="4" in="SourceAlpha" result="offset" />
                <feGaussianBlur in="offset" stdDeviation="4" result="blur1" />
                <feFlood floodColor="#3B82F6" floodOpacity="0.15" result="color" />
                <feComposite operator="in" in="color" in2="blur1" result="shadow1" />
                
                <feOffset dx="0" dy="2" in="SourceAlpha" result="offset2" />
                <feGaussianBlur in="offset2" stdDeviation="2" result="blur2" />
                <feFlood floodColor="#3B82F6" floodOpacity="0.25" result="color2" />
                <feComposite operator="in" in="color2" in2="blur2" result="shadow2" />
                
                <feMerge>
                  <feMergeNode in="shadow1" />
                  <feMergeNode in="shadow2" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>
            
            {/* Background track with entrance animation */}
            <motion.circle
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{ pathLength: 1, opacity: 1 }}
              transition={{ delay: 0.5, duration: 0.8, ease: "easeOut" }}
              cx={size / 2}
              cy={size / 2}
              r={width / 2}
              stroke="#F1F5F9"
              fill="transparent"
              strokeWidth={progressWidth}
              strokeLinecap="round"
              filter="url(#innerShadow)"
            />
            
            {/* Progress arc with animated entrance */}
            <motion.circle
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{ pathLength: angleLength / 360, opacity: 1 }}
              transition={{ delay: 0.8, duration: 1, ease: [0.22, 1, 0.36, 1] }}
              cx={size / 2}
              cy={size / 2}
              r={width / 2}
              stroke="url(#progressGradient)"
              fill="transparent"
              strokeWidth={progressWidth}
              strokeLinecap="round"
              transform={`rotate(${startAngle} ${size / 2} ${size / 2})`}
              filter="url(#elevation)"
            />
          </svg>

          {/* Sun icon with entrance animation */}
          <motion.div 
            initial={{ opacity: 0, scale: 0, x: -20 }}
            animate={{ opacity: 1, scale: 1, x: 0 }}
            transition={{ delay: 1.2, duration: 0.4, type: "spring", stiffness: 200 }}
            whileHover={{ scale: 1.1, filter: 'drop-shadow(0 4px 8px rgba(234, 179, 8, 0.25))' }}
            className="absolute transition-all duration-200"
            style={{
              left: startX,
              top: startY,
              width: iconSize,
              height: iconSize,
              filter: 'drop-shadow(0 2px 4px rgba(234, 179, 8, 0.2))'
            }}
          >
            <img src="/Images/sun.png" alt="Sun" className="w-full h-full" />
          </motion.div>

          {/* Moon icon with entrance animation */}
          <motion.div 
            initial={{ opacity: 0, scale: 0, x: 20 }}
            animate={{ opacity: 1, scale: 1, x: 0 }}
            transition={{ delay: 1.2, duration: 0.4, type: "spring", stiffness: 200 }}
            whileHover={{ scale: 1.1, filter: 'drop-shadow(0 4px 8px rgba(59, 130, 246, 0.25))' }}
            className="absolute transition-all duration-200"
            style={{
              left: endX,
              top: endY,
              width: iconSize,
              height: iconSize,
              filter: 'drop-shadow(0 2px 4px rgba(59, 130, 246, 0.2))'
            }}
          >
            <img src="/Images/night.png" alt="Moon" className="w-full h-full" />
          </motion.div>

          {/* Time display with staggered text animation */}
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.4, duration: 0.4 }}
            className="absolute inset-0 flex flex-col items-center justify-center"
          >
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.5, duration: 0.4 }}
              className="text-[48px] font-bold text-slate-800 leading-none tracking-tight"
            >
              {diffHours}
              <motion.span 
                initial={{ opacity: 0, x: -5 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.6, duration: 0.3 }}
                className="text-[32px] font-semibold text-slate-600 ml-1"
              >
                hr
              </motion.span>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.7, duration: 0.3 }}
              className="text-sm text-slate-400 mt-1 font-medium tracking-wider uppercase"
            >
              {diffMinutes} min
            </motion.div>
          </motion.div>
        </div>
      </motion.div>

      {/* Minimalistic divider line */}
      <motion.div
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ delay: 1.7, duration: 0.4 }}
        className="w-[80%] mx-auto h-px bg-gray-100/80"
      />

      {/* Time details section with staggered entrance - now closer to the progress bar */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.8, duration: 0.4 }}
        className="px-8 py-5 flex justify-between"
      >
        <motion.div 
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 1.9, duration: 0.3 }}
          className="flex flex-col items-start"
        >
          <span className="text-xs font-medium text-gray-400 mb-1.5 tracking-wider uppercase">Start Time</span>
          <span className="text-base font-semibold text-gray-600 tracking-wide">
            {formatTime(startHour, startMinute, startPeriod)}
          </span>
        </motion.div>
        <motion.div 
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 1.9, duration: 0.3 }}
          className="flex flex-col items-end"
        >
          <span className="text-xs font-medium text-gray-400 mb-1.5 tracking-wider uppercase">End Time</span>
          <span className="text-base font-semibold text-gray-600 tracking-wide">
            {formatTime(endHour, endMinute, endPeriod)}
          </span>
        </motion.div>
      </motion.div>
    </motion.div>
  );
};

export default ScreenTimeProgress; 