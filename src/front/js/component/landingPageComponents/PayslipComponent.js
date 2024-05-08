import React, { useContext } from "react";
import { Context } from "../../store/appContext";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFile } from '@fortawesome/free-solid-svg-icons'


export const PayslipComponent = () => {
	const { store, actions } = useContext(Context);

	return (
        <div>
            <h1 className="mb-5">Payslips</h1>
            <div style={{display: 'flex'}}>
                <div className="mx-2">
                    <FontAwesomeIcon icon={faFile} style={{height: '10vh', width: '10vh'}} />
                    <p>Payslip January 2024</p>
                </div>
                <div className="mx-2">
                    <FontAwesomeIcon icon={faFile} style={{height: '10vh', width: '10vh'}} />
                    <p>Payslip February 2024</p>
                </div>
                <div className="mx-2">
                    <FontAwesomeIcon icon={faFile} style={{height: '10vh', width: '10vh'}} />
                    <p>Payslip March 2024</p>
                </div>
                <div className="mx-2">
                    <FontAwesomeIcon icon={faFile} style={{height: '10vh', width: '10vh'}} />
                    <p>Payslip April 2024</p>
                </div>
            </div>
        </div>
	);
};

export default PayslipComponent;  
