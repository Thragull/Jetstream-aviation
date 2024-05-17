import React, { useState } from "react";
import LogoJetstream from "../../img/LogoJetstream.png";
import { Link } from "react-router-dom";
import "../../styles/navbar.css";

const Navbar = () => {
  
  return (
    <nav className="NavbarHome">
      <Link to="/" className="nav-link">
        <h1 className="title-nav-home">JetStream</h1>
      </Link>
      <div className="navbar-collapse" id="btnbarNavDropdown">
        <div className="nav-links">
          <Link to="/Welcome" className="NavBtn nav-link">
            <p className="link-nav">Welcome</p>
          </Link>
          <Link to="/Fleet" className="NavBtn nav-link">
            <p className="link-nav">Fleet</p>
          </Link>
          <Link to="/Services" className="NavBtn nav-link">
            <p className="link-nav">Services</p>
          </Link>
          <Link to="/contact" className="NavBtn nav-link">
            <p className="link-nav">Contact</p>
          </Link>
          <Link to="/AboutUs" className="NavBtn nav-link">
            <p className="link-nav">About Us</p>
          </Link>
        </div>
      </div>
      <img src={LogoJetstream} className="LogoJetstream" alt="LogoJetstream" />
    </nav>
  );
};

export default Navbar;
