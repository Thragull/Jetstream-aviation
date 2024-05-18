import React from 'react';
import '../../styles/Fleet.css';

const Plane = (props) => {
  return (
    <div className="plane-card justify-content-center mb-5">
      <div className="card">
        <img src={props.imgSrc} className="card-img-top text-center" />
        <div className="card-body">
          <h5 className="card-title text-center">{props.title}</h5>
          <p className="card-text text-center">{props.text}</p>
        </div>
      </div>
    </div>
  );
};

export default Plane;
