import React, { useContext, useState } from "react";
import { Context } from "../../store/appContext";


export const CrewControllerComponent = () => {
	const { store, actions } = useContext(Context);

	return (
        <div>
            <h1>Crew Controller</h1>
        </div>
	);
};

export default CrewControllerComponent; 