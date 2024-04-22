import React, { useContext } from "react";
import { Context } from "../../store/appContext";


export const DashboardComponent = () => {
	const { store, actions } = useContext(Context);

	return (
        <div>
            <h1>Dashboard</h1>
        </div>
	);
};

export default DashboardComponent; 