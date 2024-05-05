import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";

import { Home } from "./pages/Home";
import { Demo } from "./pages/demo";
import { Single } from "./pages/single";
import {LandingPageWorker} from "./pages/LandingPageWorker"
import injectContext from "./store/appContext";

import Contact from "./component/Contact";
import { Footer } from "./component/footer";
import LandingPageCliente from "./component/LandingPageCliente";
import AboutUs from "./component/AboutUs";
import Fleet from "./component/Fleet";
import Services from "./component/Services";
import LoginPage from "./pages/LoginPage";
import Prueba from "./component/Prueba";



//create your first component
const Layout = () => {
  //the basename is used when your project is published in a subdirectory and not in the root of the domain
  // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
  const basename = process.env.BASENAME || "";

  if (!process.env.BACKEND_URL || process.env.BACKEND_URL == "")
    return <BackendURL />;

  return (
    <div>
      <BrowserRouter basename={basename}>
        <ScrollToTop>
          {/* <Navbar /> */}
          <Routes>
            <Route element={<Home />} path="/" />
            <Route element={<Demo />} path="/demo" />
            <Route element={<Single />} path="/single/:theid" />
            <Route element={<h1>Not found!</h1>} />
            <Route element={<LandingPageCliente />} path="/client" />
            <Route element={<LandingPageWorker/>} path="/worker"/>
            <Route element={<Contact />} path="/contact" />
            <Route element={<AboutUs />} path="/aboutUs" />
            <Route element={<Fleet />} path="/fleet" />
            <Route element={<Services />} path="/services" />
            <Route element={<LoginPage/>} path="/login" />
            <Route element={<Prueba/>} path="/prueba"/>
          </Routes>
          {/* <Footer /> */}
        </ScrollToTop>
      </BrowserRouter>
    </div>
  );

};

export default injectContext(Layout);
