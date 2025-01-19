import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface NavItemProps {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  onClick: () => void;
  isExpanded: boolean;
}

const NavItem: React.FC<NavItemProps> = ({ icon, label, active, onClick, isExpanded }) => (
  <motion.div
    onClick={onClick}
    className="relative flex items-center w-full cursor-pointer group"
    whileHover={{ x: 2 }}
    transition={{ duration: 0.15 }}
  >
    {active && (
      <motion.div
        layoutId="activeTab"
        className="absolute inset-y-0 left-3 right-[-12px] bg-white before:content-[''] before:absolute before:right-0 
          before:top-[-25px] before:w-[25px] before:h-[25px] before:rounded-br-[25px] before:shadow-[6px_6px_0_6px_white]
          before:bg-transparent after:content-[''] after:absolute after:right-0 after:bottom-[-25px] 
          after:w-[25px] after:h-[25px] after:rounded-tr-[25px] after:shadow-[6px_-6px_0_6px_white] after:bg-transparent"
        initial={false}
        transition={{ type: "spring", stiffness: 500, damping: 30 }}
        style={{
          borderTopLeftRadius: '16px',
          borderBottomLeftRadius: '16px',
        }}
      />
    )}
    <div 
      className={`flex items-center gap-3 px-5 py-2.5 w-full relative z-10 transition-all duration-200
        ${active ? 'text-indigo-600' : 'text-white/70 group-hover:text-white'}`}
    >
      <div className={`w-[18px] h-[18px] flex items-center justify-center transition-transform duration-150 ${active ? 'scale-110' : 'group-hover:scale-105'}`}>
        {icon}
      </div>
      <AnimatePresence mode="wait">
        {isExpanded && (
          <motion.span 
            className="text-[14px] font-medium tracking-wide whitespace-nowrap"
            initial={{ opacity: 0, width: 0 }}
            animate={{ opacity: 1, width: "auto" }}
            exit={{ opacity: 0, width: 0 }}
            transition={{ duration: 0.15, ease: "easeOut" }}
          >
            {label}
          </motion.span>
        )}
      </AnimatePresence>
    </div>
  </motion.div>
);

interface SidebarProps {
  currentView?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ currentView = 'home' }) => {
  const [activeTab, setActiveTab] = React.useState(currentView);
  const [isExpanded, setIsExpanded] = React.useState(true);
  const [isLoaded, setIsLoaded] = React.useState(false);

  React.useEffect(() => {
    setIsLoaded(true);
  }, []);

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    window.dispatchEvent(new CustomEvent('viewChange', { detail: tab }));
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Company name and logo - Inside sidebar now */}
      <motion.div 
        className="absolute top-6 left-0 right-0 flex items-center px-5 z-20"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2, delay: 0.1 }}
      >
        <div className="flex items-center gap-2.5">
          <motion.div 
            className="p-1.5 bg-white rounded-xl shadow-md"
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.2 }}
          >
            <motion.img 
              src="/src-tauri/icons/icon.png"
              alt="Samadhan"
              className="w-5 h-5 rounded-lg"
            />
          </motion.div>
          <AnimatePresence mode="wait">
            {isExpanded && (
              <motion.span 
                className="text-gray-800 text-[15px] font-medium tracking-wide"
                initial={{ opacity: 0, x: -10, width: 0 }}
                animate={{ opacity: 1, x: 0, width: 'auto' }}
                exit={{ opacity: 0, x: -10, width: 0 }}
                transition={{ duration: 0.2 }}
              >
                Samadhan
              </motion.span>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Sidebar */}
      <motion.div 
        initial={{ width: 220, x: -100, opacity: 0 }}
        animate={{ 
          width: isExpanded ? 220 : 80,
          x: 0,
          opacity: 1
        }}
        transition={{ 
          duration: isLoaded ? 0.3 : 0.5,
          ease: isLoaded ? "easeInOut" : [0.23, 1, 0.32, 1]
        }}
        className="bg-indigo-600 flex flex-col relative overflow-hidden mt-20 shadow-xl min-h-[calc(100vh-5rem)]"
        style={{
          borderTopRightRadius: '32px',
        }}
      >
        {/* Toggle Button */}
        <motion.div 
          className="absolute -right-0.5 top-7 z-50"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4, duration: 0.2 }}
        >
          <motion.button
            onClick={() => setIsExpanded(!isExpanded)}
            className="w-5 h-5 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-50"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <motion.div
              animate={{ rotate: isExpanded ? 0 : 180 }}
              transition={{ duration: 0.2 }}
              className="flex items-center justify-center w-full h-full"
            >
              <svg 
                className="w-3 h-3 text-indigo-600" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2.5"
              >
                <path d="M9 5l7 7-7 7" />
              </svg>
            </motion.div>
          </motion.button>
        </motion.div>

        {/* Profile Section - Always visible */}
        <motion.div 
          className="flex flex-col items-center px-5 pt-8 pb-10"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.3 }}
        >
          <motion.div 
            className="relative rounded-full bg-white/10 mb-3 overflow-hidden ring-2 ring-white/20 ring-offset-2 ring-offset-indigo-600 shadow-lg"
            animate={{ 
              width: isExpanded ? '3.5rem' : '2.75rem',
              height: isExpanded ? '3.5rem' : '2.75rem'
            }}
            transition={{ duration: 0.2 }}
          >
            <img 
              src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&h=100&fit=crop&crop=faces"
              alt="User"
              className="w-full h-full object-cover"
            />
          </motion.div>
          <AnimatePresence mode="wait">
            {isExpanded && (
              <motion.h2 
                className="text-[15px] font-medium text-white tracking-wide"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -5 }}
                transition={{ duration: 0.15 }}
              >
                Hello, Paurakh
              </motion.h2>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Navigation */}
        <motion.nav 
          className="flex flex-col space-y-1 px-1"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.3 }}
        >
          <NavItem
            icon={<svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            </svg>}
            label="Home"
            active={activeTab === 'home'}
            onClick={() => handleTabChange('home')}
            isExpanded={isExpanded}
          />
          <NavItem
            icon={<svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M3 3V21H21M9 18V9M15 18V5M21 18V11" />
            </svg>}
            label="Analytics"
            active={activeTab === 'analytics'}
            onClick={() => handleTabChange('analytics')}
            isExpanded={isExpanded}
          />
          <NavItem
            icon={<svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M12 2L20 7V17L12 22L4 17V7L12 2Z" />
            </svg>}
            label="Goals"
            active={activeTab === 'goals'}
            onClick={() => handleTabChange('goals')}
            isExpanded={isExpanded}
          />
          <NavItem
            icon={<svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M8 12H8.01M12 12H12.01M16 12H16.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>}
            label="Coaching"
            active={activeTab === 'coaching'}
            onClick={() => setActiveTab('coaching')}
            isExpanded={isExpanded}
          />
          <NavItem
            icon={<svg className="w-[18px] h-[18px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>}
            label="Settings"
            active={activeTab === 'settings'}
            onClick={() => setActiveTab('settings')}
            isExpanded={isExpanded}
          />
        </motion.nav>

        {/* Logout Button */}
        <motion.div 
          className="mt-auto pb-6 px-1"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.3 }}
        >
          <NavItem
            icon={<svg className="w-[18px] h-[18px] rotate-180" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75">
              <path d="M17 16L21 12M21 12L17 8M21 12H9M9 21H7C5.89543 21 5 20.1046 5 19V5C5 3.89543 5.89543 3 7 3H9" />
            </svg>}
            label="Log out"
            active={false}
            onClick={() => {}}
            isExpanded={isExpanded}
          />
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Sidebar; 