import React, { useContext, useEffect, useState } from "react";
import { Context } from "../../store/appContext";
import InfoComponent from "./reusableComponents/InfoComponent";
import EditProfile from "./ProfileComponents/EditProfile";
import InflightProfile from "./ProfileComponents/InflightProfile";
import "./ProfileComponents/profile_component.css";

const ProfileComponent = () => {
    const { store, actions } = useContext(Context);
    const [editProfile, setEditProfile] = useState(false);
    const [seeInflight, setSeeInflight] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                await actions.getInflight(store.loggedInEmployee.id);
            } catch (error) {
                console.error('Error fetching inflight data:', error);
            }
        };

        if (store.loggedInEmployee.department_id === 3) {
            fetchData();
        }
    }, [store.loggedInEmployee.id, store.loggedInEmployee.department_id, actions]);

    const handleTabClick = (inflight) => {
        setSeeInflight(inflight);
    };

    return (
        <div className="profile-container">
            {editProfile ? (
                <EditProfile saveChangesFunction={() => setEditProfile(false)} />
            ) : (
                <div>
                    {store.loggedInEmployee.department_id === 3 && (
                        <div className="tab-container">
                            <div
                                className={`tab ${seeInflight ? "" : "active"}`}
                                onClick={() => handleTabClick(false)}
                            >
                                Personal Info
                            </div>
                            <div
                                className={`tab ${seeInflight ? "active" : ""}`}
                                onClick={() => handleTabClick(true)}
                            >
                                Flight Details
                            </div>
                        </div>
                    )}
                    {seeInflight ? (
                        <InflightProfile />
                    ) : (
                        <div className="profile-info">
                            <div className="info-row">
                                <InfoComponent label={<b>First Name</b>} name={store.loggedInEmployee.name} />
                                <InfoComponent label={<b>Last Name</b>} name={store.loggedInEmployee.surname} />
                                {store.loggedInEmployee.birthday && (
                                    <InfoComponent label={<b>Date of Birth</b>} name={store.loggedInEmployee.birthday} />
                                )}
                            </div>
                            <div className="info-row">
                                <InfoComponent label={<b>Email</b>} name={store.loggedInEmployee.email} />
                            </div>
                            <div className="info-row">
                                <InfoComponent label={<b>Department</b>} name={store.loggedInEmployee.department_id} />
                                <InfoComponent label={<b>Role</b>} name={store.loggedInEmployee.role_id} />
                            </div>
                            <div className="info-row">
                                <InfoComponent label={<b>Nationality</b>} name={store.loggedInEmployee.nationality_id} />
                            </div>
                            <div className="info-row">
                                <InfoComponent label={<b>Address</b>} name={store.loggedInEmployee.address} />
                                <InfoComponent label={<b>Zip Code</b>} name={store.loggedInEmployee.zipcode} />
                            </div>
                            <div className="info-row">
                                <InfoComponent label={<b>Country</b>} name={store.loggedInEmployee.country_id} />
                                <InfoComponent label={<b>State</b>} name={store.loggedInEmployee.state_id} />
                                <InfoComponent label={<b>City</b>} name={store.loggedInEmployee.city} />
                            </div>
                            <div className="edit-button-container">
                                <button onClick={() => setEditProfile(true)} className="edit-button">
                                    Edit Profile
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ProfileComponent;
