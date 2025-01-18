import * as React from 'react';
import { motion } from 'framer-motion';
import { Calendar, BarChart2 } from 'lucide-react';

interface SidebarProps {
  currentView: 'daily' | 'weekly';
  onViewChange: (view: 'daily' | 'weekly') => void;
}

const Sidebar: React.FC<SidebarProps> = ({ currentView, onViewChange }) => {
  return (
    <motion.div 
      initial={{ x: -280, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{
        type: "spring",
        stiffness: 260,
        damping: 20
      }}
      className="w-[280px] h-full bg-white border-r border-[#f5f5f5] p-6"
    >
      <div className="flex flex-col h-full">
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-8 h-8 rounded-xl bg-blue-600 flex items-center justify-center">
            <span className="text-white font-semibold">S</span>
          </div>
          <span className="text-xl font-bold text-gray-900">Samadhan</span>
        </div>

        <nav className="flex-1">
          <div className="space-y-1">
            <button
              onClick={() => onViewChange('daily')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-left transition-colors ${
                currentView === 'daily'
                  ? 'bg-blue-50 text-blue-600'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <Calendar className="w-5 h-5" />
              <span className="font-medium">Daily Overview</span>
            </button>

            <button
              onClick={() => onViewChange('weekly')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-left transition-colors ${
                currentView === 'weekly'
                  ? 'bg-blue-50 text-blue-600'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <BarChart2 className="w-5 h-5" />
              <span className="font-medium">Weekly Overview</span>
            </button>
          </div>
        </nav>

        <div className="mt-auto pt-6 border-t border-gray-100">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
              <span className="text-sm font-medium text-gray-600">JD</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">John Doe</p>
              <p className="text-sm text-gray-500 truncate">john@example.com</p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default Sidebar; 