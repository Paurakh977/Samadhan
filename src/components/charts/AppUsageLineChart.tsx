import { useState, useRef, useEffect } from "react";
import { Line } from "react-chartjs-2";
import { motion } from "framer-motion";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from "chart.js";

const AppUsageLineChart = ({ data, chartData, options }) => {
  const [hiddenDatasets, setHiddenDatasets] = useState<string[]>([]);
  const chartRef = useRef<ChartJS<"line">>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  useEffect(() => {
    const handleResize = () => {
      if (chartRef.current) {
        setTimeout(() => {
          chartRef.current?.resize();
          chartRef.current?.update('none');
        }, 0);
      }
    };

    const resizeObserver = new ResizeObserver(handleResize);
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    window.addEventListener('resize', handleResize);

    return () => {
      resizeObserver.disconnect();
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const toggleDataset = (appName) => {
    if (hiddenDatasets.includes(appName)) {
      hiddenDatasets.splice(hiddenDatasets.indexOf(appName), 1);
    } else {
      hiddenDatasets.push(appName);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="h-full flex flex-col"
    >
      <motion.div 
        className="flex flex-wrap items-center gap-2 sm:gap-4 mb-4"
        layout="position"
      >
        {data.map((app) => {
          const isHidden = hiddenDatasets.includes(app.appName);
          return (
            <motion.button
              key={app.appName}
              onClick={() => toggleDataset(app.appName)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className={`flex items-center shrink-0 ${
                isHidden ? 'opacity-40' : 'opacity-100'
              } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-100 rounded-full px-1`}
            >
              <motion.div 
                className={`w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full mr-1.5 sm:mr-2 border ${
                  isHidden ? 'border-gray-300' : 'border-[1.5px]'
                }`}
                style={{ borderColor: isHidden ? undefined : app.color }}
                animate={{ 
                  scale: isHidden ? 0.9 : 1,
                  opacity: isHidden ? 0.5 : 1
                }}
                transition={{ duration: 0.2 }}
              />
              <motion.span 
                className={`text-xs sm:text-[13px] font-medium text-slate-600 tracking-wide ${
                  isHidden ? 'line-through decoration-1 text-slate-400' : ''
                }`}
                animate={{ 
                  opacity: isHidden ? 0.6 : 1,
                }}
                transition={{ duration: 0.2 }}
              >
                {app.appName}
              </motion.span>
            </motion.button>
          );
        })}
      </motion.div>
      <motion.div 
        ref={containerRef}
        className="relative flex-1 h-[calc(100%-3rem)]"
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Line 
          data={chartData} 
          options={{
            ...options,
            maintainAspectRatio: false,
            responsive: true,
            scales: {
              ...options.scales,
              x: {
                ...options.scales.x,
                ticks: {
                  ...options.scales.x.ticks,
                  autoSkip: true,
                  maxRotation: 0,
                  padding: 8,
                  font: {
                    size: window.innerWidth < 640 ? 11 : 13,
                    weight: 500,
                    family: "'Inter', sans-serif"
                  }
                }
              },
              y: {
                ...options.scales.y,
                ticks: {
                  ...options.scales.y.ticks,
                  font: {
                    size: window.innerWidth < 640 ? 11 : 13,
                    weight: 500,
                    family: "'Inter', sans-serif"
                  }
                }
              }
            }
          }} 
          ref={chartRef}
          redraw={false}
        />
      </motion.div>
    </motion.div>
  );
};

export default AppUsageLineChart; 