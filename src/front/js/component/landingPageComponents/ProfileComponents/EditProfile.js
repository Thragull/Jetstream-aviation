import React, { useContext, useEffect, useRef } from "react";
import { Context } from "../../../store/appContext";
import InputComponent from "../reusableComponents/InputComponent";
<script src="https://cdnjs.cloudflare.com/ajax/libs/air-datepicker/2.2.3/js/i18n/datepicker.en.js"></script>



export const EditProfile = (props) => {
   
    const { store, actions } = useContext(Context);
    const datepickerRef = useRef(null);

    

    return (
        <div>
            <h1 className="mb-5">Edit Profile</h1>
            <div style={{display: "flex"}}>
                <InputComponent label="Name" placeholder="Name"/> 
                <InputComponent label="Sirame" placeholder="Sirname"/> 
            </div>
            <div className="mx-3 mb-3" style={{display: 'flex'}}>
                <span className=" me-1 input-group-text" id="basic-addon1">Birth Date</span>
                <input type='date' id='dateInput'></input>
            </div>
            <div style={{display: "flex"}}>
                <InputComponent label="Phone Number" placeholder="Phone Number"/> 
                <InputComponent label="Nationality" placeholder="Nationality"/> 
            </div>
            <div style={{display: "flex"}}>
                <InputComponent label="Address" placeholder="Address"/> 
            </div>
            <div style={{display: "flex"}}>
                <InputComponent label="Country" placeholder="country"/> 
                <InputComponent label="State" placeholder="state"/> 
                <InputComponent label="City" placeholder="city"/> 
            </div>
            <div className="my-5">
                <button onClick={props.saveChangesFunction} type="button" className="btn btn-warning">Save changes</button>
            </div>
        </div>
    );
};

export default EditProfile;
