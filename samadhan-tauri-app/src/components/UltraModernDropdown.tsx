import React, { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { MinimalIcon } from "./MinimalIcon"

type TimeOption = 'today' | 'yesterday' | 'this_week';
const options: TimeOption[] = ["today", "yesterday", "this_week"];
const displayNames: Record<TimeOption, string> = {
  today: "Today",
  yesterday: "Yesterday",
  this_week: "This Week"
};

interface Props {
  value: TimeOption;
  onChange: (value: TimeOption) => void;
}

export default function UltraModernDropdown({ value, onChange }: Props) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative font-sans z-50">
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/50 hover:bg-blue-50/50 transition-all duration-300 backdrop-blur-sm"
        whileHover={{ 
          scale: 1.02,
          transition: { duration: 0.2, ease: "easeOut" }
        }}
        whileTap={{ scale: 0.98 }}
      >
        <motion.span
          className="text-sm font-medium"
          animate={{ 
            color: isOpen ? "#2563EB" : "#64748B",
          }}
          transition={{ duration: 0.2 }}
        >
          {displayNames[value]}
        </motion.span>
        <MinimalIcon isOpen={isOpen} />
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -4, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -4, scale: 0.95 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className="absolute right-0 mt-2 w-36 bg-white/95 backdrop-blur-sm rounded-xl shadow-lg border border-blue-100/50 overflow-hidden"
          >
            {options.map((option, index) => (
              <motion.button
                key={option}
                onClick={() => {
                  onChange(option);
                  setIsOpen(false);
                }}
                className="relative block w-full text-left px-4 py-2 text-sm text-gray-600 transition-all duration-200 hover:pl-6"
                initial={{ opacity: 0, x: -4 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ 
                  delay: index * 0.05,
                  duration: 0.2
                }}
                whileHover={{
                  backgroundColor: "rgba(219, 234, 254, 0.5)",
                  color: "#2563EB",
                  transition: { duration: 0.2 }
                }}
              >
                <motion.div
                  initial={{ scale: 0, opacity: 0 }}
                  whileHover={{ 
                    scale: 1, 
                    opacity: 1,
                    transition: { duration: 0.2 }
                  }}
                  className="absolute left-2 top-1/2 -translate-y-1/2 w-1 h-1 bg-blue-500 rounded-full"
                />
                {displayNames[option]}
              </motion.button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
} 