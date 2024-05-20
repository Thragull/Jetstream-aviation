import React from "react";
import "../../styles/home.css";
import Window1Img from "../../img/Window1Img.jpg";
import Window2Img from "../../img/Window2Img.jpg";
import Window3Img from "../../img/Window3Img.jpg";
import LogoJetstream from "../../img/LogoJetstream.png";
import { Link } from "react-router-dom";
import { Footer } from "../component/footer";

export const Home = () => {
  return (
    <div className="nav-component">
      <div className="nav-lessfot">
        <nav className="NavbarHome">
          <h1 className="title-nav-home">JetStream</h1>
          <img
            src={LogoJetstream}
            className="LogoJetstream"
            alt="LogoJetstream"
          />
        </nav>
        <div className="RowWindows row">
          <div className="col-3 text-center">
            <img
              src={Window1Img}
              alt="Window1Img"
              className="img img-fluid rounded-pill"
            />
            <div className="d-grid mx-auto text-center">
              <Link to="/client">
                <button className="btn-home" type="button">
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
                <button className="btn-home" type="button">
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
              <button className="btn-home" type="button">
                <i className="fa-solid fa-earth-americas"></i>
                <b> Promotions</b>
              </button>
            </div>
          </div>
          <div className="col-3 bg-white opacity-0"></div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Home;
