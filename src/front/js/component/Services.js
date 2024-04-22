import React from "react";
import Navbar from "./Navbar";

const Services = () => {
  return (
    <div>
      <div>
        <Navbar />
      </div>
      <div className="row">
        <div className="col-4">
          <div className="card" style="width: 18rem;">
            <img src="..." className="card-img-top" alt="..." />
            <div className="card-body">
              <h5 className="card-title">Card title</h5>
              <p className="card-text">
                Some quick example text to build on the card title and make up
                the bulk of the card's content.
              </p>
              <a href="#" className="btn btn-primary">
                Contact Us
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Services;
