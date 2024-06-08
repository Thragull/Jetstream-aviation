/*import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../../store/appContext";
import './Test.css'

const Test = () => {
    const navigate = useNavigate();
    const { store, actions } = useContext(Context);
    const [ countries, setCountries ] = useState(null)
    const [ loaded, setLoaded ] = useState(false)

    const fetchCountries = async () => {
        const data = await actions.getCountries()
        setCountries(data)
        console.log(data)
        setLoaded(true)
    }

    useEffect(() => {
        if (!loaded){
            fetchCountries()
        }
    }, [loaded])
  
    return (
        <div>
            <div className="container row">
                <div className="col-3">
                    <select className="form-select " aria-label="Select Country">
                        <option selected>Select Country</option>
                        {loaded ? countries.map((country)=>{return <option key={country.id} value={country.id}>
                            {()=>{return <img key={country.id} className="flag" src={country.flag} />}}
                            {country.country}
                        </option>}) : null}
                    </select>
                </div>
                <div className="col-3">
                    <select className="form-select col-3" aria-label="Select State">
                        <option selected>Select State</option>
                    </select>
                </div>
            </div>
        </div>
    )
}

export default Test
*/
/*import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../../store/appContext";
import './Test.css';

const Test = () => {
    const navigate = useNavigate();
    const { store, actions } = useContext(Context);
    const [countries, setCountries] = useState(null);
    const [loaded, setLoaded] = useState(false);
    const [selectedCountry, setSelectedCountry] = useState(null);

    const fetchCountries = async () => {
        const data = await actions.getCountries();
        setCountries(data);
        console.log(data);
        setLoaded(true);
    };

    useEffect(() => {
        if (!loaded) {
            fetchCountries();
        }
    }, [loaded]);

    const handleCountrySelect = (country) => {
        setSelectedCountry(country);
    };

    return (
        <div>
            <div className="container row">
                <div className="col-3">
                    <div className="dropdown">
                        <button
                            className="btn dropdown-toggle"
                            type="button"
                            id="dropdownMenuButton"
                            data-bs-toggle="dropdown"
                            aria-expanded="false"
                        >
                            {selectedCountry ? selectedCountry.country : 'Select Country'}
                        </button>
                        <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            {loaded && countries.map((country) => (
                                <li key={country.id} onClick={() => handleCountrySelect(country)}>
                                    <a className="dropdown-item" href="#">
                                        <img className="flag" src={country.flag} alt="flag" /> {country.country}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className="col-3">
                    <select className="form-select col-3" aria-label="Select State">
                        <option selected><img className="flag" src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Flag_of_Spain.svg" alt="flag" />Select State</option>
                    </select>
                </div>
            </div>
        </div>
    );
};

export default Test;
*/

import React, { useState, useEffect, useContext } from "react";
import Select from 'react-select';
import { Context } from "../../store/appContext";
import './Test.css';

const Test = () => {
    const { store, actions } = useContext(Context);
    const [countries, setCountries] = useState([]);
    const [loaded, setLoaded] = useState(false);

    const fetchCountries = async () => {
        const data = await actions.getCountries();
        setCountries(data.map(country => ({
            value: country.id,
            label: (
                <div className="country-option">
                    <img src={country.flag} alt={`Flag of ${country.country}`} className="flag" />
                    {country.country}
                </div>
            ),
            country: country.country
        })));
        setLoaded(true);
    };

    useEffect(() => {
        if (!loaded) {
            fetchCountries();
        }
    }, [loaded]);

    // Custom filter function to enable key navigation based on first letter
    const customFilterOption = (option, inputValue) => {
        return option.data.country.toLowerCase().startsWith(inputValue.toLowerCase());
    };

    return (
        <div className="container row">
            <div className="col-3">
                <Select
                    options={countries}
                    classNamePrefix="select"
                    placeholder="Select Country"
                    isSearchable={false}
                    filterOption={customFilterOption}
                />
            </div>
            <div className="col-3">
                <select className="form-select col-3" aria-label="Select State">
                    <option selected>Select State</option>
                </select>
            </div>
        </div>
    );
};

export default Test;
