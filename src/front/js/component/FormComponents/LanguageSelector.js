import React, { useState, useEffect, useContext } from "react";
import Select from 'react-select';
import { Context } from "../../store/appContext";
import './LanguageSelector.css';

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

const LanguageSelector = ({ onLanguageChange }) => {
    const { actions } = useContext(Context);
    const [languages, setLanguages] = useState([]);

    useEffect(() => {
        const fetchLanguages = async () => {
            const data = await actions.getLanguages();
            setLanguages(data);
        };

        fetchLanguages();
    }, [actions]);

    const formatOptionLabel = ({ flag, language }) => (
        <div className="language-option d-flex align-items-center">
            <img src={flag} alt={`Flag of ${language}`} className="language-flag me-2" />
            <span>{language}</span>
        </div>
    );

    const handleChange = selectedOption => {
        onLanguageChange(selectedOption);
    };

    return (
        <Select
            options={languages}
            getOptionLabel={option => option.language}
            getOptionValue={option => option.id}
            formatOptionLabel={formatOptionLabel}
            onChange={handleChange}
            placeholder="Language"
            isSearchable
            styles={customStyles}
        />
    );
};

export default LanguageSelector;

