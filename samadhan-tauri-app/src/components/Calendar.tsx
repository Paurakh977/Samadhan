import React from 'react';
import { motion } from 'framer-motion';
import Calendar from 'react-calendar'; // Make sure to install react-calendar
import '../styles/calendar.css'; // Import custom styles

const CalendarComponent: React.FC = () => {
  const [date, setDate] = React.useState(new Date());
  const [events, setEvents] = React.useState([
    {
      time: "11:00 - 11:30 AM",
      title: "Review work place safety",
      location: "Grev Margitgatan 6, Stockholm",
    },
    {
      time: "1:00 - 1:30 PM",
      title: "Team alignment",
      location: "Video call",
    },
    {
      time: "2:00 - 2:30 PM",
      title: "Lunch with Sabrina",
      location: "Starbucks",
    },
    {
      time: "3:00 - 4:30 PM",
      title: "Meeting with clients",
      location: "Office",
    },
  ]);

  return (
    <motion.div 
      className="bg-white rounded-lg shadow-lg border border-gray-200 p-6 h-full"
      initial={{ opacity: 0, y: -20 }} 
      animate={{ opacity: 1, y: 0 }} 
      transition={{ duration: 0.5 }}
    >
      <h2 className="text-gray-900 text-lg font-bold mb-2">Calendar</h2>
      <p className="text-gray-500 text-sm mb-4">Manage your daily activities and events.</p>
      <div className="flex flex-col md:flex-row h-full">
        <div className="w-full md:w-1/2">
          <Calendar
            onChange={setDate}
            value={date}
            className="react-calendar"
            style={{
              border: 'none',
              width: '100%',
              borderRadius: '8px',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
            }}
          />
        </div>
        <div className="w-full md:w-1/2 pl-0 md:pl-4 h-full">
          <h3 className="text-md font-semibold">Events for {date.toLocaleDateString()}</h3>
          <div className="mt-2 h-full overflow-y-auto">
            {events.map((event, index) => (
              <motion.div 
                key={index} 
                className="bg-gray-100 p-4 rounded-md mb-2 shadow-md"
                initial={{ opacity: 0, y: 10 }} 
                animate={{ opacity: 1, y: 0 }} 
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <p className="text-sm font-medium">{event.time}</p>
                <p className="text-sm">{event.title}</p>
                <p className="text-xs text-gray-500">{event.location}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default CalendarComponent; 