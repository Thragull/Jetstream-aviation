import React from "react";
import Navbar from "./Navbar";
import { Link } from "react-router-dom";
import { Footer } from "./footer";

const Services = () => {
  return (
    <div>
      <Navbar />

      <div className="ServicesCards row">
        <div className="col-lg-4 col-md-6 col-sm-12">
          <div className="card-serv mt-2 ms-2">
            <img
              className="ImgServices"
              src="https://res.cloudinary.com/dhwe9frkd/image/upload/v1714073446/samples/JetStream/ACMI-Lease_xl6zm9.png"
            ></img>
            <div className="card-body-serv">
              <h5 className="ST card-title-serv text-center p-2">ACMI Lease</h5>
              <p className="card-text-serv pt-2">
                An ACMI lease refers to a specialized aircraft leasing arrangement encompassing Aircraft, Crew, Maintenance, and Insurance services.
              </p>
              <p className="card-text-serv pt-2">Through this lease, Jetstream provides clients with access to aircraft, along with trained crew members, comprehensive maintenance support, and insurance coverage for a predetermined duration.</p>
              <p className="card-text-serv pt-2">This arrangement allows Jetstream's clients to address short-term operational needs or seasonal demand fluctuations efficiently without the burden of long-term commitments or investment in their fleet.</p>
            </div>
          </div>
        </div>

        <div className="col-lg-4 col-md-6 col-sm-12">
          <div className="card-serv mt-2 ms-2">
            <img
              className="ImgServices"
              src="https://res.cloudinary.com/dhwe9frkd/image/upload/v1714073698/samples/JetStream/charter_u04vqv.webp"
            ></img>
            <div className="card-body-serv">
              <h5 className="ST card-title-serv text-center p-2">Charter Flights</h5>
              <p className="card-text-serv pt-2">
                On JetStream, charter flights provide customized air travel solutions tailored to clients' specific needs, offering flexible departure times, routes, and aircraft selection for a personalized travel experience.
              </p>
              <p className="card-text-serv pt-2">
                Whether for business or leisure purposes, Jetstream's charter flights cater to individual preferences, ensuring comfort, privacy, and efficiency throughout the journey.
              </p>
              <p className="card-text-serv pt-2">
                With dedicated customer service and a diverse fleet of aircraft, Jetstream's charter flights offer unparalleled flexibility and convenience for discerning travelers.
              </p>
            </div>
          </div>
        </div>

        <div className="col-lg-4 col-md-6 col-sm-12">
          <div className="card-serv mt-2 ms-2">
            <img
              className="ImgServices"
              src="https://res.cloudinary.com/dhwe9frkd/image/upload/v1714074029/samples/JetStream/azafata_elejsn.jpg"
            ></img>
            <div className="card-body-serv">
              <h5 className="ST card-title-serv text-center p-2">Aircraft Management</h5>
              <p className="card-text-serv pt-2">
                On JetStream, aircraft management refers to the comprehensive services provided to aircraft owners to streamline operations and maximize the value of their assets.</p>
              <p className="card-text-serv pt-2">Jetstream offers a range of management solutions, including maintenance oversight, crew staffing, scheduling, and regulatory compliance.</p>
              <p className="card-text-serv pt-2">By entrusting their aircraft to Jetstream, owners can enjoy hassle-free ownership while Jetstream ensures the aircraft's safety, efficiency, and performance. With Jetstream's expertise and personalized approach, aircraft owners can optimize their investment.
              </p>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="button-div-serv col-12 text-center">
            <Link to="/contact">
              <a href="#" className="btnServices btn btn">
                Get your Budget
              </a>
            </Link>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Services;
