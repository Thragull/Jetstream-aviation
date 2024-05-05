import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../../store/appContext";
import ShowBudgets from "./ShowBudgets";
import "./budgets.css"


const Budgets = () => {
    const { store, actions } = useContext(Context);

    const handleTabClick = (tab) => {
        if (tab === "pending") {
            actions.setPendingBudgets(true);
            actions.setAcceptedBudgets(false);
        } else if (tab === "accepted") {
            actions.setPendingBudgets(false);
            actions.setAcceptedBudgets(true);
        } else {
            actions.setPendingBudgets(false);
            actions.setAcceptedBudgets(false);
        }
    };
    
    return (
        <div className="container mt-3">
            <ul className="nav nav-tabs justify-content-center" role="tablist">
                <li className="nav-item" role="presentation">
                    <a className="nav-link active" id="pending-link" data-bs-toggle="tab" data-bs-target="#pending" role="tab" aria-controls="home-tab-pane" aria-selected="true" onClick={() => handleTabClick("pending")}>Pending</a>
                </li>
                <li className="nav-item" role="presentation">
                    <a className="nav-link" id="accepted-link" data-bs-toggle="tab" data-bs-target="#accepted" role="tab" aria-controls="home-tab-pane" aria-selected="false" onClick={() => handleTabClick("accepted")}>Accepted</a>
                </li>
                <li className="nav-item" role="presentation">
                    <a className="nav-link" id="rejected-link" data-bs-toggle="tab" data-bs-target="#rejected" role="tab" aria-controls="home-tab-pane" aria-selected="false" onClick={() => handleTabClick("rejected")}>Rejected</a>
                </li>
            </ul>
            <div className="tab-content" id="myTabContent">
                <div className="tab-pane fade show active" id="pending" role="tabpanel" aria-labelledby="home-tab" tabindex="0"><ShowBudgets /></div>
                <div className="tab-pane fade" id="accepted" role="tabpanel" aria-labelledby="profile-tab" tabindex="0"><ShowBudgets /></div>
                <div className="tab-pane fade" id="rejected" role="tabpanel" aria-labelledby="contact-tab" tabindex="0"><ShowBudgets /></div>
            </div>
        </div>
    )
}

export default Budgets