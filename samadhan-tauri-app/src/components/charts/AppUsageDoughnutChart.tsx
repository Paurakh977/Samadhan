import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';
import { useRef, useEffect, useState } from 'react';
import UltraModernDropdown from '../UltraModernDropdown';
import { invoke } from '@tauri-apps/api/core';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

interface AppUsageData {
  name: string;
  used_time: number;
  color?: string;
}

interface ChartDataItem {
  name: string;
  value: number;
  color: string;
  minutes: number;
}

interface ProcessedData {
  [key: string]: {
    apps: AppUsageData[];
    total_time: number;
  };
}

interface Props {
  email: string;
}

interface CachedData {
  today: { apps: AppUsageData[], total_time: number };
  yesterday: { apps: AppUsageData[], total_time: number };
  this_week: { apps: AppUsageData[], total_time: number };
}

const COLORS = [
  '#0f3460',  // Dark blue
  '#1a4b8c',  // Medium dark blue
  '#2563eb',  // Primary blue
  '#60a5fa',  // Light blue
  '#93c5fd',  // Lighter blue
];

const AppUsageDoughnutChart: React.FC<Props> = ({ email }) => {
  const chartRef = useRef<ChartJS | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<'today' | 'yesterday' | 'this_week'>('today');
  const [cachedData, setCachedData] = useState<CachedData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!email) {
        setError('No email provided');
        setIsLoading(false);
        return;
      }

      try {
        console.log('Fetching data for email:', email);
        // Clear existing cache on component mount
        sessionStorage.removeItem(`app_usage_all_${email}`);

        // Fetch fresh data from API
        const response = await invoke<{
          success: boolean;
          data: {
            data: {
              today: { apps: AppUsageData[], total_time: number };
              yesterday: { apps: AppUsageData[], total_time: number };
              this_week: { apps: AppUsageData[], total_time: number };
            };
          };
          error?: string;
        }>('fetch_all_app_usage', { email });

        console.log('API Response:', response);

        if (response.success && response.data) {
          const rawData = response.data.data; // Access the nested data object
          console.log('Raw data:', rawData);
          
          // Process the data and convert seconds to hours
          const processData = (periodData: { apps: AppUsageData[], total_time: number }) => {
            return {
              apps: periodData.apps.map((app, index) => ({
                name: app.name,
                used_time: app.used_time,
                color: COLORS[index % COLORS.length]
              })),
              total_time: periodData.total_time
            };
          };

          const processedData = {
            today: processData(rawData.today),
            yesterday: processData(rawData.yesterday),
            this_week: processData(rawData.this_week)
          };

          console.log('Processed data:', processedData);
          setCachedData(processedData);
        } else {
          console.error('API Error:', response.error);
          setError(response.error || 'No data available');
        }
      } catch (error) {
        console.error('Error fetching app usage data:', error);
        setError('Failed to fetch data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [email]);

  const currentData = cachedData?.[selectedPeriod];
  const currentApps = currentData?.apps || [];
  
  // Convert seconds to hours for each app
  const appsInHours = currentApps.map(app => ({
    name: app.name,
    hours: app.used_time / 3600, // Convert seconds to hours
    color: app.color || COLORS[currentApps.indexOf(app) % COLORS.length]
  }));

  // Sort apps by usage and get top 5
  appsInHours.sort((a, b) => b.hours - a.hours);
  const top5Apps = appsInHours.slice(0, 5);
  
  // Calculate Others category
  const otherApps = appsInHours.slice(5);
  const othersHours = otherApps.reduce((sum, app) => sum + app.hours, 0);
  
  // Combine top 5 with Others
  const dataWithOthers = [
    ...top5Apps,
    ...(otherApps.length > 0 ? [{
      name: "Others",
      hours: othersHours,
      color: '#bfdbfe' // Light blue for Others
    }] : [])
  ];
  
  // Calculate total hours
  const totalHours = dataWithOthers.reduce((sum, app) => sum + app.hours, 0);

  // Calculate percentages and format data for chart
  const chartData = dataWithOthers.map(app => ({
    name: app.name,
    value: Number(((app.hours / totalHours) * 100).toFixed(1)),
    color: app.color,
    hours: app.hours
  }));

  // Calculate display hours and minutes from total
  const displayHours = Math.floor(totalHours);
  const displayMinutes = Math.round((totalHours - displayHours) * 60);

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
            return chartData[item.dataIndex].name;
          },
          label: (context: any) => {
            const app = chartData[context.dataIndex];
            const hours = Math.floor(app.hours);
            const minutes = Math.round((app.hours - hours) * 60);
            return [
              `${app.value}%`,
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

  const data = {
    labels: chartData.map(app => app.name),
    datasets: [{
      data: chartData.map(app => app.value),
      backgroundColor: chartData.map(app => app.color),
      borderWidth: 1.5,
      borderColor: '#ffffff',
      hoverBorderColor: '#ffffff',
      spacing: 3,
      borderRadius: 2,
      hoverBorderWidth: 1.5,
      hoverOffset: 12
    }]
  };

  return (
    <div className="h-full w-full flex flex-col">
      <div className="flex justify-end mb-4">
        <UltraModernDropdown 
          value={selectedPeriod}
          onChange={(value) => setSelectedPeriod(value as typeof selectedPeriod)}
        />
      </div>
      <div className="relative flex-1">
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="flex items-center justify-center h-full text-red-500">
            {error}
          </div>
        ) : currentData ? (
          <Doughnut 
            ref={(element) => {
              if (element) {
                chartRef.current = element;
              }
            }}
            data={data}
            options={options}
          />
        ) : null}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center transition-all duration-700 ease-in-out group">
            <div className="flex items-baseline justify-center transform transition-all duration-700 ease-in-out group-hover:scale-[1.02]">
              <span className="text-[3.25rem] font-semibold text-gray-900 font-['Plus Jakarta Sans'] tracking-tighter leading-none transition-all duration-700 ease-in-out group-hover:text-gray-800">
                {displayHours}
              </span>
              <span className="text-lg font-medium text-gray-900 font-['Plus Jakarta Sans'] ml-1 transition-all duration-700 ease-in-out group-hover:translate-x-0.5 group-hover:text-gray-800">
                hr
              </span>
            </div>
            <div className="flex items-baseline justify-center mt-1.5 transform transition-all duration-700 ease-in-out group-hover:translate-y-0.5">
              <span className="text-2xl font-medium text-gray-600 font-['Plus Jakarta Sans'] tracking-tight leading-none transition-all duration-700 ease-in-out group-hover:text-gray-700">
                {displayMinutes}
              </span>
              <span className="text-sm font-medium text-gray-600 font-['Plus Jakarta Sans'] ml-1 transition-all duration-700 ease-in-out group-hover:text-gray-700">
                MIN
              </span>
            </div>
            <div className="text-sm font-medium text-gray-400 mt-1 transition-all duration-700 ease-in-out group-hover:text-gray-500">
              Total Usage
            </div>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap gap-1.5 justify-center mt-5">
        {chartData.map((app, index) => (
          <div 
            key={app.name}
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
              style={{ backgroundColor: app.color }}
            />
            <span className="text-[0.65rem] font-medium text-zinc-600 font-['Plus Jakarta Sans'] tracking-wide transition-all duration-700 ease-in-out group-hover:text-zinc-800 group-hover:tracking-wider group-hover:translate-x-0.5">
              {app.name}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AppUsageDoughnutChart; 