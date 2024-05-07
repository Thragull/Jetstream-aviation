//import react into the bundle
import React from "react";
import ReactDOM from "react-dom";
// import Home from "./pages/Home";
import "../styles/index.css";
import "../styles/home.css";
import "../styles/Welcome.css";
import "../styles/Services.css";
import "../styles/Contact.css";
import "../styles/Fleet.css";
import "../styles/Footer.css";
import "../styles/AboutUs.css";
import "../styles/NavbarCliente.css";
import Layout from "./layout";

//include your index.scss file into the bundle
//import your own components

//render your react application

// root.render (<layout/>)
ReactDOM.render(<Layout/>, document.querySelector("#app"));
