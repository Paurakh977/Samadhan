import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

interface WeeklyUsageData {
  day: string;
  hours: number;
  minutes: number;
}

interface WeeklyUsageBarChartProps {
  data: WeeklyUsageData[];
}

const WeeklyUsageBarChart = ({ data }: WeeklyUsageBarChartProps) => {
  const chartData = {
    labels: data.map(item => item.day),
    datasets: [
      {
        data: data.map(item => item.hours + item.minutes / 60),
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