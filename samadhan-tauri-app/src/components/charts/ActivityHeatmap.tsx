import { useState, useCallback, memo } from 'react';
import HeatMap from '@uiw/react-heat-map';
import type { MouseEvent } from 'react';
import { heatmapData as defaultData } from '../../data/heatmapData';
import { motion, AnimatePresence } from 'framer-motion';
import '../../styles/heatmap.css';

interface ActivityHeatmapProps {
  data?: { date: string; count: number }[];
}

const LegendItem = memo(({ color }: { color: string }) => (
  <div
    className="w-[10px] h-[10px] rounded-sm"
    style={{ backgroundColor: color }}
  />
));

LegendItem.displayName = 'LegendItem';

const Tooltip = memo(({ show, text, x, y }: { show: boolean; text: string; x: number; y: number }) => (
  <AnimatePresence>
    {show && (
      <motion.div 
        initial={{ opacity: 0, y: 5 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 5 }}
        transition={{ duration: 0.15 }}
        className="fixed z-50 px-3 py-2 text-xs font-light text-white bg-gray-900/90 rounded-md shadow-lg backdrop-blur-sm pointer-events-none transform -translate-x-1/2"
        style={{ 
          left: x,
          top: y - 35,
        }}
      >
        {text}
      </motion.div>
    )}
  </AnimatePresence>
));

Tooltip.displayName = 'Tooltip';

const ActivityHeatmap = ({ data = defaultData }: ActivityHeatmapProps) => {
  const [tooltip, setTooltip] = useState({ show: false, text: '', x: 0, y: 0 });

  const formatDate = useCallback((date: string) => {
    const d = new Date(date);
    return d.toLocaleDateString('en-US', { 
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });
  }, []);

  const handleMouseEnter = useCallback((ev: MouseEvent<SVGRectElement>) => {
    const element = ev.currentTarget;
    const rect = element.getBoundingClientRect();
    const date = element.getAttribute('data-date');
    
    if (!date) return;
    
    const dataPoint = data.find(d => d.date === date);
    const count = dataPoint?.count ?? 0;
    
    const text = count === 0 
      ? `No goals on ${formatDate(date)}` 
      : `${count} ${count === 1 ? 'goal' : 'goals'} on ${formatDate(date)}`;
    
    setTooltip({
      show: true,
      text,
      x: rect.left + window.scrollX + rect.width / 2,
      y: rect.top + window.scrollY
    });
  }, [data, formatDate]);

  const handleMouseLeave = useCallback(() => {
    setTooltip({ show: false, text: '', x: 0, y: 0 });
  }, []);

  const legendColors = ['#ebedf0', '#0E4429', '#006D32', '#26A641', '#39D353'];

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="space-y-4 p-6 bg-white rounded-lg shadow-sm"
    >
      <h3 className="text-lg font-medium text-gray-900 mb-4">Activity Contributions</h3>

      <div className="w-full overflow-x-auto">
        <div className="w-full max-w-[780px] mx-auto activity-heatmap">
          <HeatMap
            value={data}
            width="100%"
            rectSize={10}
            space={3}
            startDate={new Date(2025, 0, 1)}
            endDate={new Date(2025, 11, 31)}
            legendCellSize={0}
            rectProps={{
              rx: 2,
              onMouseEnter: handleMouseEnter,
              onMouseLeave: handleMouseLeave
            }}
            panelColors={{
              0: '#ebedf0',   // Level 0: 0 goals (gray)
              1: '#0E4429',   // Level 1: 1-2 goals (darkest)
              2: '#006D32',   // Level 2: 3-4 goals
              3: '#26A641',   // Level 3: 4-5 goals
              4: '#39D353'    // Level 4: 6+ goals
            }}  
            weekLabels={['', 'Mon', '', 'Wed', '', 'Fri', '']}
            monthLabels={['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}
            style={{
              color: '#9CA3AF',
              fontSize: '11px',
              fontFamily: 'Inter, system-ui, sans-serif',
              fontWeight: 300
            }}
          />
          
          <div className="flex items-center gap-2 text-[11px] text-[#57606a] mt-2 ml-[580px]">
            <span className="font-light">Less</span>
            <div className="flex gap-[3px]">
              {legendColors.map((color) => (
                <LegendItem key={color} color={color} />
              ))}
            </div>
            <span className="font-light">More</span>
          </div>
        </div>
      </div>

      <Tooltip {...tooltip} />
    </motion.div>
  );
};

export default memo(ActivityHeatmap); 