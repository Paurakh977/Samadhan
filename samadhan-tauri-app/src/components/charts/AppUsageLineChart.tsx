import { useState } from "react";
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

interface AppUsageData {
  appName: string;
  data: number[];
  color: string;
  fillColor?: string;
}

interface AppUsageLineChartProps {
  data: AppUsageData[];
}

const AppUsageLineChart = ({ data }: AppUsageLineChartProps) => {
  const [hiddenDatasets, setHiddenDatasets] = useState<string[]>([]);
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  const toggleDataset = (appName: string) => {
    setHiddenDatasets(prev => 
      prev.includes(appName) 
        ? prev.filter(name => name !== appName)
        : [...prev, appName]
    );
  };

  const chartData = {
    labels: days,
    datasets: data.map((app, index) => {
      const ctx = document.createElement('canvas').getContext('2d');
      const gradient = ctx?.createLinearGradient(0, 0, 0, 280);
      if (gradient) {
        gradient.addColorStop(0, `${app.color}20`);  // Darker at top (12.5% opacity)
        gradient.addColorStop(0.5, `${app.color}10`); // Medium fade in middle (6.25% opacity)
        gradient.addColorStop(1, `${app.color}00`);   // Completely transparent at bottom
      }
      
      const isHidden = hiddenDatasets.includes(app.appName);
      
      return {
        label: app.appName,
        data: app.data,
        borderColor: app.color,
        backgroundColor: gradient || 'transparent',
        fill: true,
        tension: 0.35,
        borderWidth: 1.5,
        pointRadius: 0,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: app.color,
        pointHoverBorderWidth: 1.5,
        order: data.length - index,
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
            return `${context.dataset.label}: ${context.parsed.y}h`;
          },
        },
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
    <div className="relative h-full">
      <div className="absolute top-0 right-0 flex items-center gap-3">
        {data.map((app) => {
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
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default AppUsageLineChart; 