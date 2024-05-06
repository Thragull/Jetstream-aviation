import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../../store/appContext";
import "./budgets.css"


const ShowBudgets = () => {
    const navigate = useNavigate();
    const { store, actions } = useContext(Context);

    useEffect(() => {
        let params = {}
        if (store.pendingBudgets){
            params = {pending: store.pendingBudgets}
        }
        else{
            params = {
                pending: false,
                accepted: store.acceptedBudgets
            }
        }
        actions.getBudgets(params);
    }, [store.pendingBudgets, store.acceptedBudgets])
  
    return (
        <div className="container mt-3">
            <ul className="list-group list-group-horizontal">
                <li className="list-group-item col-1 text-center header">Name</li>
                <li className="list-group-item col-1 text-center header">Surname</li>
                <li className="list-group-item col-1 text-center header">Business</li>
                <li className="list-group-item col-2 text-center header">Email</li>
                <li className="list-group-item col-1 text-center header">Phone #</li>
                <li className="list-group-item col-2 text-center header">Start</li>
                <li className="list-group-item col-2 text-center header">End</li>
                <li className="list-group-item col-2 text-center header">Total</li>
            </ul>
            {store.budgets.map((item) => {
                const startDate = item.start_date.split(' ')[0];
                const endDate = item.end_date.split(' ')[0];
                const bgClass = item.pending ? 'pending' : (item.accepted ? 'accepted' : 'rejected');
                return(
                    <ul key={item.id} className="list-group list-group-horizontal">
                        <li className={`list-group-item col-1 text-center ${bgClass}`}>{item.client_name}</li>
                        <li className={`list-group-item col-1 text-center ${bgClass}`}>{item.client_surname}</li>
                        <li className={`list-group-item col-1 text-center ${bgClass}`}>{item.client_business}</li>
                        <li className={`list-group-item col-2 text-center ${bgClass}`}>{item.client_email}</li>
                        <li className={`list-group-item col-1 text-center ${bgClass}`}>{item.client_phone}</li>
                        <li className={`list-group-item col-2 text-center ${bgClass}`}>{startDate}</li>
                        <li className={`list-group-item col-2 text-center ${bgClass}`}>{endDate}</li>
                        <li className={`list-group-item col-2 text-center ${bgClass}`}>{item.total_price+"€"}</li>
                    </ul>
                )
            })}
        </div>
    )
}

export default ShowBudgets
