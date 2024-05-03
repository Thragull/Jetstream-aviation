import React, { useContext, useState, useEffect } from "react";
import { Context } from "../../store/appContext";
import CreateFlight from "./CrewControllerComponents/CreateFlight";
import SelectComponent from "./reusableComponents/SelectComponent";
import FlightsTable from "./CrewControllerComponents/FlightsTable";
import InputComponent from "./reusableComponents/InputComponent";


export const CrewControllerComponent = () => {
	const { store, actions } = useContext(Context);
    const [createFlight, setCreateFlight] = useState(false)
    const [flights, setFlights] = useState([])
    const [fleet, setFleet] = useState([])
    const [inflightEmployees, setInflightEmployees] = useState([])
    const [airports, setAirports] = useState([])
    const [roles, setRoles] = useState([])
    const [selectedRole, setSelectedRole] = useState(null)
    const [selectedEmployee, setSelectedEmployee] = useState(null)
    const [filterFlight, setFilterFlight] = useState({
        departure_id: null,
        arrival_id: null,
        aircraft_id: null, 
    })
    

    const filterFlights = async () => {
        let apicall = process.env.BACKEND_URL + `/api/flights?`
        let moreThan1Filter = false
        let flightsData 
        
        
        for (let key in filterFlight) {
            if (filterFlight[key] != null && filterFlight[key]!= NaN) {
                if(moreThan1Filter == true) {
                    apicall = apicall + `&${key}=${filterFlight[key]}` 
                }
                else {
                    apicall = apicall + `${key}=${filterFlight[key]}`
                }
                moreThan1Filter = true
                console.log(apicall)
            }
        }
        try{
            const resp = await fetch(
                apicall
            )
            flightsData = await resp.json()
            console.log(flights)
        }
        catch (error) {
            console.log(error)
        }
        for (let i = 0; i<flightsData.length; i++)  {
            const departureAirport = await actions.getAirportById(flightsData[i].departure);
            flightsData[i].departure = departureAirport;
            const arrivalAirport = await actions.getAirportById(flightsData[i].arrival)
            flightsData[i].arrival = arrivalAirport
            
            
        }
        setFlights(flightsData)
        console.log(`Actualizado: ${JSON.stringify(flights)}`)
    }

    const handleFilter = (event) => {
       
        const {name, value} = event.target
        let parsedValue
        if (isNaN(value)) {
            parsedValue = value
        }
        else { parsedValue = parseInt(value)}
        setFilterFlight({...filterFlight, [name]: parsedValue})
        console.log(filterFlight)
    }


    const handleEmployee = (event) => {
        let name
        setSelectedEmployee(event.target.value)
        selectedEmployee == 3 ?
        name = "cpt"
        :
        selectedEmployee == 4 ? 
        name = 'fo' : 
        selectedEmployee == 5 || selectedEmployee == 6 ? 
        name = 'cc2'
        : name = null
        return name
    }

    const roleFilter = async (value) => {
        setSelectedRole(value)
        console.log(value)
        if(value != null && value != undefined) {
        const employees = await actions.getEmployeesByRol(value)
        setInflightEmployees(employees)
        console.log(employees)
        }
    }

    useEffect(() => {
        const fecthAircrafts = async () => {
            const fleetData = await actions.getAllFleet()
            setFleet(fleetData)
            console.log(fleetData)
        }
        const fetchRoles = async () => {
            const roleData = await actions.getRoles()
            setRoles(roleData)
        }
        const fecthAirports = async () => {
            const airportsData = await actions.getAirports()
            setAirports(airportsData)
        }
        fecthAircrafts()
        fecthAirports()
        filterFlights()
        fetchRoles()
    }, [])

    useEffect(() => {
        filterFlights()
    }, [filterFlight])

   
    

	return (
        <div>
            <h1>Crew Controller</h1>
            {createFlight ? <CreateFlight/> : 
                <div>
                    <div>
                        <div className="row">
                            <div className="col-6">
                                <SelectComponent 
                                label="Aircraft"
                                name="aircraft_id"
                                selectLabel="Filter by aircraft"
                                onChange={handleFilter}
                                map={() => (
                                    fleet.map((aircraft) => (
                                         <option key={aircraft.id} value={aircraft.id}>{aircraft.registration}</option>
                                    ))
                                )}
                                />
                            </div>
                            <div className="col-5">
                                <InputComponent label="Flight Number" name="flight_number" handleScript={handleFilter}/>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-6">
                                <SelectComponent 
                                    label="Departure Airport"
                                    name="departure_id"
                                    selectLabel="Filter by Departure Airport"
                                    onChange={handleFilter}
                                    map={() => (
                                        airports.map((airport) => (
                                             <option  key={airport.id} value={airport.id}>{`${airport.airport} ${airport.IATA}`}
                                             </option>
                                        ))
                                    )}
                                />
                            </div>
                            <div className="col-6">
                                <SelectComponent 
                                label="Arrival Airport"
                                name="arrival_id"
                                selectLabel="Filter by Arrival Airport"
                                onChange={handleFilter}
                                map={() => (
                                    airports.map((airport) => (
                                         <option key={airport.id} value={airport.id}>{`${airport.airport}`}</option>
                                    ))
                                )}
                                />
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-6">
                            <SelectComponent 
                                label="Inflight"
                                name="employee_id"
                                value={selectedRole}
                                selectLabel="role"
                                onChange={(event) => roleFilter(event.target.value)} // Pasar el valor seleccionado como argumento
                                map={() => (
                                    roles.map((role) => (
                                        <option key={role.id} value={role.id}>{`${role.role}`}</option>
                                    ))
                                )}
                            />
                            </div>
                            <div className="col-6">
                            <SelectComponent 
                                    label="Inflight"
                                    name={selectedRole}
                                    selectLabel="Filter by Employee"
                                    onChange={handleFilter}
                                    map={() => (
                                        inflightEmployees.length == 0 ? <option>No role selected</option> : 
                                        inflightEmployees.map((employee) => (
                                             <option key={employee.id} value={employee.id}>{`${employee.name} ${employee.surname}`}</option>
                                        ))
                                    )}
                                />
                            </div>
                        </div>
                    </div>
                    <div className="mx-2">
                        <FlightsTable
                            map = {() => (
                                flights.length == 0 ? 
                                    <td>No flights match the criteria</td>
                                : 
                                flights.map((flight, index) => (
                                    <tr key={index + 1}>
                                        <th scope="row">{index + 1}</th>
                                        <td>{flight.aircraft}</td>
                                        <td>{flight.departure}</td>
                                        <td>{flight.arrival}</td>
                                        <td>{flight.departure_UTC}</td>
                                        <td>{flight.arrival_UTC}</td>
                                        <td>{flight.flight_number}</td>
                                    </tr>
                                ))
                            )}    
                        />
                    </div>
                    <button  type="button" onClick={()=> setCreateFlight(!createFlight)} className="btn btn-success">Create new Flight</button>
                </div>}      
        </div>
	);
};

export default CrewControllerComponent; 