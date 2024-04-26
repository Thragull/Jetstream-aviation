import React from "react";
import LogoJetstream from "../../img/LogoJetstream.png";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="NavbarHome navbar navbar-expand-lg text-white">
      <div className="container-fluid text-white fs-5 mt-5">
        <Link to='/'>
          <a className="navbar-brand" href="https://special-space-couscous-q77qrp54p9vwf4g77-3000.app.github.dev/">
            <h1 className="text-white fs-1 mb-4">JetStream</h1>
          </a>
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNavDropdown">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link to="/AboutUs">
                <a className="nav-link text-white" href="#">
                  <p>
                    <b>About Us</b>
                  </p>
                </a>
              </Link>
            </li>

            <li className="nav-item text-white">
            <Link to="/Fleet">
              <a className="nav-link text-white" href="#">
                <p>
                  <b>Fleet</b>
                </p>
              </a>
            </Link>
            </li>
            <li className="nav-item text-white">
            <Link to="/Services">
              <a className="nav-link text-white" href="#">
                <p>
                  <b>Services</b>
                </p>
              </a>
            </Link>
            </li>
            
            <li className="nav-item">
              <Link to="/contact">
                <a className="nav-link text-white" href="#">
                  <p className="ContactButton">
                    <b>Contact</b>
                  </p>
                </a>
              </Link>
            </li>
          </ul>
        </div>
        <div className="logo mt-5 me-5">
          <img
            src={LogoJetstream}
            className="me-0"
            alt="logo"
            width="200"
            height="200"
          ></img>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
