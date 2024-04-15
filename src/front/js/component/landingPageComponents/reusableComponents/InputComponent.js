import { Context } from "../../../store/appContext";
import React, { useContext, useState, useEffect } from "react";


export const InputComponent = (props) => {
	const { store, actions } = useContext(Context);

	return (
     <div className="input-group mb-3 mx-3">
        <span className="input-group-text" id="basic-addon1">{props.label}</span>
        <input type="text" className="form-control" placeholder={props.placeholder} aria-label="Username" aria-describedby="basic-addon1"></input>
     </div>
	);
};

export default InputComponent; 

