import React, { useContext } from "react";
import { Context } from "../../store/appContext";


export const MoodelsComponent = () => {
	const { store, actions } = useContext(Context);

	return (
        <div>
            <h1>Moodels</h1>
        </div>
	);
};

export default MoodelsComponent; 