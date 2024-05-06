import React, { useContext } from "react";
import { Context } from "../../../store/appContext";


export const InfoComponent = (props) => {
	const { store, actions } = useContext(Context);


	return (
        <div className=" mx-2 p-2" style={{borderRadius: "20px", backgroundColor: 'rgba(255,255,255,0.0', display: 'inline-block', fontSize: '1.5vw'}}>
            <p>{props.label}: {props.name}</p>
        </div>
	);
};

export default InfoComponent; 