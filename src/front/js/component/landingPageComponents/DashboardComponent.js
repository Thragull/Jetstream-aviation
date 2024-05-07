import React, { useContext } from "react";
import { Context } from "../../store/appContext";
import Lottie from "react-lottie";
import animationData from "../../../img/construction_animation.json";


export const DashboardComponent = () => {
	const { store, actions } = useContext(Context);

    const defaultOptions = {
        loop: true,
        autoplay: true,
        animationData: animationData, 
        renderSettings: {
            preserveAspectRatio: "xMidYMid slice"
    }
}

	return (
        <div>
            <h1>Dashboard</h1>
            <div className="mt-5">
                <Lottie
                    options={defaultOptions}
                    height={400}
                    width={400}
                />
            </div>
        </div>
	);
};

export default DashboardComponent; 