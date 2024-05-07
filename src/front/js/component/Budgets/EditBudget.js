import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Context } from "../../store/appContext";
import "./budgets.css"


const EditBudget = (props) => {
    const navigate = useNavigate();
    const { store, actions } = useContext(Context);
    const [startDate, setStartDate] = useState(new Date(store.singleBudget.start_date).toISOString().split('T')[0]);
    const [endDate, setEndDate] = useState(new Date(store.singleBudget.end_date).toISOString().split('T')[0]);
    const [totalPrice, setTotalPrice] = useState(store.singleBudget.total_price)
    const [accepted, setAccepted] = useState(store.singleBudget.accepted)
  
    const putBudget = () =>{
        const authToken = localStorage.getItem("jwt-token");
        let url = process.env.BACKEND_URL + '/api/budgets?id='+ store.singleBudget.id;

        fetch(url, {
                method: "PUT",
                body: JSON.stringify(store.singleBudget),
                headers: {
                    Authorization: `Bearer ${authToken}`,
                    "Content-Type" : "application/json"
                }
        })
        .then((response)=> response.json())
        .then((data) => {props.onSaveChanges()})
        .catch((err) => {console.log(err)})
    }
    const changeDetails = () => {
        actions.setSingleBudget({...store.singleBudget, start_date: startDate, end_date: endDate, total_price: totalPrice,
                                accepted: accepted, pending: false})
                                putBudget()                        
    }
    
    return (
        <div className="container mt-5">
            <form>
                <div className="row">
                    <div className="mb-3 col-6">
                        <label for="ClientName" className="form-label">Name</label>
                        <input disabled type="text" className="form-control" id="ClientName" value={store.singleBudget.client_name}/>
                    </div>
                    <div className="mb-3 col-6">
                        <label for="ClientSurname" className="form-label">Surname</label>
                        <input disabled type="text" className="form-control" id="ClientSurname"  value={store.singleBudget.client_surname}/>
                    </div>
                </div>
                <div className="row">
                    <div className="mb-3 col-4">
                        <label for="ClientBusiness" className="form-label">Business</label>
                        <input disabled type="text" className="form-control" id="ClientBusiness" value={store.singleBudget.client_business}/>
                    </div>
                    <div className="mb-3 col-4">
                        <label for="ClientEmail" className="form-label">Email</label>
                        <input disabled type="email" className="form-control" id="ClientEmail"  value={store.singleBudget.client_email}/>
                    </div>
                    <div className="mb-3 col-4">
                        <label for="ClientPhone" className="form-label">Phone</label>
                        <input disabled type="number" className="form-control" id="ClientPhone"  value={store.singleBudget.client_phone}/>
                    </div>
                </div>
                <div className="row">
                    <div className="mb-3 col-4">
                        <label for="StartDate" className="form-label">Start</label>
                        <input type="date" className="form-control" id="StartDate" value={startDate}
                        onChange={(element) => {setStartDate(element.target.value)}}/>
                    </div>
                    <div className="mb-3 col-4">
                        <label for="EndDate" className="form-label">End</label>
                        <input type="date" className="form-control" id="EndDate"  value={endDate}
                        onChange={(element) => {setEndDate(element.target.value)}}/>
                    </div>
                    <div className="mb-3 col-4">
                        <label for="TotalAmount" className="form-label">Total</label>
                        <input type="number" className="form-control" id="TotalAmount" value={totalPrice}
                        onChange={(element) => {setTotalPrice(element.target.value)
                        }}/>
                    </div>
                </div>
                <div className="row">
                    <div className="col-12 d-flex justify-content-center">
                        <div className="form-check form-check-inline">
                            <input className="form-check-input" type="radio" name="budgetDecision" id="AcceptBudget" value={"true"} 
                            onChange={() => {setAccepted(true)}}/>
                            <label className="form-check-label" for="AcceptBudget" > 
                                Accept
                            </label>
                        </div>
                        <div className="form-check form-check-inline">
                            <input className="form-check-input" type="radio" name="budgetDecision" id="RejectBudget" value={"false"} 
                            onChange={() => {setAccepted(false)}}/>
                            <label className="form-check-label" for="RejectBudget" > 
                                Reject
                            </label>
                        </div>
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-12 d-flex justify-content-center">
                        <button type="button" className="btn btn-secondary"
                        onClick={changeDetails}>Submit</button>
                    </div>
                </div>
            </form>

        </div>
    )
}

export default EditBudget