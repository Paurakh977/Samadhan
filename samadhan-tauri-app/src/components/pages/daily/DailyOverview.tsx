import { motion } from 'framer-motion';
import { Stats } from '../../components/stats/Stats';
import { DailyActivityChart } from '../../charts/DailyActivityChart';
import { ScreenTimeProgress } from '../../charts/ScreenTimeProgress';

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

export function DailyOverview() {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="h-full flex flex-col px-6 pt-6"
    >
      <Stats />
      <div className="flex gap-6 mt-2 flex-1">
        <ScreenTimeProgress
          startHour={3}
          startMinute={25}
          startPeriod="PM"
          endHour={1}
          endMinute={10}
          endPeriod="AM"
        />
        <DailyActivityChart />
      </div>
    </motion.div>
  );
} 