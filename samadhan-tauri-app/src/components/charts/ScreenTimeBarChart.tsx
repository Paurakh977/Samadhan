import { useState, memo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bar } from '@visx/shape';
import { Group } from '@visx/group';
import { scaleBand, scaleLinear } from '@visx/scale';
import { Text } from '@visx/text';

interface ScreenTimeData {
  day: string;
  entertainment: number;
  social: number;
  productivity: number;
  other: number;
}

type Category = keyof Omit<ScreenTimeData, 'day'>;

const data: ScreenTimeData[] = [
  { day: 'Mon', entertainment: 2.5, social: 1.8, productivity: 3.2, other: 0.8 },
  { day: 'Tue', entertainment: 2.1, social: 2.2, productivity: 4.1, other: 0.5 },
  { day: 'Wed', entertainment: 3.2, social: 1.5, productivity: 3.8, other: 0.7 },
  { day: 'Thu', entertainment: 2.8, social: 2.1, productivity: 3.5, other: 0.9 },
  { day: 'Fri', entertainment: 3.5, social: 2.8, productivity: 2.9, other: 1.1 },
  { day: 'Sat', entertainment: 4.2, social: 3.1, productivity: 2.1, other: 1.3 },
  { day: 'Sun', entertainment: 4.8, social: 3.5, productivity: 1.8, other: 1.5 }
];

const categories: Category[] = ['entertainment', 'social', 'productivity', 'other'];
const colors: Record<Category, string> = {
  entertainment: '#FF6B6B',
  social: '#4ECDC4',
  productivity: '#45B7D1',
  other: '#96A5A6'
};

// Add category labels mapping for better display names
const categoryLabels: Record<Category, string> = {
  entertainment: 'Entertainment',
  social: 'Social',
  productivity: 'Productivity',
  other: 'Other'
};

interface Props {
  width: number;
  height: number;
}

interface TooltipData {
  x: number;
  y: number;
  day: string;
  data: ScreenTimeData;
}

