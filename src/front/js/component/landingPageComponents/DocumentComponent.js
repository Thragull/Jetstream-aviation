import React, { useContext } from "react";
import { Context } from "../../store/appContext";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFolder } from '@fortawesome/free-solid-svg-icons'



export const DocumentComponent = () => {
	const { store, actions } = useContext(Context);

	return (
        <div>
            <h1>Documents</h1>
            <div style={{display: 'flex'}}>
                <div style={{width: '12vw'}} className="mx-4">
                    <button type="button" className="btn" style={{background: 'transparent'}}>
                        <FontAwesomeIcon icon={faFolder} style={{height: '10vh', width: '10vh'}} onClick={()=> {}} />
                        <p>Official Documentation</p>
                    </button>
                </div>
                <div style={{width: '12vw'}} className="mx-4">
                    <button type="button" className="btn" style={{background: 'transparent'}}>
                        <FontAwesomeIcon icon={faFolder} style={{height: '10vh', width: '10vh'}} onClick={()=> {}} />
                        <p>Certificates</p>
                    </button>
                </div>
                <div style={{width: '12vw'}} className="mx-4">
                    <button type="button" className="btn" style={{background: 'transparent'}}>
                        <FontAwesomeIcon icon={faFolder} style={{height: '10vh', width: '10vh'}} onClick={()=> {}} />
                        <p>Other</p>
                    </button>
                </div>
            </div>
        </div>
	);
};

export default DocumentComponent; 