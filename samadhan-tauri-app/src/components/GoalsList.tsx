import React from 'react';
import { motion } from 'framer-motion';

const GoalsList: React.FC = () => {
  const goals = [
    "Limit screen time to 2 hours",
    "Increase productivity by 10%",
    "Drop social media usage by 12%",
    "Limit screen time to 4 hours",
    "Decrease screen time by 10%",
    "Drop usage of Youtube by 15%",
    "Limit usage of Whatsapp by 10%",
    "Decrease entertainment time by 8%",
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
