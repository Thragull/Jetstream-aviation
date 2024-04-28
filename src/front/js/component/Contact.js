import React from "react";
import Navbar from "./Navbar";

const Contact = () => {
  return (
    <div>
      <div>
        <Navbar />
      </div>
      <div className="text-center mt-5 text-dark">
        <h1>Contact</h1>
      </div>

      <div className="row">
        <div className="col-9 mb-3 ps-5">
          <label for="exampleFormControlInput1" className="form-label">
            <b>Name</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleFormControlInput1"
            placeholder="Name "
          />
        </div>

        <div className="col-9 mb-3 ps-5">
          <label for="exampleFormControlInput1" className="form-label">
            <b>Last Name</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleFormControlInput1"
            placeholder="Last Name"
          />
        </div>
      </div>

      <div className="row">
        <div className="InputEmail col-9 mb-3 ps-5">
          <label for="exampleFormControlInput1" className="form-label">
            <b>Email address </b>
          </label>
          <input
            type="email"
            className="form-control"
            id="exampleFormControlInput1"
            placeholder="name@example.com"
          />
        </div>
        
        <div className="col-9 mb-3 ps-5">
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

      <div className="row">
        <div className="col-9 mb-3 ps-5 pb-4">
          <label for="exampleFormControlTextarea1" className="form-label">
            <b>Comments</b>
          </label>
          <textarea
            className="form-control"
            id="exampleFormControlTextarea1"
            rows="6"
          ></textarea>
        </div>
        <div className="col-9 mb-3 ps-5 pb-4 d-flex flex-row-reverse">
           <button type="button" className="btn btn-primary">Send</button>
        </div>    
      </div>
    </div>
  );
};

export default Contact;
