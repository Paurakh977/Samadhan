import React from 'react';
import { motion } from 'framer-motion';

const GoalsList: React.FC = () => {
  const goals = [
    "Read for 30 minutes",
    "Exercise for at least 1 hour",
    "Complete a work project",
    "Spend quality time with family",
    "Meditate for 10 minutes",
    "Limit screen time to 2 hours",
    "Cook a new recipe",
  ];

  return (
    <motion.div 
      className="bg-white rounded-lg shadow-lg border border-zinc-100 p-6 transition-transform transform hover:scale-105 h-[400px]"
      initial={{ opacity: 0, y: -20 }} 
      animate={{ opacity: 1, y: 0 }} 
      transition={{ duration: 0.5 }}
    >
      <h2 className="text-zinc-900 text-lg font-semibold mb-4">Daily Goals</h2>
      <ul className="list-none pl-0">
        {goals.map((goal, index) => (
          <motion.li 
            key={index} 
            className="flex items-center text-zinc-700 text-sm mb-3"
            initial={{ opacity: 0, y: 10 }} 
            animate={{ opacity: 1, y: 0 }} 
            transition={{ duration: 0.3, delay: index * 0.1 }} // Delay for staggered effect
          >
            <span className="text-green-500 mr-2">✔️</span>
            <span className="font-normal">{goal}</span>
          </motion.li>
        ))}
      </ul>
    </motion.div>
  );
};

export default GoalsList;
