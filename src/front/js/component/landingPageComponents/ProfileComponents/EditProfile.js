import React, {useState, useContext, useEffect, useRef } from "react";
import { Context } from "../../../store/appContext";
import InputComponent from "../reusableComponents/InputComponent";
<script src="https://cdnjs.cloudflare.com/ajax/libs/air-datepicker/2.2.3/js/i18n/datepicker.en.js"></script>



export const EditProfile = (props) => {
   
    const { store, actions } = useContext(Context);
    const datepickerRef = useRef(null);

    const [countries, setCountries] = useState([]);
    const [selectedCountry, setSelectedCountry] = useState(null)
    const [states, setStates] = useState([])

    useEffect(()=> {
        const fetchCountries = async () => {
            const countriesData = await actions.getCountries();
            setCountries(countriesData);
        };
    
        fetchCountries();
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

    

    return (
        <div>
            <h1 className="mb-5">Edit Profile</h1>
            <div style={{display: "flex"}}>
                <InputComponent label="Name" placeholder="Name"/> 
                <InputComponent label="Sirame" placeholder="Sirname"/> 
            </div>
            <div className="mx-3 mb-3" style={{display: 'flex'}}>
                <span className=" me-1 input-group-text" id="basic-addon1">Birth Date</span>
                <input type='date' id='dateInput'></input>
            </div>
            <div style={{display: "flex"}}>
                <InputComponent label="Phone Number" placeholder="Phone Number"/> 
                <InputComponent label="Nationality" placeholder="Nationality"/> 
            </div>
            <div style={{display: "flex"}}>
                <InputComponent label="Address" placeholder="Address"/> 
            </div>
            <div className="row">
                <div className="col-6 mb-3 mx-3" style={{display: "flex", height: '6vh'}}>
                    <span className="input-group-text" id="basic-addon1">Country</span>
                        <select 
                            className="form-select form-select-lg mb-3" 
                            aria-label="Large select example" 
                            style={{height: '6vh', fontSize: '2vh'}}
                            value={selectedCountry}
                            onChange={handleCountryChange}
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
                    <select className="form-select form-select-lg mb-3" aria-label="Large select example" style={{height: '6vh', fontSize: '2vh'}}>
                            <option selected>Select a State</option>
                            {selectedCountry != null ? 
                            states.map((state, index)=> (
                                <option key={index} value={state.id}>{state.state}</option>
                            )) : <option>Select a country first</option>}
                    </select>
                </div>
            </div>
            <div style={{display: "flex"}}>
                 <InputComponent label="City" placeholder="city"/> 
            </div>
            <div className="my-5">
                <button onClick={()=> {
                    props.saveChangesFunction}} 
                    type="button" className="btn btn-warning">Save changes</button>
            </div>
        </div>
    );
};

export default EditProfile;
