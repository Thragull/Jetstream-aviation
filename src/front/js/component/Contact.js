import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import Navbar from "./Navbar";
import "../../styles/Contact.css"
import { Modal } from "react-bootstrap";
import { Footer } from "./footer";

const Contact = () => {

  const navigate = useNavigate();
  const { store, actions } = useContext(Context);
  const [model, setModel] = useState(0)
  const [selectedConfiguration, setSelectedConfiguration] = useState(0)
  const [name, setName] = useState("")
  const [surname, setSurname] = useState("")
  const [business, setBusiness] = useState("")
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState(0)
  const [startDate, setStartDate] = useState(new Date())
  const [endDate, setEndDate] = useState(new Date())
  const [planeNumber, setPlaneNumber] = useState(0)
  const [crew, setCrew] = useState()
  const [models, setModels] = useState([])
  const [configurations, setConfigurations] = useState([])
  const [unitaryPrice, setUnitaryPrice] = useState()

  const [showModal, setShowModal] = useState(false);

  const openModal = () => {
    setShowModal(true);
    console.log("debería abrir")
  };

  const closeModal = () => {
    setShowModal(false);
  };

  const calculateDaysDifference = () => {
    const oneDay = 24 * 60 * 60 * 1000; 
    const start = new Date(startDate);
    const end = new Date(endDate);
    const differenceInMilliseconds = Math.abs(end - start);
    return Math.round(differenceInMilliseconds / oneDay);
  };

  const handleCrewChange = (event) => {
    setCrew(event.target.checked);
  };

  const getPriceForSelection = () =>{
    let url = process.env.BACKEND_URL +'/api/prices?model_id='+model+'&configuration_id='+selectedConfiguration+'&crew='+crew;

    fetch(url)
    .then((response)=> response.json())
    .then((data) => {setUnitaryPrice(data[0].price)})
    .catch((err) => err)
  }

  const submitBudget = () => {
    getPriceForSelection();
  }

  const postBudget = (budget) => {
    let url = process.env.BACKEND_URL + '/api/budgets'
    fetch(url, {
      method: "POST",
      body: JSON.stringify(budget),
      headers: {
        "Content-Type" : "application/json"
      }
    }
    )
    .then((response)=> response.json())
    .then((data) => {console.log(data)})
    .catch((err) => err)
  }

  useEffect(() => {
    const fetchModels = async () => {
      const arrModels = await actions.getModels()
      setModels(arrModels)
    }
    
    if (model === 0) {
      fetchModels();
    } else {
      const fetchConfigurations = async () => {
        const arrConfigurations = await actions.getConfigurations(model);
        setConfigurations(arrConfigurations);
      };
      fetchConfigurations();
    }
    if (unitaryPrice){
      let totalPrice = unitaryPrice * planeNumber * calculateDaysDifference()

      let budget = {
        "client_name": name,
        "client_surname": surname,
        "client_business": business,
        "client_email": email,
        "client_phone": phone,
        "start_date": startDate,
        "end_date": endDate,
        "total_price": totalPrice
      }
      postBudget(budget)
      openModal()
    }
  }, [model, selectedConfiguration, crew, unitaryPrice])

  return (
    <div>
      <div>
        <Navbar />
      </div>
      <div id="budgetForm" className="container">
        <form>
          <div className="row">
              <div className="mb-3 col-6">
                  <label for="ClientName" className="form-label">Name</label>
                  <input required type="text" className="form-control" id="ClientName" value={name}
                  onChange={(element) => {setName(element.target.value)}}/>
              </div>
              <div className="mb-3 col-6">
                  <label for="ClientSurname" className="form-label">Surname</label>
                  <input required type="text" className="form-control" id="ClientSurname"  value={surname}
                  onChange={(element) => {setSurname(element.target.value)}}/>
              </div>
          </div>
          <div className="row">
              <div className="mb-3 col-4">
                  <label for="ClientBusiness" className="form-label">Business</label>
                  <input required type="text" className="form-control" id="ClientBusiness" value={business}
                  onChange={(element) => {setBusiness(element.target.value)}}/>
              </div>
              <div className="mb-3 col-4">
                  <label for="ClientEmail" className="form-label">Email</label>
                  <input required type="email" className="form-control" id="ClientEmail"  value={email}
                  onChange={(element) => {setEmail(element.target.value)}}/>
              </div>
              <div className="mb-3 col-4">
                  <label for="ClientPhone" className="form-label">Phone</label>
                  <input required type="number" className="form-control" id="ClientPhone"  value={phone}
                  onChange={(element) => {setPhone(element.target.value)}}/>
              </div>
          </div>
            <div className="row">
                <div className="mb-3 col-6">
                    <label for="StartDate" className="form-label">Start</label>
                    <input type="date" className="form-control" id="StartDate" value={startDate}
                    onChange={(element) => {setStartDate(element.target.value)}}/>
                </div>
                <div className="mb-3 col-6">
                    <label for="EndDate" className="form-label">End</label>
                    <input type="date" className="form-control" id="EndDate"  value={endDate}
                    onChange={(element) => {setEndDate(element.target.value)}}/>
                </div>
            </div> 
          <div className="row">
            <div className="mb-3 col-1">
              <label for="PlaneNumber" className="form-label">#</label>
              <input required type="number" className="form-control" id="PlaneNumber" min={0} value={planeNumber}
              onChange={(element) => {setPlaneNumber(element.target.value)}}/> 
            </div>
            <div className="mb-3 col-3">
            <label for="Model" className="form-label">Models</label>
              <select if="Model" className="form-select" aria-label="Model"
              onChange={(element) => {setModel(element.target.value)}}>
                <option selected>Select a model</option>
                {models.map((item) =>{ return(<option key={item.id} value={item.id}>{item.model}</option>)})}
              </select>
            </div>
            <div className="mb-3 col-4">
            <label for="Configurations" className="form-label">Configurations</label>
              <select id="Configurations" className="form-select" aria-label="Configurations"
                onChange={(element) => {setSelectedConfiguration(element.target.value)}}>
                <option selected>Select a Configuration</option>
                {configurations.map((item) =>{ return(<option key={item.id} value={item.id}>C: {item.business} Y:{item.economy}</option>)})}
              </select>
            </div>
            <div className="mb-3 col-4">
              <div id="Switch" className="form-check form-switch">
                <label className="form-check-label" for="flexSwitchCheckDefault">Do you want to hire crew?</label>
                <input className="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault"
                onChange={handleCrewChange}/>
                
              </div>
            </div>
          </div>
          <div className="row mt-2">
            <div className="col-12 d-flex justify-content-center">
                <button type="button" className="btn btn-secondary"
                onClick={submitBudget}>Submit</button>
            </div>
          </div>
        </form>
        <Modal show={showModal} onHide={() => setShowModal(false)}>
          <Modal.Header id="modalHeader" closeButton>
            <Modal.Title><img className="stop" src={stop}/>Budget Created<img className="stop" src={stop}/> </Modal.Title>
          </Modal.Header>
          <Modal.Body className="bg-light">
            <div>
              <p><strong>Name:</strong> {name}</p>
              <p><strong>Surname:</strong> {surname}</p>
              <p><strong>Business:</strong> {business}</p>
              <p><strong>Email:</strong> {email}</p>
              <p><strong>Phone:</strong> {phone}</p>
              <p><strong>Start Date:</strong> {startDate}</p>
              <p><strong>End Date:</strong> {endDate}</p>
              <p><strong>Plane Number:</strong> {planeNumber}</p>
              <p><strong>Total Price:</strong> {unitaryPrice ? unitaryPrice * planeNumber * calculateDaysDifference() : '-'}</p>
            </div>
          </Modal.Body>
          <Modal.Footer id="modalFooter">
            <button className="btn btn-secondary" onClick={() => setShowModal(false)}>OK</button>
          </Modal.Footer>
        </Modal>
      </div>
      <Footer />
    </div>
  );
};

export default Contact;
