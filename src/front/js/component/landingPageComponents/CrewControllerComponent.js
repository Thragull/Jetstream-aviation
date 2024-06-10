import React, { useContext, useState, useEffect } from "react";
import { Context } from "../../store/appContext";
import CreateFlight from "./CrewControllerComponents/CreateFlight";
import SelectComponent from "./reusableComponents/SelectComponent";
import FlightsTable from "./CrewControllerComponents/FlightsTable";
import InputComponent from "./reusableComponents/InputComponent";
import "./CrewControllerComponents/crew_controler.css";

export const CrewControllerComponent = () => {
    const { store, actions } = useContext(Context);
    const [createFlight, setCreateFlight] = useState(false);
    const [flights, setFlights] = useState([]);
    const [fleet, setFleet] = useState([]);
    const [inflightEmployees, setInflightEmployees] = useState([]);
    const [airports, setAirports] = useState([]);
    const [roles, setRoles] = useState([]);
    const [selectedRole, setSelectedRole] = useState(null);
    const [selectedEmployee, setSelectedEmployee] = useState(null);
    const [filterFlight, setFilterFlight] = useState({
        departure_id: null,
        arrival_id: null,
        aircraft_id: null,
    });

    const filterFlights = async () => {
        let apicall = process.env.BACKEND_URL + `/api/flights?`;
        let moreThan1Filter = false;
        let flightsData;
        const authToken = localStorage.getItem("jwt-token");

        for (let key in filterFlight) {
            if (filterFlight[key] != null && !isNaN(filterFlight[key])) {
                if (moreThan1Filter) {
                    apicall += `&${key}=${filterFlight[key]}`;
                } else {
                    apicall += `${key}=${filterFlight[key]}`;
                }
                moreThan1Filter = true;
            }
        }
        try {
            const resp = await fetch(apicall, {
                headers: {
                    Authorization: `Bearer ${authToken}`,
                },
            });
            flightsData = await resp.json();
        } catch (error) {
            console.log(error);
        }
        for (let i = 0; i < flightsData.length; i++) {
            const departureAirport = await actions.getAirportById(
                flightsData[i].departure
            );
            flightsData[i].departure = departureAirport;
            const arrivalAirport = await actions.getAirportById(
                flightsData[i].arrival
            );
            flightsData[i].arrival = arrivalAirport;
        }
        setFlights(flightsData);
    };

    const handleFilter = (event) => {
        const { name, value } = event.target;
        const parsedValue = isNaN(value) ? value : parseInt(value);
        setFilterFlight({ ...filterFlight, [name]: parsedValue });
    };

    const handleEmployee = (event) => {
        let name;
        setSelectedEmployee(event.target.value);
        switch (selectedEmployee) {
            case 3:
                name = "cpt";
                break;
            case 4:
                name = "fo";
                break;
            case 5:
            case 6:
                name = "cc2";
                break;
            default:
                name = null;
        }
        return name;
    };

    const roleFilter = async (value) => {
        setSelectedRole(value);
        if (value != null && value != undefined) {
            const employees = await actions.getEmployeesByRol(value);
            setInflightEmployees(employees);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            const fleetData = await actions.getAllFleet();
            const airportsData = await actions.getAirports();
            const rolesData = await actions.getRoles();
            setFleet(fleetData);
            setAirports(airportsData);
            setRoles(rolesData);
            filterFlights();
        };
        fetchData();
    }, []);

    useEffect(() => {
        filterFlights();
    }, [filterFlight]);

    return (
        <div className="container">
            {createFlight ? (
                <CreateFlight />
            ) : (
                <div>
                    <div className="row mb-4">
                        <div className="col-md-6">
                            <SelectComponent
                                label="Aircraft"
                                name="aircraft_id"
                                selectLabel="Filter by aircraft"
                                onChange={handleFilter}
                                map={() =>
                                    fleet.map((aircraft) => (
                                        <option
                                            key={aircraft.id}
                                            value={aircraft.id}
                                        >
                                            {aircraft.registration}
                                        </option>
                                    ))
                                }
                            />
                        </div>
                        <div className="col-md-6">
                            <InputComponent
                                label="Flight Number"
                                name="flight_number"
                                handleScript={handleFilter}
                            />
                        </div>
                    </div>
                    <div className="row mb-4">
                        <div className="col-md-6">
                            <SelectComponent
                                label="Departure Airport"
                                name="departure_id"
                                selectLabel="Filter by Departure Airport"
                                onChange={handleFilter}
                                map={() =>
                                    airports.map((airport) => (
                                        <option
                                            key={airport.id}
                                            value={airport.id}
                                        >
                                            {`${airport.airport} ${airport.IATA}`}
                                        </option>
                                    ))
                                }
                            />
                        </div>
                        <div className="col-md-6">
                            <SelectComponent
                                label="Arrival Airport"
                                name="arrival_id"
                                selectLabel="Filter by Arrival Airport"
                                onChange={handleFilter}
                                map={() =>
                                    airports.map((airport) => (
                                        <option
                                            key={airport.id}
                                            value={airport.id}
                                        >
                                            {`${airport.airport}`}
                                        </option>
                                    ))
                                }
                            />
                        </div>
                    </div>
                    <div className="row mb-4">
                        <div className="col-md-6">
                            <SelectComponent
                                label="Inflight"
                                name="role_id"
                                selectLabel="Filter by Role"
                                onChange={(event) =>
                                    roleFilter(event.target.value)
                                }
                                map={() =>
                                    roles.map((role) => (
                                        <option
                                            key={role.id}
                                            value={role.id}
                                        >
                                            {`${role.role}`}
                                        </option>
                                    ))
                                }
                            />
                        </div>
                        <div className="col-md-6">
                            <SelectComponent
                                label="Inflight"
                                name="employee_id"
                                selectLabel="Filter by Employee"
                                onChange={handleFilter}
                                map={() =>
                                    inflightEmployees.length === 0 ? (
                                        <option>No role selected</option>
                                    ) : (
                                        inflightEmployees.map((employee) => (
                                            <option
                                                key={employee.id}
                                                value={employee.id}
                                            >
                                                {`${employee.name} ${employee.surname}`}
                                            </option>
                                        ))
                                    )
                                }
                            />
                        </div>
                    </div>
                    <div className="row mb-4">
                        <div className="col-md-12">
                            <FlightsTable
                                map={() =>
                                    flights.length === 0 ? (
                                        <tr>
                                            <td colSpan="7">
                                                No flights match the criteria
                                            </td>
                                        </tr>
                                    ) : (
                                        flights.map((flight, index) => (
                                            <tr key={index + 1}>
                                                <th scope="row">
                                                    {index + 1}
                                                </th>
                                                <td>{flight.aircraft}</td>
                                                <td>{flight.departure}</td>
                                                <td>{flight.arrival}</td>
                                                <td>{flight.departure_UTC}</td>
                                                <td>{flight.arrival_UTC}</td>
                                                <td>{flight.flight_number}</td>
                                            </tr>
                                        ))
                                    )
                                }
                            />
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-12">
                            <button
                                type="button"
                                onClick={() => setCreateFlight(!createFlight)}
                                className="btn btn-primary create-button"
                            >
                                Create new Flight
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CrewControllerComponent;
