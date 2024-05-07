import { Context } from "../../../store/appContext";
import React, { useContext, useState, useEffect } from "react";


export const SelectComponent = (props) => {
	const { store, actions } = useContext(Context);

	return (
     <div className=" mb-3" style={{display: "flex"}}>
        <span className="input-group-text" id="basic-addon1" style={{ height: '6vh', fontSize: '2vh'}}>{props.label}</span>
        <select 
                            className="form-select form-select-lg mb-3" 
                            aria-label="Large select example" 
                            style={{height: '6vh', fontSize: '2vh'}}
                            value={props.selectValue}
                            name = {props.name}
                            onChange={props.onChange}
                            >
                            <option selected>{props.selectLabel}</option>
                            {
                                props.map()
                            }
        </select>
     </div>
	);
};

export default SelectComponent; 