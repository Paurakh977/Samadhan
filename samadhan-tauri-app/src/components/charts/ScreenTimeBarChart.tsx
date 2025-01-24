import React, { useState, memo, useEffect } from 'react';
import { motion, AnimatePresence, useInView } from 'framer-motion';
import { Bar } from '@visx/shape';
import { Group } from '@visx/group';
import { scaleBand, scaleLinear } from '@visx/scale';
import { Text } from '@visx/text';
import { invoke } from '@tauri-apps/api/core';

interface ScreenTimeData {
  day: string;
  entertainment: number;
  social: number;
  productivity: number;
  other: number;
}

type Category = keyof Omit<ScreenTimeData, 'day'>;

const categories: Category[] = ['entertainment', 'social', 'productivity', 'other'];
const colors: Record<Category, string> = {
  entertainment: '#FF6B6B',
  social: '#4ECDC4',
  productivity: '#45B7D1',
  other: '#96A5A6'
};

const categoryLabels: Record<Category, string> = {
  entertainment: 'Entertainment',
  social: 'Social',
  productivity: 'Productivity',
  other: 'Other'
};

interface Props {
  width: number;
  height: number;
  email: string;
}

interface TooltipData {
  x: number;
  y: number;
  day: string;
  data: ScreenTimeData;
}

const ScreenTimeBarChart = memo(({ width, height, email }: Props) => {
  const ref = React.useRef(null);
  const isInView = useInView(ref, {
    once: true,
    amount: 0.5,  // Only trigger when 50% of the component is visible
    margin: "0px 0px 0px 0px"
  });
  const [hoveredBar, setHoveredBar] = useState<string | null>(null);
  const [tooltipData, setTooltipData] = useState<TooltipData | null>(null);
  const [data, setData] = useState<ScreenTimeData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const response = await invoke<any>('fetch_category_screen_time', { email });
        
        if (response.status === 'success') {
          const days = response.data.days;
          const dates = Object.keys(days).sort();
          
          const processedData: ScreenTimeData[] = dates.map(date => {
            const dayData = days[date];
            const dayName = new Date(date).toLocaleDateString('en-US', { weekday: 'short' });
            
            return {
              day: dayName,
              entertainment: dayData['Entertainment'] || 0,
              social: dayData['Social Networking'] || 0,
              productivity: dayData['Productivity'] || 0,
              other: dayData['Others'] || 0
            };
          });
          
          setData(processedData);
        } else {
          setError('Failed to fetch data');
        }
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to fetch data');
      } finally {
        setIsLoading(false);
      }
    };

    if (email) {
      fetchData();
    }
  }, [email]);

  // Margins
  const margin = { top: 40, right: 30, bottom: 30, left: 60 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Scales
  const yScale = scaleBand({
    range: [0, innerHeight],
    domain: data.map(d => d.day),
    padding: 0.2  // Increased padding for better spacing
  });

  const xScale = scaleLinear({
    range: [0, innerWidth],
    domain: [0, Math.max(...data.map(d => 
      Math.max(d.entertainment, d.social, d.productivity, d.other)
    )) * 1.1],
    nice: true
  });

  // Bar dimensions
  const categoryPadding = 2; // Increased padding between categories
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

  if (!isInView) return <div ref={ref} className="h-full" />;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="animate-pulse text-gray-400 text-sm"
        >
          Loading screen time data...
        </motion.div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-red-500 text-sm font-medium"
        >
          {error}
        </motion.div>
      </div>
    );
  }

  return (
    <div ref={ref} className="relative">
      {/* Legend with original animation */}
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
          {/* Y-axis labels with original fade animation */}
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

          {/* Bars with original staggered animation */}
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
                        rx={8}
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

      {/* Original tooltip implementation */}
      <AnimatePresence>
        {tooltipData && (
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: 5 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 5 }}
            transition={{ duration: 0.15, ease: 'easeOut' }}
            className="fixed z-50 p-2.5 text-[13px] bg-white/95 rounded-lg shadow-sm pointer-events-none border border-gray-100/50 backdrop-blur-sm mb-8"
            style={{
              left: tooltipData.x + 10,
              top: Math.min(tooltipData.y - 10, window.innerHeight - 200), // Ensure tooltip doesn't go off screen
              minWidth: '160px',
              maxWidth: '200px',
              transform: `translateY(${tooltipData.y > window.innerHeight - 200 ? '-100%' : '0'})`
            }}
          >
            <div className="font-medium text-gray-900 mb-2 pb-1.5 border-b border-gray-100">
              {tooltipData.day}
            </div>
            <div className="space-y-2 pt-1">
              {categories.map(category => (
                <div key={category} className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-1.5">
                    <div 
                      className="w-2 h-2 rounded-[2px]"
                      style={{ backgroundColor: colors[category] }}
                    />
                    <span className="text-gray-700 text-[12px] font-medium tracking-tight">
                      {categoryLabels[category]}
                    </span>
                  </div>
                  <span className="font-medium text-[12px] text-gray-900 tabular-nums">
                    {(() => {
                      const hours = Math.floor(tooltipData.data[category]);
                      const minutes = Math.round((tooltipData.data[category] - hours) * 60);
                      return `${hours}h ${minutes}m`;
                    })()}
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