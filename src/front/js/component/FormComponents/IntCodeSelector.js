import React, { useState, useEffect, useContext } from "react";
import Select from 'react-select';
import { Context } from "../../store/appContext";
import './IntCodeSelector.css';

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

const IntCodeSelector = ({ onIntCodeChange }) => {
    const { actions } = useContext(Context);
    const [intCodes, setIntCodes] = useState([]);

    useEffect(() => {
        const fetchIntCodes = async () => {
            const data = await actions.getIntCodes();
            setIntCodes(data);
        };

        fetchIntCodes();
    }, [actions]);

    const formatOptionLabel = ({ flag, intCode }) => (
        <div className="intCode-option d-flex align-items-center">
            <img src={flag} alt={`Flag of ${intCode}`} className="intCode-flag me-2" />
            <span>{intCode}</span>
        </div>
    );

    const handleChange = selectedOption => {
        onIntCodeChange(selectedOption);
    };

    return (
        <Select
            options={intCodes}
            getOptionLabel={option => option.intCode}
            getOptionValue={option => option.id}
            formatOptionLabel={formatOptionLabel}
            onChange={handleChange}
            placeholder="Select an international code..."
            isSearchable
            styles={customStyles}
        />
    );
};

export default IntCodeSelector;

