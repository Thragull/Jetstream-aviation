import React, { useContext, useState, useEffect } from "react";
import { Context } from "../../../store/appContext";
import InputComponent from "../reusableComponents/InputComponent";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlaneDeparture } from '@fortawesome/free-solid-svg-icons'


export const CreateFlight = () => {
	const { store, actions } = useContext(Context);
    const [countries, setCountries] = useState([])
    const [departureCountry, setDepartureCountry] = useState(undefined)
    const [arrivalCountry, setArrivalCountry] = useState(null)
    const [departureAirports, setDepartureAirports] = useState([])
    const [arrivalAirports, setArrivalAirports] = useState([])
    const [fleet, setFleet] = useState([])
    const [captains, setCaptains] = useState([])
    const [firstOfficers, setFirstOfficers] = useState([])
    const [seniors, setSeniors] = useState([])
    const [crew, setCrew] = useState([])
    const [flight, setFlight] = useState({})
    
    const handleInputChange = (event) => {
        const { name, value } = event.target;
        let parsedValue = value; // Inicialmente, asumimos que el valor es una cadena
    
        // Verificar si el valor es un número
        if (!isNaN(value)) {
            // Si es un número, realizar la conversión a entero y convertirlo a cadena
            parsedValue = parseInt(value).toString();
        }
    
        // Verificar si parsedValue es una cadena y contiene ':'
        if (typeof parsedValue === 'string' && parsedValue.includes(":")) {
            // Si contiene ':', añadir ':00' al final para convertirlo en un formato HH:MM:SS
            parsedValue += ":00";
        } 
    
        // Actualizar el estado del componente con el valor parseado
        setFlight({ ...flight, [name]: parsedValue });
        console.log(flight);
    };
    
    

    useEffect(()=> {
        const fetchCountries = async () => {
            const countriesData = await actions.getCountries();
            setCountries(countriesData);
        };
        const fetchFleet = async () => {
            const fleetData = await actions.getAllFleet();
            setFleet(fleetData);
        };
        const fetchCaptains = async () => {
            const captainsData = await actions.getEmployeesByRol(3)
            setCaptains(captainsData)
            
        }
        const fetchFirstOfficers = async () => {
            const firstOfficersData = await actions.getEmployeesByRol(4)
            setFirstOfficers(firstOfficersData)
            
        }
        const fetchSeniors = async () => {
            const seniorsData = await actions.getEmployeesByRol(5)
            setSeniors(seniorsData)
            
        }
        const fecthCabinCrew = async () => {
            const cabincrewData = await actions.getEmployeesByRol(6)
            setCrew(cabincrewData)
        }
        fetchCountries();
        fetchFleet();
        fetchCaptains();
        fetchFirstOfficers();
        fetchSeniors();
        fecthCabinCrew();



    },[]);

    useEffect(()=> {
        if(departureCountry !== null) {
            handleDepartureCountryChange()
        }
        if(arrivalCountry !== null) {
            handleArrivalCountryChange()
        }
    },[departureCountry]);

    const handleDepartureCountryChange = async (countryValue) => {
        setDepartureCountry(countryValue);
        if (countryValue) {
            const airportsData = await actions.getAirportsByCountry(countryValue);
            setDepartureAirports(airportsData);
        }
    };

    const handleArrivalCountryChange = async (countryValue) => {
        setArrivalCountry(countryValue);
        if (countryValue) {
            const airportsData = await actions.getAirportsByCountry(countryValue);
            setArrivalAirports(airportsData);
        }
    };
    
    const postFlight = async () => {
        try {
            const response = await fetch(`${process.env.BACKEND_URL}/api/flights`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(flight),
                mode: 'cors'
            });
            if (response.ok) {
                console.log("Flight added to database");
                // Limpiar el formulario o realizar cualquier otra acción necesaria
            } else {
                const data = await response.json();
                console.error(data.msg);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }

	return (
        <div>
            <h4>Create Flight</h4>
                <form>
                    <div className="my-4" style={{display: "flex", justifyContent: "space-evenly"}}>
                        <div>
                            <span className="input-group-text" id="basic-addon1" style={{height: '4vh', fontSize: '1vw'}} >Departure Country</span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '6vh', fontSize: '1vw'}}
                                name = "country"
                                value={departureCountry}
                                onChange={(event)=>handleDepartureCountryChange(event.target.value)}
                                >
                                <option selected>Departure Country</option>
                                {
                                    countries.map((country, index)=> (
                                        <option key={index} value={country.id}>{country.country}</option>
                                    ))
                                }
                            </select>
                            <span className="input-group-text" id="basic-addon1" style={{height: '4vh', fontSize: '1vw'}}>
                                  Departure Airport <i className=" mx-4 fas fa-plane-departure"></i>
                            </span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '6vh', fontSize: '1vw'}}
                                name = "departure_id"
                                onChange={handleInputChange}
                                
                                >
                                <option selected>Departure Airports</option>
                                {
                                    departureAirports.map((airport, index)=> (
                                        <option key={index} value={airport.id}>{`${airport.airport} ${airport.IATA}`}</option>
                                    ))
                                }
                            </select>
                        </div>
                        <div>
                            <span className="input-group-text"  style={{height: '4vh', fontSize: '1vw'}} >Arrival Country</span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '6vh', fontSize: '1vw'}}
                                name = "country"
                                value={arrivalCountry}
                                onChange={(event)=>handleArrivalCountryChange(event.target.value)}
                                >
                                <option selected>Arrival Country</option>
                                {
                                    countries.map((country, index)=> (
                                        <option key={index} value={country.id}>{country.country}</option>
                                    ))
                                }
                            </select>
                            <span className="input-group-text" id="basic-addon1" style={{height: '4vh', fontSize: '1vw'}}>
                                Departure Airport <i className=" mx-4 fas fa-plane-arrival"></i> 
                            </span>

                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '6.3vh', fontSize: '1vw'}}
                                name = "arrival_id"
                                onChange={handleInputChange}
                                
                                >
                                <option selected>Arrival Airports</option>
                                {
                                    arrivalAirports.map((airport, index)=> (
                                        <option key={index} value={airport.id}>{`${airport.airport} ${airport.IATA}`}</option>
                                    ))
                                }
                            </select>
                        </div>
                    </div>
                    <div style={{display: "flex", justifyContent: "space-between"}}>
                    <span className="input-group-text"  style={{height: '4vh', fontSize: '1vw'}} >Aircraft</span>
                    <select 
                        className="form-select form-select-lg mb-3" 
                        aria-label="Large select example" 
                        style={{height: '4vh', fontSize: '0.9vw', textAlign: "initial"}}
                        name = "aircraft_id"
                        onChange={handleInputChange}
                        >
                        <option selected>Aircraft</option>
                        {
                            fleet.map((airplane, index)=> (
                                <option key={index} value={airplane.id}>{`${airplane.registration}`}</option>
                            ))
                        }
                    </select>
                    <span className="ms-2 input-group-text"  style={{height: '4vh', fontSize: '1vw'}} >Captain</span>
                    <select 
                        className="form-select form-select-lg mb-3" 
                        aria-label="Large select example" 
                        style={{height: '4vh', fontSize: '0.9vw'}}
                        name = "cpt_id"
                        onChange={handleInputChange}
                        >
                        <option selected>Select captain</option>
                        {
                            captains.map((captain, index)=> (
                                <option key={index} value={captain.id}>{`${captain.name} ${captain.surname}`}</option>
                            ))
                        }
                    </select> 
                    </div>
                    <div style={{display: "flex", justifyContent: "space-between"}}>
                    <span className="input-group-text"  style={{height: '4vh', fontSize: '1vw'}} >First Officer</span>
                    <select 
                        className="me-2 form-select form-select-lg mb-3" 
                        aria-label="Large select example" 
                        style={{height: '4vh', fontSize: '0.9vw'}}
                        name = "fo_id"
                        onChange={handleInputChange}
                        >
                        <option selected>First Officer</option>
                        {
                            firstOfficers.map((firstOfficer, index)=> (
                                <option key={index} value={firstOfficer.id}>{`${firstOfficer.name} ${firstOfficer.surname}`}</option>
                            ))
                        }
                    </select>
                    <span className="input-group-text"  style={{height: '4vh', fontSize: '0.9vw'}} >Senior</span>
                    <select 
                        className="form-select form-select-lg mb-3" 
                        aria-label="Large select example" 
                        style={{height: '4vh', fontSize: '0.9vw'}}
                        name = "sccm_id"
                        onChange={handleInputChange}
                        >
                        <option selected>Select Senior</option>
                        {
                            seniors.map((senior, index)=> (
                                <option key={index} value={senior.id}>{`${senior.name} ${senior.surname}`}</option>
                            ))
                        }
                    </select>
                    </div>
                    <div style={{display: "flex", justifyContent: "space-between"}}>
                        <span className="input-group-text"  style={{height: '4vh', fontSize: '1vw'}} >Cabin Crew 2</span>
                        <select 
                            className="form-select form-select-lg mb-3" 
                            aria-label="Large select example" 
                            style={{height: '4vh', fontSize: '0.9vw'}}
                            name = "cc2_id"
                            onChange={handleInputChange}
                            >
                            <option selected>Select</option>
                            {
                                crew.map((crew2, index)=> (
                                    <option key={index} value={crew2.id}>{`${crew2.name} ${crew2.surname}`}</option>
                                ))
                            }
                        </select>
                        <span className="input-group-text"  style={{height: '4vh', fontSize: '1vw'}} >Cabin Crew 3</span>
                        <select 
                            className="form-select form-select-lg mb-3" 
                            aria-label="Large select example" 
                            style={{height: '4vh', fontSize: '0.9vw'}}
                            name = "cc3_id"
                            onChange={handleInputChange}
                            >
                            <option selected>Select</option>
                            {
                                crew.map((crew3, index)=> (
                                    <option key={index} value={crew3.id}>{`${crew3.name} ${crew3.surname}`}</option>
                                ))
                            }
                        </select>
                        <span className="input-group-text"  style={{height: '4vh', fontSize: '1vw'}} >Cabin Crew 4</span>
                        <select 
                            className="form-select form-select-lg mb-3" 
                            aria-label="Large select example" 
                            style={{height: '4vh', fontSize: '0.9vw'}}
                            name = "cc4_id"
                            onChange={handleInputChange}
                            >
                            <option selected>Select</option>
                            {
                                crew.map((crew4, index)=> (
                                    <option key={index} value={crew4.id}>{`${crew4.name} ${crew4.surname}`}</option>
                                ))
                            }
                        </select>
                    </div>
                    <div style={{display: "flex"}}>
                        <InputComponent label="Flight number" placeholder="Flight number" name="flight_number" handleScript={handleInputChange}/>
                        <div style={{display: "flex", width: "50vw"}}>
                        <span className=" me-1 input-group-text" id="basic-addon1">Date</span>
                        <input name="date" onChange={handleInputChange} type='date' id='dateInput'></input>
                        </div>
                    </div>
                    <div style={{display: "flex"}}>
                        <div>
                            <div className="me-2" style={{display: "flex", fontSize: "1vw"}}>
                                <span className="input-group-text" id="basic-addon1" style={{fontSize: "1vw", width: "8vw"}}>Dep UTC</span>    
                                <input name="departure_UTC" onChange={handleInputChange}  type='time' id='timeInput'></input>
                            </div>
                            <div className="me-2" style={{display: "flex",  fontSize: "1vw"}}>
                                <span className="input-group-text" style={{fontSize: "1vw", width: "8vw"}} id="basic-addon1">Dep LT</span>    
                                <input name="departure_LT" onChange={handleInputChange} type='time' id='timeInput'></input>
                            </div>
                        </div>    
                        <div>
                            <div className="ms-2" style={{display: "flex",  fontSize: "1vw"}}>
                                <span className="input-group-text" style={{fontSize: "1vw", width: "8vw"}} id="basic-addon1">Arr UTC</span>    
                                <input name="arrival_UTC" onChange={handleInputChange} type='time' id='timeInput'></input>
                            </div>
                            <div className="ms-2" style={{display: "flex", fontSize: "1vw"}}>
                                <span className="input-group-text" style={{fontSize: "1vw", width: "8vw"}} id="basic-addon1">Arr LT</span>    
                                <input name="arrival_LT" onChange={handleInputChange}  type='time' id='timeInput'></input>
                            </div>
                        </div> 
                    </div>
                </form>
                <button type="button" onClick={postFlight} className="mt-5 btn btn-success">Create FLight</button>
        </div>
	);
};

export default CreateFlight; 