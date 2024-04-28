import React, {useState, useContext, useEffect, useRef } from "react";
import { Context } from "../../../store/appContext";
import InputComponent from "../reusableComponents/InputComponent";
<script src="https://cdnjs.cloudflare.com/ajax/libs/air-datepicker/2.2.3/js/i18n/datepicker.en.js"></script>



export const EditProfile = (props) => {
   
    const { store, actions } = useContext(Context);
    const datepickerRef = useRef(null);

    const [countries, setCountries] = useState([]);
    const [selectedCountry, setSelectedCountry] = useState(null)
    const [selectedNationality, setSelectedNationality] = useState(null)
    const [states, setStates] = useState([])
    const [nationalities, setNationalities] = useState([])
    const [editedProfile, setEditedProfile] = useState(store.loggedInEmployee)

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        // Si el nombre es 'state', 'country', o 'nationality', convierte el valor a entero
        let parsedValue = value;
        if (name === 'state' || name === 'country' || name === 'nationality') {
            parsedValue = parseInt(value);
        }
        setEditedProfile({ ...editedProfile, [name]: parsedValue });
        console.log(editedProfile);
    };



    useEffect(()=> {
        const fetchCountries = async () => {
            const countriesData = await actions.getCountries();
            setCountries(countriesData);
        };
        const fetchNationalities = async() => {
            const nationalitiesData = await actions.getNationalities();
            setNationalities(nationalitiesData)
            
        }
    
        fetchCountries();
        fetchNationalities();


    },[]);



    const handleCountryChange = async (event) => {
        const countryValue = event.target.value
        setSelectedCountry(event.target.value)
        if (selectedCountry != null) {
            const statesData = await actions.getStates(countryValue);
            setStates(statesData)
            console.log(states)
        } 
    }


    const editEmployee = async () => {
        const authToken = localStorage.getItem("jwt-token");
        try {
            const response = await fetch(`${process.env.BACKEND_URL}/api/employee?id=${store.loggedInEmployee.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${authToken}`
                },
                body: JSON.stringify(editedProfile),
            });
            if (response.ok) {
                console.log("Employee successfully added to database");
                // Limpiar el formulario o realizar cualquier otra acción necesaria
            } else {
                const data = await response.json();
                console.error(data.msg);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    };

    

    return (
        <div>
            <h1 className="mb-5">Edit Profile</h1>
            <div style={{display: "flex"}}>
                <InputComponent label="Name" placeholder={store.loggedInEmployee.name} name="name" handleScript = {handleInputChange}/> 
                <InputComponent label="Sirame" placeholder={store.loggedInEmployee.surname} name="surname" handleScript = {handleInputChange}/> 
            </div>
            <div className="mx-3 mb-3" style={{display: 'flex'}}>
                <span className=" me-1 input-group-text" id="basic-addon1">Birth Date</span>
                <input type='date' id='dateInput'></input>
            </div>
            <div style={{display: "flex"}}>
                <InputComponent label="Phone Number" placeholder="Phone Number" name="phone_number"/> 
                <span className="input-group-text" id="basic-addon1" style={{height: '6vh', fontSize: '2vh'}} >Nationality</span>
                        <select 
                            className="form-select form-select-lg mb-3" 
                            aria-label="Large select example" 
                            style={{height: '6vh', fontSize: '2vh'}}
                            value={selectedNationality}
                            name = "nationality"
                            onChange={handleInputChange}
                            >
                            <option selected>Select a nationality</option>
                            {
                                nationalities.map((nationality, index)=> (
                                    <option key={index} value={nationality.id}>{nationality.nationality}</option>
                                ))
                            }
                        </select>
            </div>
            <div style={{display: "flex"}}>
                <InputComponent label="Address" placeholder="Address" name="address" handleScript={handleInputChange}/> 
            </div>
            <div className="row">
                <div className="col-6 mb-3 mx-3" style={{display: "flex", height: '6vh'}}>
                    <span className="input-group-text" id="basic-addon1">Country</span>
                        <select 
                            className="form-select form-select-lg mb-3" 
                            aria-label="Large select example" 
                            style={{height: '6vh', fontSize: '1vw'}}
                            value={selectedCountry}
                            onChange={(event)=> {
                                handleCountryChange(event)
                                handleInputChange(event)
                            }}
                            name = "country"
                            >
                            <option selected>Select a country</option>
                            {
                                countries.map((country, index)=> (
                                    <option key={index} value={country.id}>{country.country}</option>
                                ))
                            }
                        </select>
                </div>
                <div className="col-6 mb-3 mx-3" style={{display: "flex", height: '6vh'}}>
                    <span className="input-group-text" id="basic-addon1">State</span>
                    <select 
                    className="form-select form-select-lg mb-3" 
                    aria-label="Large select example" 
                    style={{height: '6vh', fontSize: '2vh'}}
                    name="state"
                    onChange={handleInputChange}
                    >
                            <option selected>Select a State</option>
                            {selectedCountry != null ? 
                            states.map((state, index)=> (
                                <option key={index} value={state.id}>{state.state}</option>
                            )) : <option>Select a country first</option>}
                    </select>
                </div>
            </div>
            <div style={{display: "flex"}}>
                 <InputComponent label="City" placeholder="city" name="city" handleScript={handleInputChange} /> 
            </div>
            <div className="my-5">
                <button onClick={()=> {
                    editEmployee()}} 
                    type="button" className="btn btn-warning">Save changes</button>
            </div>
        </div>
    );
};

export default EditProfile;