const ScreenTimeBarChart = memo(({ width, height }: Props) => {
  const [hoveredBar, setHoveredBar] = useState<string | null>(null);
  const [tooltipData, setTooltipData] = useState<TooltipData | null>(null);

  // Margins
  const margin = { top: 30, right: 20, bottom: 20, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Scales
  const yScale = scaleBand({
    range: [0, innerHeight],
    domain: data.map(d => d.day),
    padding: 0.15  // Reduced padding between day groups for much thicker bars
  });

  const xScale = scaleLinear({
    range: [0, innerWidth],
    domain: [0, Math.max(...data.map(d => 
      Math.max(d.entertainment, d.social, d.productivity, d.other)
    )) * 1.1],
    nice: true
  });

  // Calculate bar height with better proportions
  const categoryPadding = 1; // Minimal padding between bars in the same group
  const groupHeight = yScale.bandwidth();
  const barHeight = (groupHeight - (categoryPadding * (categories.length - 1))) / categories.length;

  const handleMouseEnter = (event: React.MouseEvent, d: ScreenTimeData, category: Category) => {
    const rect = (event.target as SVGElement).getBoundingClientRect();
    setHoveredBar(`${d.day}-${category}`);
    setTooltipData({
      x: rect.right,
      y: rect.top,
      day: d.day,
      data: d
    });
  };

  const handleMouseLeave = () => {
    setHoveredBar(null);
    setTooltipData(null);
  };

  return (
    <div className="relative">
      {/* Legend with fade in animation */}
      <motion.div 
        initial={{ opacity: 0, y: -5 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.1 }}
        className="flex items-center gap-8 mb-8 justify-end"
      >
        <div className="flex items-center gap-8 text-[13px] text-gray-600">
          {categories.map((category, index) => (
            <motion.div 
              key={category} 
              initial={{ opacity: 0, x: -5 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="flex items-center gap-2"
            >
              <div 
                className="w-3 h-3 rounded-[3px]"
                style={{ backgroundColor: colors[category] }}
              />
              <span className="font-medium tracking-tight">
                {categoryLabels[category]}
              </span>
            </motion.div>
          ))}
        </div>
      </motion.div>

      <svg width={width} height={height}>
        <Group left={margin.left} top={margin.top}>
          {/* Y-axis labels with fade in */}
          {yScale.domain().map((day, index) => (
            <motion.g
              key={day}
              initial={{ opacity: 0, x: -5 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
            >
              <Text
                x={-18}
                y={yScale(day)! + yScale.bandwidth() / 2}
                textAnchor="end"
                dy=".33em"
                fontSize={13}
                fill="#4B5563"
                fontWeight={500}
                fontFamily="Inter, system-ui, sans-serif"
              >
                {day}
              </Text>
            </motion.g>
          ))}

          {/* Bars with staggered animation */}
          {data.map((d, dayIndex) => (
            <Group key={d.day}>
              {categories.map((category, i) => {
                const barY = yScale(d.day)! + (i * (barHeight + categoryPadding));
                const barWidth = xScale(d[category]);
                const isHovered = hoveredBar === `${d.day}-${category}`;

                return (
                  <motion.g 
                    key={category}
                    initial={{ opacity: 0, scaleX: 0 }}
                    animate={{ opacity: 1, scaleX: 1 }}
                    transition={{
                      duration: 0.4,
                      delay: dayIndex * 0.1 + i * 0.05,
                      ease: [0.34, 1.56, 0.64, 1]
                    }}
                    style={{ transformOrigin: '0 0' }}
                  >
                    <motion.g
                      animate={{
                        filter: isHovered ? 'brightness(1.1)' : 'brightness(1)',
                        scale: isHovered ? 1.01 : 1
                      }}
                      transition={{ 
                        duration: 0.2,
                        ease: 'easeOut'
                      }}
                      style={{ transformOrigin: `${barY + barHeight / 2}px ${barWidth / 2}px` }}
                    >
                      <Bar
                        x={0}
                        y={barY}
                        width={barWidth}
                        height={barHeight}
                        fill={colors[category]}
                        opacity={isHovered ? 1 : 0.92}
                        rx={4}
                        onMouseEnter={(e) => handleMouseEnter(e, d, category)}
                        onMouseLeave={handleMouseLeave}
                        style={{
                          transition: 'all 0.2s ease-out',
                          cursor: 'pointer'
                        }}
                      />
                    </motion.g>
                  </motion.g>
                );
              })}
            </Group>
          ))}
        </Group>
      </svg>

      <AnimatePresence>
        {tooltipData && (
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: 5 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 5 }}
            transition={{ duration: 0.15, ease: 'easeOut' }}
            className="fixed z-50 p-3.5 text-[13px] bg-white rounded-lg shadow-lg pointer-events-none border border-gray-100/50 backdrop-blur-sm min-w-[180px]"
            style={{
              left: tooltipData.x + 10,
              top: tooltipData.y,
              backgroundColor: 'rgba(255, 255, 255, 0.98)',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04)'
            }}
          >
            <div className="font-medium text-gray-900 mb-2.5 pb-1.5 border-b border-gray-100">
              {tooltipData.day}
            </div>
            <div className="space-y-2">
              {categories.map(category => (
                <div key={category} className="flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <div 
                      className="w-2.5 h-2.5 rounded-[3px]"
                      style={{ backgroundColor: colors[category] }}
                    />
                    <span className="text-gray-700 font-medium tracking-tight">
                      {categoryLabels[category]}
                    </span>
                  </div>
                  <span className="font-semibold text-gray-900 tabular-nums">
                    {tooltipData.data[category].toFixed(1)}h
                  </span>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
});

ScreenTimeBarChart.displayName = 'ScreenTimeBarChart';

export default ScreenTimeBarChart; 