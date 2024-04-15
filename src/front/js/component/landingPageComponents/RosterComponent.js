import React, { useContext } from "react";
import { Context } from "../../store/appContext";
import CalendarComponent from "./RosterComponents/CalendarComponent";
import InfoComponent from "./reusableComponents/InfoComponent";





export const RosterComponent = () => {
	const { store, actions } = useContext(Context);

    const todayDate = new Date(); 

	return (
        <div>
            <h1>Roster</h1>
            <InfoComponent label="BH"/>
            <div>
                <CalendarComponent/>
            </div>
        </div>
	);
};

export default RosterComponent; 