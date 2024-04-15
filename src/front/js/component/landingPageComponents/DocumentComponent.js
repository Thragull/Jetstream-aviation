import React, { useContext } from "react";
import { Context } from "../../store/appContext";


export const DocumentComponent = () => {
	const { store, actions } = useContext(Context);

	return (
        <div>
            <h1>Documents</h1>
        </div>
	);
};

export default DocumentComponent; 