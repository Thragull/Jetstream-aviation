import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";


const Prueba = () => {
    const navigate = useNavigate();
    const { store, actions } = useContext(Context);

    useEffect(() => {
        actions.pruebaGetCountries()
    }, [])
  
    return (
        <div>
            <select class="form-select" aria-label="Default select example">
                <option defaultValue="0">Open this select menu</option>
                {store.countries.map((item, index) => {
                    return(
                        <option key={index} value={item.id}>{item.country}</option>
                    )
                })}
            </select>
        </div>
    )
}

export default Prueba
