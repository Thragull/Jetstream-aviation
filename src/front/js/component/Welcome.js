import React from "react";
import Navbar from "./Navbar";
import Window2Img from "../../img/Window2Img.jpg";
import { Footer } from "./footer";

const LandingPageCliente = () => {
  return (
    
  <div>
    <div>
      <Navbar/>
    </div>  
    <div className="row">
      <div className="col-3">
      <img
          src={Window2Img}
          alt="WindowImg2"
          className="HalfWindowImage img-fluid pt-4"
          
        />
      </div>
      <div className="Welcome col-5">
      <p className="m-5 pt-5 text-center">"Welcome to <b>JetStream</b>, your gateway to bespoke air travel experiences. At JetStream, we pride ourselves on being more than just a charter airline – we're pioneers of personalized aviation. With a steadfast commitment to safety, reliability, and luxury, we redefine the art of flying, offering discerning travelers the freedom to soar to new heights in unparalleled comfort and style. "At JetStream, we embrace innovation and excellence at every turn. From our cutting-edge technology to our impeccable service standards, we continuously strive to set new benchmarks in the world of charter aviation. "





</p>
      </div>
    </div>
    <Footer />
  </div>  
  )
};

export default LandingPageCliente;
