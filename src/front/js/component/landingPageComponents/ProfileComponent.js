import React, { useContext, useState } from "react";
import { Context } from "../../store/appContext";
import InfoComponent from "./reusableComponents/InfoComponent";
import EditProfile from "./ProfileComponents/EditProfile";
import "./ProfileComponents/profile_component.css";
import InflightProfile from "./ProfileComponents/InflightProfile";


export const ProfileComponent = () => {
	const { store, actions } = useContext(Context);

    const [editProfile, setEditProfile] = useState(false)
    const [seeinflight, setSeeInflight] = useState(false)
    const activeTabColor = 'rgba(21, 39, 53,0.95)'
    const inactiveTabColor = 'rgba(255,255,255,0.5)'
    const activeProfileColor = seeinflight ? 'rgba(255,255,255,0.5)' : activeTabColor
    const activeInsightColor = seeinflight ? activeTabColor : inactiveTabColor
    const activeTabProfileTextColor = seeinflight ?  'rgba(21, 39, 53,0.95)' : 'white'
    const activeTabInsightTextColor = seeinflight ? 'white' : 'rgba(21, 39, 53,0.95)'
    




    const Divider = ({ width, height, color, margin }) => {
        const dividerStyle = {
          width:   "100%",
          height:  "2px",
          backgroundColor: "rgba(255,255,255,0.2)",
          margin: "0"
        };
      
        return <div style={dividerStyle}></div>;
      };

	return (
       editProfile ?   
            <EditProfile saveChangesFunction={()=> setEditProfile(false)}/>    
                 :  
        <div>
            <h1 className="mb-5">Profile</h1>
                <div className="row" style={{justifyContent: "space-between"}}>
                <div className="tab col-6" style={{background: `${activeProfileColor}`, color: `${activeTabProfileTextColor}`  }} onClick={()=> setSeeInflight(false)}>
                    Profile
                </div>
                <div onClick={()=> setSeeInflight(true)}  className="tab col-6" style={{background: `${activeInsightColor}`, color: `${activeTabInsightTextColor}`  }} >
                    Insight
                </div>
            </div>
            {seeinflight ? <InflightProfile/> : 
                <div>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Name" name={store.loggedInEmployee.name}/>
                        <InfoComponent label="Sirname" name={store.loggedInEmployee.surname}/>
                        <InfoComponent label="Birthday" name="13/06/1996"/>
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Email" name={store.loggedInEmployee.email}/>
                        <InfoComponent label="Phone Number" name="+34 678932436"/>
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Department" name="Cabin Crew"/>
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Nationality" name="Spanish"/>
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Adress" name="C/Finlandia 14, 14"/>
                        <InfoComponent label="ZipCode" name="46002"/>
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Country" name="Spain"/>
                        <InfoComponent label="State" name="C.Valencia"/>
                        <InfoComponent label="City" name="Valencia"/>
                    </div>
                    <Divider/> 
                    <div className="my-5">
                        <button onClick={()=> setEditProfile(true)} type="button" className="btn btn-info">Edit Profile</button>
                    </div> 
                </div> 
}
        </div>
	);
};

export default ProfileComponent; 