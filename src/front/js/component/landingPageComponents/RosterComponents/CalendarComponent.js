import React, { useContext, useState, useEffect } from "react";
import { Context } from "../../../store/appContext";
import { Calendar, dayjsLocalizer } from "react-big-calendar";
import 'react-big-calendar/lib/css/react-big-calendar.css'
import "./calendarstyle.css"
import dayjs from "dayjs";


export const CalendarComponent = (props) => {
	const { store, actions } = useContext(Context);
    const localizer = dayjsLocalizer(dayjs);
    const [currentView, setCurrentView] = useState('month');
    const [selectedDay, setSelectedDay] = useState(new Date(), 'day')
    const handleViewChange = (view) => {
      setCurrentView(view);
        };

    const handleNavigate = (date, view) => {
        if(currentView == 'day') {
            console.log(date.toString())
            setSelectedDay(date)
        }
    }



    const events = [
        {
            start: dayjs('2024-04-13T10:00:00').toDate(),
            end: dayjs('2024-04-13T13:30:00').toDate(), 
            title: 'MAD-BCN',
             subtitle: 'hello' 
        },
        {
                    start: dayjs('2024-04-13T14:00:00').toDate(),
            end: dayjs('2024-04-13T16:30:00').toDate(), 
            title: 'MAD-VLC',
        },
        {
            start: dayjs('2024-04-16T14:00:00').toDate(),
            end: dayjs('2024-04-16T16:30:00').toDate(), 
            title: 'MAD-VLC',
        }
        
    ]

    const components = {
        event: props => {
            return <div>{props.title}</div>
        }
    }

	return (
        <div>
            <div className="calendarContainer " style={{height: currentView == 'agenda' || currentView == 'month' ? '70vh' : '12vh'}}>
                <div className="mx-5 mt-3" style={{height: currentView == 'agenda' || currentView == 'month' ? '70vh' : '5vh'}}>
                    <Calendar
                        localizer = {localizer}
                        events={events}
                        views={["month", "day", "agenda"]}
                        components={components}
                        timeslots={1}
                        step={60}
                        onView={(view) => handleViewChange(view)}
                        onNavigate={(date, view) => handleNavigate(date, view)}
                    />
                </div>
            </div>
            { currentView == 'day' ? 
            <div className="mt-0">
                <h2 style={{ position: "relative", zIndex: 2 }}>Itinerary</h2>
                <div>
                    {events.filter(event => dayjs(event.start).isSame(selectedDay, 'day'))
                        .map((event, index)=> {
                            return (
                                <div className="my-4 mx-5 accordion-item" key={index} style={{backgroundColor: 'yellow'}}>
                                    <h2 className="accordion-header" style={{}}>
                                        <button
                                            className="accordion-button"
                                            type="button"
                                            data-bs-toggle="collapse"
                                            data-bs-target={`#collapse-${index}`}
                                            aria-expanded="true"
                                            aria-controls={`collapse-${index}`}
                                            style={{
                                                backgroundColor: 'white'
                                            }}
                                        >
                                            {event.title}
                                        </button>
                                    </h2>
                                    <div
                                        id={`collapse-${index}`}
                                        className="accordion-collapse collapse show"
                                        aria-labelledby={`heading-${index}`}
                                        data-bs-parent="#accordionExample"
                                    >
                                        <div className="accordion-body">
                                            {event.subtitle}
                                        </div>
                                    </div>
                                </div>
)
})}
                </div>
            </div>
            :
            <div></div>
}
         </div>


        
	);
};

export default CalendarComponent; 