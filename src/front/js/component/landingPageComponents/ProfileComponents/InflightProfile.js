import { Context } from "../../../store/appContext";
import React, { useContext, useState, useEffect } from "react";
import InfoComponent from "../reusableComponents/InfoComponent";


export const InflightProfile = (props) => {
	const { store, actions } = useContext(Context);

	return (
        <div>
            <div style={{display: "flex"}}>
                <InfoComponent label="License"/>
                <InfoComponent label="Passport"/>
                <InfoComponent label="Pass exporation"/>
            </div>
            <div style={{display: "flex"}}>
                <InfoComponent label="Certificate"/>
                <InfoComponent label="Certificate expiration"/>
            </div>
            <div style={{display: "flex"}}>
                <InfoComponent label="Home Base"/>
            </div>
            <div style={{display: "flex"}}>
                <InfoComponent label="Roster Asigned"/>
            </div>
            <div style={{display: "flex"}}>
                <InfoComponent label="Monthly BH"/>
                <InfoComponent label="Yearly BH"/>
                <InfoComponent label="Total BH"/>
            </div>
            <div style={{display: "flex"}}>
                <InfoComponent label="Monthly DH"/>
                <InfoComponent label="Yearly DH"/>
            </div>

        </div>
        
	);
};

export default InflightProfile; 
