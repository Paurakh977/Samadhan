import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';
import { useRef } from 'react';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

interface AppUsageData {
  appName: string;
  hours: number;
  color: string;
}

interface AppUsageDoughnutChartProps {
  data: AppUsageData[];
}

const AppUsageDoughnutChart = ({ data }: AppUsageDoughnutChartProps) => {
  const chartRef = useRef<ChartJS | null>(null);
  
  // Add Others category with 1.2 hours
  const dataWithOthers = [...data, { appName: "Others", hours: 1.2, color: '#bfdbfe' }];
  
  // Calculate total hours
  const totalHours = dataWithOthers.reduce((sum, app) => sum + app.hours, 0);

  // Calculate percentages
  const appPercentages = dataWithOthers.map(app => ({
    ...app,
    percentage: ((app.hours / totalHours) * 100).toFixed(2)
  }));

  const chartData = {
    labels: appPercentages.map(app => app.appName),
    datasets: [
      {
        data: appPercentages.map(app => app.hours),
        backgroundColor: [
          '#0f3460',  // Dark blue
          '#1a4b8c',  // Medium dark blue
          '#2563eb',  // Primary blue
          '#60a5fa',  // Light blue
          '#93c5fd',  // Lighter blue
          '#bfdbfe',  // Lightest blue for Others
        ],
        hoverBackgroundColor: [
          '#0a2344',  // Darker hover
          '#143a6d',  // Darker hover
          '#1e4fd1',  // Darker hover
          '#4a8ff8',  // Darker hover
          '#7ab3fb',  // Darker hover
          '#a5c7fa',  // Darker hover for Others
        ],
        borderWidth: 1.5,
        borderColor: '#ffffff',
        hoverBorderColor: '#ffffff',
        spacing: 3,
        borderRadius: 2,
        hoverBorderWidth: 1.5,
        hoverOffset: 12
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '80%',
    radius: '93%',
    layout: {
      padding: {
        top: 15,
        right: 15,
        bottom: 15,
        left: 15
      }
    },
    animation: {
      animateRotate: true,
      animateScale: true,
      duration: 600,
      easing: 'easeInOutCubic' as const
    },
    transitions: {
      active: {
        animation: {
          duration: 400,
          easing: 'easeOutCirc' as const
        }
      }
    },
    hover: {
      mode: 'index' as const,
      intersect: true,
      animationDuration: 300
    },
    interaction: {
      mode: 'index' as const,
      intersect: true,
      axis: 'xy' as const
    },
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        enabled: true,
        position: 'nearest' as const,
        backgroundColor: '#ffffff',
        titleColor: '#0f172a',
        bodyColor: '#64748b',
        padding: {
          top: 10,
          right: 14,
          bottom: 10,
          left: 14
        },
        titleMarginBottom: 4,
        bodySpacing: 3,
        titleFont: {
          size: 12,
          family: "'Plus Jakarta Sans', sans-serif",
          weight: 600
        },
        bodyFont: {
          size: 11,
          family: "'Plus Jakarta Sans', sans-serif",
          weight: 500
        },
        displayColors: true,
        boxWidth: 4,
        boxHeight: 4,
        usePointStyle: true,
        cornerRadius: 6,
        caretSize: 0,
        callbacks: {
          title: (tooltipItems: any) => {
            const item = tooltipItems[0];
            const app = appPercentages[item.dataIndex];
            return app.appName;
          },
          label: (context: any) => {
            const app = appPercentages[context.dataIndex];
            const hours = Math.floor(app.hours);
            const minutes = Math.round((app.hours - hours) * 60);
            return [
              `${app.percentage}%`,
              `${hours}h ${minutes}m`
            ];
          },
          labelPointStyle: (context: any) => {
            return {
              pointStyle: 'circle' as const,
              rotation: 0
            };
          }
        }
      }
    }
  };

  return (
    <div className="h-full w-full flex flex-col">
      <div className="relative flex-1">
        <Doughnut 
          ref={(element) => {
            if (element) {
              chartRef.current = element;
            }
          }}
          id="doughnut-chart" 
          data={chartData} 
          options={options} 
        />
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center transition-all duration-700 ease-in-out group">
            <div className="flex items-baseline justify-center transform transition-all duration-700 ease-in-out group-hover:scale-[1.02]">
              <span className="text-[3.25rem] font-semibold text-gray-900 font-['Plus Jakarta Sans'] tracking-tighter leading-none transition-all duration-700 ease-in-out group-hover:text-gray-800">
                {Math.floor(totalHours)}
              </span>
              <span className="text-lg font-medium text-gray-900 font-['Plus Jakarta Sans'] ml-1 transition-all duration-700 ease-in-out group-hover:translate-x-0.5 group-hover:text-gray-800">
                hr
              </span>
            </div>
            <div className="flex items-baseline justify-center mt-1.5 transform transition-all duration-700 ease-in-out group-hover:translate-y-0.5">
              <span className="text-lg font-medium text-gray-400 font-['Plus Jakarta Sans'] transition-all duration-700 ease-in-out group-hover:text-gray-500">
                {Math.round((totalHours - Math.floor(totalHours)) * 60)}
              </span>
              <span className="text-xs font-medium text-gray-400 font-['Plus Jakarta Sans'] ml-1 transition-all duration-700 ease-in-out group-hover:text-gray-500">
                MIN
              </span>
            </div>
            <div className="text-[0.65rem] font-medium text-gray-300 font-['Plus Jakarta Sans'] tracking-wider mt-2 opacity-80 transition-all duration-700 ease-in-out group-hover:opacity-100 group-hover:tracking-widest group-hover:text-gray-400">
              Total Usage
            </div>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap gap-1.5 justify-center mt-5">
        {appPercentages.map((app, index) => (
          <div 
            key={app.appName}
            className="flex items-center gap-2 px-3 py-1.5 bg-zinc-50/40 rounded-md hover:bg-zinc-100/60 transform transition-all duration-700 ease-in-out hover:translate-y-[-1px] hover:shadow-sm cursor-pointer group"
            onMouseEnter={() => {
              if (chartRef.current) {
                const chart = chartRef.current;
                chart.setActiveElements([{datasetIndex: 0, index}]);
                const meta = chart.getDatasetMeta(0);
                const arc = meta.data[index];
                chart.tooltip?.setActiveElements([{datasetIndex: 0, index}], {
                  x: arc.x,
                  y: arc.y - 10
                });
                chart.update();
              }
            }}
            onMouseLeave={() => {
              if (chartRef.current) {
                const chart = chartRef.current;
                chart.setActiveElements([]);
                chart.tooltip?.setActiveElements([], { x: 0, y: 0 });
                chart.update();
              }
            }}
          >
            <div 
              className="w-2 h-2 rounded-full transform transition-all duration-700 ease-in-out group-hover:scale-105"
              style={{ backgroundColor: chartData.datasets[0].backgroundColor[index] }}
            />
            <span className="text-[0.65rem] font-medium text-zinc-600 font-['Plus Jakarta Sans'] tracking-wide transition-all duration-700 ease-in-out group-hover:text-zinc-800 group-hover:tracking-wider group-hover:translate-x-0.5">
              {app.appName}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AppUsageDoughnutChart; 