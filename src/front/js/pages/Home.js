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
            <div className="container">
              <div className="navbar-brand">
                <img
                  src={LogoJetstream}
                  className="LogoJetstream"
                  alt="LogoJetstream"
                  width="300"
                  height="300"
                />
                <div>
                  <h1 id="tittle">Jetstream</h1>
                </div>
              </div>
            </div>
          </nav>
        </div>

        <div className="row ps-5 ms-5">
          <div className="col-3 pt-5">
            <img
              src={Window1Img}
              alt="Window1Img"
              className="img1 img-fluid rounded-pill w-100 h-75"
            />
            <div className="d-grid mx-auto text-center">
              <Link to="/client"> 
                <button className="btn1 btn" type="button">
                  <i className="fa-solid fa-plane"></i>
                  <b> Customer</b>
                </button>
              </Link>
            </div>
          </div>

          <div className="col-3 pt-5">
            <img
              src={Window2Img}
              alt="Window2Img"
              className="img2 img-fluid rounded-pill w-100 h-75"
            />
            <div className="d-grid mx-auto">
              <Link to="/login">
                <button className="btn2 btn" type="button">
                  <i className="fa-regular fa-circle-user"></i>
                  <b> Employee</b>
                </button>
              </Link>
            </div>
          </div>

          <div className="col-3 pt-5">
            <img
              src={Window3Img}
              alt="Window3Img"
              className="img3 img-fluid rounded-pill w-100 h-75"
            />
            <div className="d-grid mx-auto">
              <button className="btn3 btn" type="button">
                <i className="fa-solid fa-earth-americas"></i>
                <b> Socials</b>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

  
  );
};

export default Home;
