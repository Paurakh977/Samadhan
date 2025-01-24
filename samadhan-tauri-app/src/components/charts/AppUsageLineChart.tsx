import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import { motion, useInView } from "framer-motion";
import { invoke } from '@tauri-apps/api/core';
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

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface Props {
  email: string;
}

interface AppUsageData {
  appName: string;
  data: number[];
  color: string;
  fillColor?: string;
}

const COLORS = [
  "#059669",  // Green
  "#dc2626",  // Red
  "#2563eb",  // Blue
];

// Add CSS styles
const styles = `
.line-chart-container {
  position: relative;
  height: 280px;
  z-index: 1;
}

#chartjs-tooltip {
  padding: 12px !important;
  min-width: 160px;
}

.tooltip-header {
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid #f1f5f9;
}

.tooltip-day {
  font-size: 13px;
  font-weight: 500;
  color: #334155;
}

.tooltip-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tooltip-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tooltip-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.tooltip-label {
  font-size: 12px;
  color: #64748b;
  flex: 1;
}

.tooltip-value {
  font-size: 12px;
  font-weight: 500;
  color: #334155;
}
`;

// Add styles to document
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement("style");
  styleSheet.innerText = styles;
  document.head.appendChild(styleSheet);
}

const AppUsageLineChart = ({ email }: Props) => {
  const ref = React.useRef(null);
  const isInView = useInView(ref, {
    once: true,
    amount: 0.5,  // Only trigger when 50% of the component is visible
    margin: "0px 0px 0px 0px"
  });
  const [hiddenDatasets, setHiddenDatasets] = useState<string[]>([]);
  const [chartData, setChartData] = useState<AppUsageData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await invoke<any>('fetch_weekly_usage', { email });
        
        if (response.success && response.data && response.data.top_apps) {
          const processedData = response.data.top_apps.map((app: any, index: number) => ({
            appName: app.name,
            data: app.daily_usage.map((day: any) => day.used_time / 3600), // Convert seconds to hours
            color: COLORS[index % COLORS.length],
            fillColor: COLORS[index % COLORS.length] + '20', // Add 12.5% opacity version for fill
          }));
          setChartData(processedData);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [email]);

  const toggleDataset = (appName: string) => {
    setHiddenDatasets(prev => 
      prev.includes(appName) 
        ? prev.filter(name => name !== appName)
        : [...prev, appName]
    );
  };

  if (!isInView) return <div ref={ref} className="h-full" />;

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="space-y-4 w-full animate-pulse">
          <div className="h-[400px] bg-gray-200 rounded-lg"></div>
        </div>
      </div>
    );
  }

  const chartDataConfig = {
    labels: days,
    datasets: chartData.map((app, index) => {
      // Create gradient
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const gradient = ctx?.createLinearGradient(0, 0, 0, 480);
      
      if (gradient) {
        gradient.addColorStop(0, `${app.color}33`);    // 20% opacity at top
        gradient.addColorStop(0.5, `${app.color}1A`);  // 10% opacity in middle
        gradient.addColorStop(1, `${app.color}00`);    // 0% opacity at bottom
      }
      
      const isHidden = hiddenDatasets.includes(app.appName);
      
      return {
        label: app.appName,
        data: app.data,
        borderColor: app.color,
        backgroundColor: gradient,
        fill: true,
        tension: 0.35,
        borderWidth: 2,
        pointRadius: 0,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: app.color,
        pointHoverBorderWidth: 1.5,
        order: chartData.length - index,
        hidden: isHidden,
      };
    }),
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'nearest' as const,
      axis: 'x' as const,
      intersect: false,
    },
    animation: {
      duration: 750,
      easing: 'easeInOutCubic' as const,
      delay: (context: any) => context.dataIndex * 100
    },
    transitions: {
      active: {
        animation: {
          duration: 400
        }
      }
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        enabled: true,
        backgroundColor: '#ffffff',
        titleColor: '#0f172a',
        bodyColor: '#334155',
        borderColor: '#f1f5f9',
        borderWidth: 1,
        padding: 16,
        titleFont: {
          size: 14,
          weight: 600,
          family: "'Inter', sans-serif"
        },
        bodyFont: {
          size: 13,
          weight: 500,
          family: "'Inter', sans-serif"
        },
        cornerRadius: 8,
        displayColors: false,
        position: 'nearest' as const,
        animation: {
          duration: 200,
          easing: 'easeOutCubic' as const
        },
        callbacks: {
          title: function(context: any) {
            return context[0].label;
          },
          label: function(context: any) {
            const hours = Math.floor(context.parsed.y);
            const minutes = Math.round((context.parsed.y - hours) * 60);
            return `${context.dataset.label}: ${hours}h ${minutes}m`;
          },
        },
      },
      filler: {
        propagate: true
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
        border: {
          display: false,
        },
        ticks: {
          font: {
            size: 12,
            weight: 500,
            family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
          },
          color: '#64748b',
          padding: 10,
        }
      },
      y: {
        min: 0,
        max: 6,
        border: {
          display: false,
        },
        grid: {
          color: 'rgba(241, 245, 249, 0.5)',
          lineWidth: 1,
          drawBorder: false,
          tickLength: 0,
        },
        ticks: {
          count: 3,
          font: {
            size: 12,
            weight: 500,
            family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
          },
          color: '#64748b',
          padding: 16,
          maxTicksLimit: 6,
          callback: function(value: number | string) {
            return value === 0 ? '' : `${value}h`;
          },
        }
      }
    },
    elements: {
      line: {
        tension: 0.32
      },
      point: {
        hitRadius: 8,
        hoverRadius: 4,
        hoverBorderWidth: 2,
        borderWidth: 2,
      }
    },
    hover: {
      mode: 'nearest' as const,
      intersect: false,
      animationDuration: 200
    }
  };

  return (
    <div ref={ref} className="relative h-full">
      <div className="absolute top-0 right-0 flex items-center gap-3">
        {chartData.map((app) => {
          return (
            <motion.button
              key={app.appName}
              onClick={() => toggleDataset(app.appName)}
              className={`flex items-center gap-2 px-2.5 py-1.5 rounded-md transition-all ${
                hiddenDatasets.includes(app.appName)
                  ? 'bg-zinc-50/80 text-zinc-400'
                  : 'bg-zinc-50/50 text-zinc-600 hover:bg-zinc-50/80'
              }`}
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
            >
              <div className="relative w-6 h-2.5 rounded-sm overflow-hidden">
                <div 
                  className="absolute inset-0 opacity-25"
                  style={{ backgroundColor: app.color }}
                />
                <div 
                  className="absolute inset-0"
                  style={{ 
                    background: `linear-gradient(to bottom, ${app.color}40, ${app.color}00)`,
                  }}
                />
              </div>
              <span className="text-[11px] font-medium tracking-wide">{app.appName}</span>
            </motion.button>
          );
        })}
      </div>
      <div className="h-full pt-12">
        <Line data={chartDataConfig} options={options} />
      </div>
    </div>
  );
};

export default AppUsageLineChart; 