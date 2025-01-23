import React, { useState } from 'react';
import ReactCalendar from 'react-calendar';
import '../styles/calendar.css';
import { motion, AnimatePresence } from 'framer-motion';
import { Value } from 'react-calendar/dist/cjs/shared/types';

interface CalendarProps {
  isExpanded: boolean;
}

interface Event {
  id: string;
  date: Date;
  startTime: string;
  endTime: string;
  title: string;
  description: string;
}

function CalendarComponent({ isExpanded }: CalendarProps) {
  const [date, setDate] = useState(new Date());
  const [showEventForm, setShowEventForm] = useState(false);
  const [events, setEvents] = useState<Event[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [newEvent, setNewEvent] = useState({
    startTime: '',
    endTime: '',
    title: '',
    description: ''
  });
  
  const handleDateChange = (value: Date | null) => {
    if (value instanceof Date) {
      setDate(value);
      setSelectedDate(value);
    }
  };

  const handleAddEvent = () => {
    if (!selectedDate) return;
    setShowEventForm(true);
  };

  const handleSaveEvent = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedDate) return;

    const event: Event = {
      id: Math.random().toString(36).substr(2, 9),
      date: selectedDate,
      ...newEvent
    };

    setEvents([...events, event]);
    setShowEventForm(false);
    setNewEvent({ startTime: '', endTime: '', title: '', description: '' });
  };

  const getEventsForDate = (date: Date) => {
    return events.filter(event => 
      event.date.toDateString() === date.toDateString()
    );
  };

  const tileContent = ({ date }: { date: Date }) => {
    const dateEvents = getEventsForDate(date);
    if (dateEvents.length > 0) {
      return (
        <div className="multiple-dots">
          {Array.from({ length: Math.min(dateEvents.length, 3) }).map((_, i) => (
            <div key={i} className="dot" />
          ))}
        </div>
      );
    }
    return null;
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('en-US', { 
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      weekday: 'long'
    }).toUpperCase();
  };

  return (
    <div className="main-content">
      <div className="calendar-container">
        <div className="calendar-header">
          <div className="calendar-title-section">
            <h2 className="calendar-title">
              {date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
              <div className="month-nav">
                <button onClick={() => {
                  const newDate = new Date(date);
                  newDate.setMonth(date.getMonth() - 1);
                  setDate(newDate);
                }}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M15 18l-6-6 6-6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
                <button onClick={() => {
                  const newDate = new Date(date);
                  newDate.setMonth(date.getMonth() + 1);
                  setDate(newDate);
                }}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 18l6-6-6-6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
              </div>
            </h2>
            <p className="calendar-subtitle">
              Here all your planned events. You will find information for each event as well you can planned new one.
            </p>
          </div>
        </div>

        <ReactCalendar
          onChange={handleDateChange}
          value={date}
          className="react-calendar"
          tileContent={tileContent}
          prev2Label={null}
          next2Label={null}
          minDetail="month"
          showNavigation={false}
          activeStartDate={date}
          formatShortWeekday={(locale: string | undefined, date: Date) => 
            ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'][date.getDay() === 0 ? 6 : date.getDay() - 1]
          }
        />
      </div>
      
      <div className="events-container">
        <div className="notification-toggle">
          <div>
            <div className="notification-title">Notifications</div>
            <div className="notification-description">Notifies when deadline is near</div>
          </div>
          <label className="toggle-switch">
            <input type="checkbox" />
            <span className="toggle-slider"></span>
          </label>
        </div>

        <div className="events-header">
          <div className="current-date">
            {selectedDate ? formatDate(selectedDate) : formatDate(new Date())}
          </div>
          <button className="add-event-button" onClick={handleAddEvent}>Add event</button>
        </div>
        
        <div className="events-list">
          {selectedDate && getEventsForDate(selectedDate).map(event => (
            <div key={event.id} className="event">
              <div className="event-time">{event.startTime} - {event.endTime}</div>
              <div className="event-title">{event.title}</div>
              <div className="event-description">{event.description}</div>
            </div>
          ))}
        </div>
      </div>

      <AnimatePresence>
        {showEventForm && (
          <motion.div 
            className="event-form-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setShowEventForm(false)}
          >
            <motion.div 
              className="event-form"
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              onClick={e => e.stopPropagation()}
            >
              <h2>Add New Event</h2>
              <form onSubmit={handleSaveEvent}>
                <div className="time-inputs">
                  <div className="form-group">
                    <label>Start Time</label>
                    <input 
                      type="time" 
                      required
                      value={newEvent.startTime}
                      onChange={e => setNewEvent({...newEvent, startTime: e.target.value})}
                    />
                  </div>
                  <div className="form-group">
                    <label>End Time</label>
                    <input 
                      type="time" 
                      required
                      value={newEvent.endTime}
                      onChange={e => setNewEvent({...newEvent, endTime: e.target.value})}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label>Event Title</label>
                  <input 
                    type="text" 
                    required
                    value={newEvent.title}
                    onChange={e => setNewEvent({...newEvent, title: e.target.value})}
                    placeholder="Enter event title"
                  />
                </div>
                <div className="form-group">
                  <label>Description</label>
                  <textarea 
                    rows={3}
                    value={newEvent.description}
                    onChange={e => setNewEvent({...newEvent, description: e.target.value})}
                    placeholder="Enter event description"
                  />
                </div>
                <button type="submit" className="save-button">Save Event</button>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default CalendarComponent; 