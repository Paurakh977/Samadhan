import { motion } from 'framer-motion';
import { Stats } from '../../components/stats/Stats';

const containerVariants = {
  hidden: { 
    opacity: 0,
  },
  visible: { 
    opacity: 1,
    transition: {
      duration: 0.4,
      ease: [0.22, 1, 0.36, 1],
      staggerChildren: 0.15
    }
  }
};

export function WeeklyOverview() {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="h-full flex flex-col px-6 pt-6"
    >
      <Stats />
      <div className="flex gap-6 mt-2 flex-1">
        {/* Weekly charts will be added here */}
        <div className="flex-1 min-h-[480px] bg-white rounded-[28px] shadow-[0_12px_36px_-12px_rgba(0,0,0,0.06)] border border-[#f5f5f5] p-6">
          <h2 className="text-2xl font-bold text-gray-900">Weekly Overview</h2>
          <p className="text-gray-500 mt-2">Weekly statistics and charts coming soon...</p>
        </div>
      </div>
    </motion.div>
  );
} 