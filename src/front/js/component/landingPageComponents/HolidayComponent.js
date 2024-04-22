import React, { useContext } from "react";
import { Context } from "../../store/appContext";


export const HolidayComponent = () => {
	const { store, actions } = useContext(Context);

	return (
        <div>
            <h1>Holidays</h1>
        </div>
	);
};

export default HolidayComponent; 