import React from "react";
import LogoJetstream from "../../img/LogoJetstream.png";
import { Link } from "react-router-dom";


const Navbar = () => {
  return (
    <nav className="NavbarHome navbar navbar-expand-lg text-white">
    
      <div>
        
      </div>
    <div className="container-fluid text-white mt-5">
      <Link to='/' style={{ textDecoration: "none" }}>
        <a className="navbar-brand" href="https://special-space-couscous-q77qrp54p9vwf4g77-3000.app.github.dev/">
          <h1 id="Titulo" className="text-white ">JetStream</h1>
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
            <Link to="/Welcome" style={{ textDecoration: "none" }}> 
              <a className="NavBtn nav-link text-white" href="#" style={{ textDecoration: "none" }}>
                <p>
                  <b>Welcome</b>
                </p>
              </a>
            </Link>
          </li>
  
          <li className="nav-item">
            <Link to="/Fleet" style={{ textDecoration: "none" }}>
              <a className="NavBtn nav-link text-white" href="#" style={{ textDecoration: "none" }}>
                <p>
                  <b>Fleet</b>
                </p>
              </a>
            </Link>
          </li>
          <li className="nav-item text-white">
            <Link to="/Services" style={{ textDecoration: "none" }}>
              <a className="NavBtn nav-link text-white" href="#" style={{ textDecoration: "none" }}>
                <p>
                  <b>Services</b>
                </p>
              </a>
            </Link>
          </li>
  
          <li className="nav-item">
            <Link to="/contact" style={{ textDecoration: "none" }}>
              <a className="NavBtn nav-link text-white" href="#" style={{ textDecoration: "none" }}>
                <p className="ContactButton">
                  <b>Contact</b>
                </p>
              </a>
            </Link>
          </li>

          <li className="nav-item">
            <Link to="/AboutUs" style={{ textDecoration: "none" }}>
              <a className="NavBtn nav-link text-white text-center" href="#" style={{ textDecoration: "none" }}>
                <p>
                  <b>About Us</b>
                </p>
              </a>
            </Link>
          </li>
        </ul>
      </div>
      <div className="Logo mt-5">
        <img
          src={LogoJetstream}
          className="LogoNavbarCliente me-0"
          alt="logo"

          
        ></img>
      </div>
      
    </div>
  </nav>
  );
};

export default Navbar;
