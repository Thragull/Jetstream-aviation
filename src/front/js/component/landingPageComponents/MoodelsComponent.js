import React, { useContext } from "react";
import { Context } from "../../store/appContext";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFolder } from '@fortawesome/free-solid-svg-icons'
import Lottie from "react-lottie";
import animationData from "../../../img/moodel_animation.json";


export const MoodelsComponent = () => {
	const { store, actions } = useContext(Context);

    const defaultOptions = {
        loop: true,
        autoplay: true,
        animationData: animationData, 
        renderSettings: {
            preserveAspectRatio: "xMidYMid slice"}
    }

	return (
        <div>
            <h1>Moodels</h1>
            <div className="mx-2">
                <button type="button" className="btn" style={{background: 'transparent'}}>
                    <FontAwesomeIcon icon={faFolder} style={{height: '10vh', width: '10vh'}} onClick={()=> {}} />
                    <p>Certificates</p>
                </button>
            </div>
            <h4>Upcoming moodels:</h4>
            <Lottie
                    options={defaultOptions}
                    height={300}
                    width={300}
                />
        </div>
	);
};

export default MoodelsComponent; 