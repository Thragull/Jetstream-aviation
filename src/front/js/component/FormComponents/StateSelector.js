import React, { useState, useEffect, useContext } from "react";
import Select from 'react-select';
import { Context } from "../../store/appContext";
import './StateSelector.css';

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

const StateSelector = ({ countryId, onStateChange }) => {
    const { actions } = useContext(Context);
    const [states, setStates] = useState([]);

    useEffect(() => {
        const fetchStates = async () => {
            if (countryId) {
                const data = await actions.getStates(countryId);
                setStates(data);
            }
        };

        fetchStates();
    }, [countryId, actions]);

    const handleChange = selectedOption => {
        onStateChange(selectedOption);
    };

    return (
        <Select
            options={states}
            getOptionLabel={option => option.state}
            getOptionValue={option => option.id}
            onChange={handleChange}
            placeholder="Select a state..."
            isSearchable
            styles={customStyles}
        />
    );
};

export default StateSelector;
