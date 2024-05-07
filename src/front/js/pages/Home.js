import React from "react";
import "../../styles/home.css";
import Window1Img from "../../img/Window1Img.jpg";
import Window2Img from "../../img/Window2Img.jpg";
import Window3Img from "../../img/Window3Img.jpg";
import LogoJetstream from "../../img/LogoJetstream.png";
import { Link } from "react-router-dom";
// import Contact from "../component/Contact";
// import Navbar from "../component/Navbar";

export const Home = () => {
  return (
    // <div>
    //   <Contact/>
    //   <Navbar/>
    // </div>
    <div>
      <div>
        <div>
          <nav className="NavbarHome ">
            <div>
              <div className="row navbar-brand d-flex ">
                <div className="col-4">
                  <p id="Title1">JetStream</p>
                </div>
                <div className="col-4"></div>
                <div className= "col-4">
                  <img
                    src={LogoJetstream}
                    className="LogoJetstream"
                    alt="LogoJetstream"
                  />
                </div>
              </div>
            </div>
          </nav>
        </div>

        <div className="RowWindows row ms-3">
          <div className="col-3 text-center">
            
            <img
              src={Window1Img}
              alt="Window1Img"
              className="img img-fluid rounded-pill"
            />
            <div className="d-grid mx-auto text-center">

              <Link to="/client">
                <button className="btn" type="button">
                  <i className="fa-solid fa-plane"></i>
                  <b> Customer</b>
                </button>
              </Link>
            </div>
          </div>

          <div className="col-3 text-center">
            <img
              src={Window2Img}
              alt="Window2Img"
              className="img img-fluid rounded-pill"
            />
            <div className="d-grid mx-auto text-center">
              <Link to="/login">

                <button className="btn" type="button">
                  <i className="fa-regular fa-circle-user"></i>
                  <b> Employee</b>
                </button>
              </Link>
            </div>
          </div>

          <div className="col-3 text-center">
            
            <img
              src={Window3Img}
              alt="Window3Img"
              className="img img-fluid rounded-pill"
            />
           
            
            <div className="d-grid mx-auto">

              <button className="btn" type="button">
              <i className="fa-solid fa-earth-americas"></i>
                <b> Promotions</b>
              </button>
            </div>
          </div>
          <div className="col-3 bg-white opacity-0"></div>
        </div>
      </div>
    </div>
  );
};

export default Home;
