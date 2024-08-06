import React from "react";
import Navbar from "./Navbar";
import Window1Img from "../../img/Window1Img.jpg";
import { Footer } from "./footer";
import "../../styles/Welcome.css";

const LandingPageCliente = () => {
  return (
    <div className="page-clients">
      <Navbar />
      <div className="flex-container">
        <div className="div-image">
          <img
            src={Window1Img}
            alt="Window2Img"
            className="img img-fluid rounded-pill"
          />
        </div>
        <div className="div-text">
          <p className="p1-welcome">
            Welcome to <b>JetStream</b>, your gateway to bespoke air travel experiences. At JetStream, we pride ourselves on being more than just a charter airline.
          </p>
          <p className="p2-welcome pt-5">
            We're pioneers of personalized aviation. With a steadfast commitment to safety, reliability, and luxury, we redefine the art of flying, offering discerning travelers the freedom to soar to new heights in unparalleled comfort and style.
          </p>
          <p className="p3-welcome pt-5">
            At JetStream, we embrace innovation and excellence at every turn. From our cutting-edge technology to our impeccable service standards, we continuously strive to set new benchmarks in the world of charter aviation.
          </p>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default LandingPageCliente;
