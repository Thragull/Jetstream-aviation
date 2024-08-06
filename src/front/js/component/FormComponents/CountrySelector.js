import React, { useState, useEffect, useContext } from "react";
import Select from 'react-select';
import { Context } from "../../store/appContext";
import './CountrySelector.css';

const customStyles = {
    control: (provided, state) => ({
        ...provided,
        borderColor: state.isFocused ? '#80bdff' : '#ced4da',
        boxShadow: state.isFocused ? '0 0 0 0.2rem rgba(0,123,255,.25)' : provided.boxShadow,
        '&:hover': {
            borderColor: state.isFocused ? '#80bdff' : '#ced4da',
        },
    }),
    option: (provided, state) => ({
        ...provided,
        backgroundColor: state.isSelected
            ? '#007bff'
            : state.isFocused
            ? '#e9ecef'
            : null,
        color: state.isSelected ? 'white' : '#495057',
        '&:hover': {
            backgroundColor: state.isSelected ? '#0056b3' : '#e9ecef',
            color: state.isSelected ? 'white' : '#495057',
        },
    }),
    singleValue: (provided, state) => ({
        ...provided,
        color: '#495057',
    }),
};

const CountrySelector = ({ onCountryChange }) => {
    const { actions } = useContext(Context);
    const [countries, setCountries] = useState([]);

    useEffect(() => {
        const fetchCountries = async () => {
            const data = await actions.getCountries();
            setCountries(data);
        };

        fetchCountries();
    }, [actions]);

    const formatOptionLabel = ({ flag, country }) => (
        <div className="country-option d-flex align-items-center">
            <img src={flag} alt={country} className="country-flag me-2" />
            <span>{country}</span>
        </div>
    );

    const handleChange = selectedOption => {
        onCountryChange(selectedOption);
    };

    return (
        <Select
            options={countries}
            getOptionLabel={option => option.country}
            getOptionValue={option => option.id}
            formatOptionLabel={formatOptionLabel}
            onChange={handleChange}
            placeholder="Country"
            isSearchable
            styles={customStyles}
        />
    );
};

export default CountrySelector;
