import React, { useState, useContext } from "react";
import CountrySelector from "./CountrySelector";
import StateSelector from "./StateSelector";
import IntCodeSelector from "./IntCodeSelector";
import LanguageSelector from "./LanguageSelector";
import NationalitySelector from "./NationalitySelector";
import { Context } from "../../store/appContext";
import './Test.css';

const Test = () => {
    const { actions } = useContext(Context);
    const [selectedCountry, setSelectedCountry] = useState(null);
    const [selectedState, setSelectedState] = useState(null);
    const [selectedIntCode, setSelectedIntCode] = useState(null);
    const [selectedLanguage, setSelectedLanguage] = useState(null);
    const [selectedNationality, setSelectedNationality] = useState(null);

    const handleCountryChange = async (country) => {
        setSelectedCountry(country);
        setSelectedState(null); // Reset state selection when a new country is selected
    };

    const handleStateChange = (state) => {
        setSelectedState(state);
    };

    const handleIntCodeChange = async (intCode) => {
        setSelectedIntCode(intCode);
    };

    const handleLanguageChange = async (language) => {
        setSelectedLanguage(language);
    };

    const handleNationalityChange = async (nationality) => {
        setSelectedNationality(nationality);
    };

    return (
        <div className="test-component">
            <h2>Select Country and State</h2>
            <CountrySelector onCountryChange={handleCountryChange} />
            {selectedCountry && (
                <div>
                    <h3>Selected Country: {selectedCountry.country}</h3>
                    <StateSelector countryId={selectedCountry.id} onStateChange={handleStateChange} />
                </div>
            )}
            {selectedState && (
                <div>
                    <h3>Selected State: {selectedState.state}</h3>
                </div>
            )}
            <h2>Select International Phone Code</h2>
            <IntCodeSelector onIntCodeChange={handleIntCodeChange} />
            {selectedIntCode && (
                <div>
                    <h3>Selected International Phone Code: {selectedIntCode.intCode}</h3>
                </div>
            )}
            <h2>Select Language</h2>
            <LanguageSelector onLanguageChange={handleLanguageChange} />
            {selectedLanguage && (
                <div>
                    <h3>Selected Language: {selectedLanguage.language}</h3>
                </div>
            )}
            <h2>Select Nationality:</h2>
            <NationalitySelector onNationalityChange={handleNationalityChange} />
            {selectedNationality && (
                <div>
                    <h3>Selected Nationality: {selectedNationality.nationality}</h3>
                </div>
            )}
        </div>
    );
};

export default Test;
