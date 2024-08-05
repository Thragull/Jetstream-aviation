import React, { useState, useEffect, useContext } from "react";
import Select from 'react-select';
import { Context } from "../../store/appContext";
import './NationalitySelector.css';

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

const NationalitySelector = ({ onNationalityChange }) => {
    const { actions } = useContext(Context);
    const [nationalities, setNationalities] = useState([]);

    useEffect(() => {
        const fetchNationalities = async () => {
            const data = await actions.getNationalities();
            setNationalities(data);
        };

        fetchNationalities();
    }, [actions]);

    const formatOptionLabel = ({ flag, nationality }) => (
        <div className="nationality-option d-flex align-items-center">
            <img src={flag} alt={`Flag of ${nationality}`} className="nationality-flag me-2" />
            <span>{nationality}</span>
        </div>
    );

    const handleChange = selectedOption => {
        onNationalityChange(selectedOption);
    };

    return (
        <Select
            options={nationalities}
            getOptionLabel={option => option.nationality}
            getOptionValue={option => option.id}
            formatOptionLabel={formatOptionLabel}
            onChange={handleChange}
            placeholder="Select a nationality..."
            isSearchable
            styles={customStyles}
        />
    );
};

export default NationalitySelector;

