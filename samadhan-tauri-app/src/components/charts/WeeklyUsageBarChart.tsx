import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from 'chart.js';
import { useEffect, useState } from 'react';
import { invoke } from '@tauri-apps/api/core';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

interface Props {
  email: string;
}

interface DayData {
  date: string;
  day: string;
  total_time: number;
}

interface AppData {
  name: string;
  total_time: number;
  daily_usage: Array<{
    date: string;
    day: string;
    used_time: number;
  }>;
}

interface WeeklyData {
  days: DayData[];
  top_apps: AppData[];
}

const WeeklyUsageBarChart: React.FC<Props> = ({ email }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [weeklyData, setWeeklyData] = useState<WeeklyData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!email) {
        setError('No email provided');
        setIsLoading(false);
        return;
      }

      try {
        const response = await invoke<any>('fetch_weekly_usage', { email });
        
        if (response.success && response.data) {
          setWeeklyData(response.data);
        } else {
          setError('No data available');
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to fetch data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [email]);

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="space-y-4 w-full animate-pulse">
          <div className="flex justify-between space-x-4">
            {[...Array(7)].map((_, i) => (
              <div key={i} className="flex-1">
                <div className="h-40 bg-gray-200 rounded-lg mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-full"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center text-red-500">
        {error}
      </div>
    );
  }

  if (!weeklyData || !weeklyData.days || weeklyData.days.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        No data available
      </div>
    );
  }

  const chartData = {
    labels: weeklyData.days.map(day => day.day.slice(0, 3)),
    datasets: [
      {
        data: weeklyData.days.map(day => day.total_time / 3600), // Convert seconds to hours
        backgroundColor: '#6355f1',
        hoverBackgroundColor: '#5346e8',
        borderRadius: 12,
        borderSkipped: false,
        barThickness: 24,
        maxBarThickness: 32,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 750,
      easing: 'easeInOutQuart' as const,
      delay: (context: any) => context.dataIndex * 100,
    },
    layout: {
      padding: {
        top: 20,
        right: 15,
        bottom: 0,
        left: 15
      }
    },
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        backgroundColor: 'white',
        titleColor: '#18181b',
        bodyColor: '#3f3f46',
        bodySpacing: 4,
        padding: 10,
        borderColor: '#f4f4f5',
        borderWidth: 1,
        boxShadow: '0 2px 4px -1px rgb(0 0 0 / 0.05)',
        bodyFont: {
          size: 11,
          family: "'Inter', system-ui, sans-serif",
          weight: 500,
        },
        titleFont: {
          size: 11,
          family: "'Inter', system-ui, sans-serif",
          weight: 600,
        },
        displayColors: false,
        callbacks: {
          title: (context: any) => context[0].label,
          label: (context: any) => {
            const hours = Math.floor(context.raw);
            const minutes = Math.round((context.raw - hours) * 60);
            return `${hours}h ${minutes}m`;
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
          drawBorder: false,
        },
        ticks: {
          font: {
            size: 11,
            family: "'Inter', system-ui, sans-serif",
            weight: 500,
          },
          color: '#71717a',
          padding: 8,
        },
        border: {
          display: false,
        }
      },
      y: {
        min: 0,
        max: 8,
        border: {
          display: false,
        },
        grid: {
          color: '#fafafa',
          drawBorder: false,
          lineWidth: 1,
        },
        ticks: {
          font: {
            size: 11,
            family: "'Inter', system-ui, sans-serif",
            weight: 500,
          },
          color: '#71717a',
          padding: 10,
          stepSize: 2,
          callback: (value: any) => value === 0 ? '' : `${value}h`,
        },
      },
    },
  };

  return (
    <div className="h-full w-full">
      <Bar 
        data={chartData} 
        options={options} 
      />
    </div>
  );
};

export default WeeklyUsageBarChart; 