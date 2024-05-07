import React from "react";
import Navbar from "./Navbar";

const Contact = () => {
  return (
    <div>
      <div>
        <Navbar />
      </div>

      <div className="text-center mt-5 text-dark">
        <p className="contact-title">Contact</p>
      </div>

      <div classNameName="row">
        <div className="col-8 mb-3 ps-5">
          <label htmlFor="exampleFormControlInput1" className="form-label">
            <b>Name</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleFormControlInput1"
          />
        </div>

        <div className="col-8 mb-3 ps-5">
          <label for="exampleFormControlInput1" className="form-label">
            <b>Last Name</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleFormControlInput1"
          />
        </div>

        <div className="col-8 mb-3 ps-5">
          <label for="exampleFormControlInput1" className="form-label">
            <b>Business</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleFormControlInput1"
          />
        </div>

        <div className="InputEmail col-8 mb-3 ps-5">
          <label for="exampleFormControlInput1" className="form-label">
            <b>Email address </b>
          </label>
          <input
            type="email"
            className="form-control"
            id="exampleFormControlInput1"
          />
        </div>

        <div className="col-8 mb-3 ps-5">
          <label for="exampleFormControlInput1" className="form-label">
            <b>Phone Number</b>
          </label>
          <input
            type="number"
            className="form-control"
            id="exampleFormControlInput1"
          />
        </div>
      </div>

      <div className="row ms-1">
        <div className="col-4 mb-3 ps-5 pb-4">
          <label for="exampleFormControlInput1" className="form-label">
            <b>Start</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleFormControlInput1"
          />
        </div>

        <div className="col-4 mb-3 ps-5 pb-4">
          <label for="exampleFormControlInput1" className="form-label">
            <b>End</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleFormControlInput1"
          />
        </div>  
        </div>
      <div className="row ms-1">
        <div className="col-4 mb-3 ps-5 pb-4">
        <label htmlFor="exampleFormControlSelect1" className="form-label">
    <b>Choose a Model</b>
  </label>
  <select className="form-select" id="exampleFormControlSelect1">
  <option>Select a Model</option>
    <option>A320</option>
    <option>A321</option>
    <option>A330</option>
    <option>A350</option>
    <option>B737</option>
    <option>B777</option>
    <option>B787</option>
    
  </select>
        </div>  

        <div className="col-4 mb-3 ps-5 pb-4">
        <label htmlFor="exampleFormControlSelect1" className="form-label">
    <b>Choose a configuration</b>
  </label>
  <select className="form-select" id="exampleFormControlSelect1">
    <option>Select a Configuration</option>
    <option>Economy</option>
    <option>Buisiness</option>
   
  </select>
        </div>  

      </div>
      

      <div classNameName="row">

      <div className="col-4 mb-3 ps-5 pb-4">
          <label for="exampleFormControlInput1" className="form-label">
            <b>Quantity</b>
          </label>
          <input
            type="number"
            className="form-control"
            id="exampleFormControlInput1"
          />
        </div>  
        <div className="col-8 mb-3 ps-5 pb-4">          
            <label className="form-check-label" for="defaultCheck1">
              <b>Would you like to add a Cabin Crew service?</b>
            </label>
            <input
              className="form-check-input ms-5"
              type="checkbox"
              value=""
              id="defaultCheck1"
            />
            </div>
        
      </div>

      <div className="col-8 mb-3 ps-5 pb-4 d-flex flex-row">
          <button type="button" className="btn btn-primary">
            Send
          </button>
        </div>
    </div>
  );
};

export default Contact;
