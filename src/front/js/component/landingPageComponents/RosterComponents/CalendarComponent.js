import React, { useContext, useState, useEffect } from "react";
import { Context } from "../../../store/appContext";
import { Calendar, dayjsLocalizer } from "react-big-calendar";
import 'react-big-calendar/lib/css/react-big-calendar.css'
import "./calendarstyle.css"
import dayjs from "dayjs";
import { faDraftingCompass } from "@fortawesome/free-solid-svg-icons/faDraftingCompass";


export const CalendarComponent = (props) => {
	const { store, actions } = useContext(Context);
    const localizer = dayjsLocalizer(dayjs);
    const [currentView, setCurrentView] = useState('month');
    const [selectedDay, setSelectedDay] = useState(new Date(), 'day')
    const [roster, setRoster] = useState([])
    const [events, setEvents] = useState([])
    const [duties, setDuties] = useState([])
    const dayOffColor = 'rgb(255,0,0,0.5)'
    const flightColor = 'rgba(13, 232, 13, 0.362)'
    const standbyColor = 'rgba(255, 166, 0, 0.537)'

    const FlightInfoComponent = (props) => {
        return (
        <div style={{display: 'flex', width: '25vw' }}>
            <div style={{color: 'red', width: '10vw', textAlign: 'start'}}>{`${props.label}:   `}</div>
            <div>{`${props.info}`}</div>
        </div>
        )
    }



    const fetchRoster =  async () => {
        const rosterData = await actions.getEmployeeRoster(store.loggedInEmployee.id)
        setRoster(rosterData)
    }

    const arrangeEvents = async () => {
        const updatedEvents = [...events];
        console.log(roster);
    
        for (const item of roster) {
            const newEvent = {};
            const duty = await actions.getDutiesById(item.duty); // Esperar a que se resuelva la promesa
            let combinedStartDateTime;
            let combinedEndDateTime;
            if(item.duty == 10) {
                for (const [key, value] of Object.entries(item)) {
                    const flightEvent = {}
                    // Iterar sobre cada entrada del objeto item
                    if (key.toLowerCase().includes("flight") && value!=null) {
                        console.log(key)
                        // Verificar si la clave incluye la palabra "flight"
                        const flight = await actions.getFlightById(value);
                        console.log(flight)
                        const departureAirport = await actions.getAirportDataById(flight.departure)
                        const arrivalAirport = await actions.getAirportDataById(flight.arrival)
                        const firstOfficer = await actions.getEmployeeById(flight.fo)
                        console.log(firstOfficer.name)
                        const senior = await actions.getEmployeeById(flight.sccm)
                        const cc2 = await actions.getEmployeeById(flight.cc2)
                        const cc3 = await actions.getEmployeeById(flight.cc3)
                        const cc4 = await actions.getEmployeeById(flight.cc4)
                        combinedStartDateTime = `${flight.date}T${flight.departure_LT}`;
                        combinedEndDateTime = `${flight.date}T${flight.arrival_LT}`;
                        flightEvent.start = dayjs(combinedStartDateTime).toDate();
                        flightEvent.end = dayjs(combinedEndDateTime).toDate();
                        flightEvent.title = flight.flight_number
                        flightEvent.iata = `${departureAirport.IATA} - ${arrivalAirport.IATA}`
                        flightEvent.departure_LT = flight.departure_LT
                        flightEvent.departure_UTC = flight.departure_UTC
                        flightEvent.arrival_UTC = flight.arrival_UTC
                        flightEvent.arrival_LT = flight.arrival_LT
                        flightEvent.fo = `${firstOfficer.name} ${firstOfficer.surname}`;
                        flightEvent.senior = `${senior.name} ${senior.surname}`;
                        flightEvent.cc2 = `${cc2.name} ${cc2.surname}`;
                        flightEvent.cc3 = `${cc3.name} ${cc3.surname}`;
                        flightEvent.cc4 = `${cc4.name} ${cc4.surname}`;

                        
                        
                        updatedEvents.push(flightEvent)

                        // Aquí puedes realizar las acciones adicionales necesarias para los vuelos
                    }
            }}else {
            if (item.check_in_LT === "None") {
                combinedStartDateTime = `${item.date}T00:00:00`;
                combinedEndDateTime = `${item.date}T23:59:59`;
            } else {
                combinedStartDateTime = `${item.date}T${item.check_in_LT}`;
                combinedEndDateTime = `${item.date}T${item.check_out_LT}`;
            }
            newEvent.start = dayjs(combinedStartDateTime).toDate();
            newEvent.end = dayjs(combinedEndDateTime).toDate();
            newEvent.title = duty;
            newEvent.subtitle = 'NFLT'
            console.log(newEvent);
            
            updatedEvents.push(newEvent);}
        }
    
        setEvents(updatedEvents);
    };
    

    useEffect(() => {
        fetchRoster()  
    }, [])

    useEffect(() => {
        if(roster.length > 0) {
            arrangeEvents()
        }
      }, [roster])
    
      useEffect(() => {
        console.log(events)
      }, [events])
  
  


    const handleViewChange = (view) => {
      setCurrentView(view);
        };

    const handleNavigate = (date, view) => {
        if(currentView == 'day') {
            console.log(date.toString())
            setSelectedDay(date)
        }
    }

     /* events = [
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
        
        
    ] */

    const components = {
        event: props => {

            return props.title.includes('J') ? 
            <div style={{
                padding: '0px' ,
                height: '15vh', 
                width: '20vw', 
                backgroundColor: props.title == 'SBYM' ? standbyColor : props.title == 'OFFD' ? dayOffColor : flightColor,
            
            }}>{props.title}</div>

            : 

            <div style={{
                padding: '0px' ,
                height: '15vh' ,
                width: '20vw', 
                backgroundColor: props.title == 'SBYM' ? standbyColor : props.title == 'OFFD' ? dayOffColor : flightColor,
            
            }}>{props.title}</div>

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
                                <div className="my-4 mx-5 accordion-item" key={index} style={{backgroundColor: 'rgba(255,255,255,0.3)'}}>
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
                                            {event.title}.    {event.iata}
                                        </button>
                                    </h2>
                                    <div
                                        id={`collapse-${index}`}
                                        className="accordion-collapse collapse show"
                                        aria-labelledby={`heading-${index}`}
                                        data-bs-parent="#accordionExample"
                                    >
                                        <div className="accordion-body">
                                            <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                                <div>
                                                    <FlightInfoComponent label="Departure LT" info={event.departure_LT} />
                                                    <FlightInfoComponent label="Departure UTC" info={event.departure_UTC} />
                                                </div>
                                                <div>
                                                    <FlightInfoComponent label="Departure LT" info={event.arrival_LT} />
                                                    <FlightInfoComponent label="Departure UTC" info={event.arrival_UTC} />
                                                </div>
                                            </div>
                                            <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                                <FlightInfoComponent label="First officer" info={event.fo} />
                                                <FlightInfoComponent label="Senior" info={event.senior} />
                                            </div>
                                            <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                                <FlightInfoComponent label="Crew 2" info={event.fo} />
                                                <FlightInfoComponent label="Crew 3" info={event.cc3} />
                                            </div>
                                            <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                                <FlightInfoComponent label="Crew 4" info={event.cc4} />                                                
                                            </div>
                                            
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