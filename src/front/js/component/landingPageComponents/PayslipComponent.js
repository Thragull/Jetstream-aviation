import React, { useContext } from "react";
import { Context } from "../../store/appContext";


export const PayslipComponent = () => {
	const { store, actions } = useContext(Context);

	return (
        <div>
            <h1>Payslip</h1>
        </div>
	);
};

export default PayslipComponent;  
