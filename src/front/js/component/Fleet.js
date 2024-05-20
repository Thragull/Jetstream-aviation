import React, { useState } from "react";
import Navbar from "./Navbar";
import Plane from "./Plane";
import { Footer } from "./footer";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronLeft, faChevronRight } from "@fortawesome/free-solid-svg-icons";
import "../../styles/Fleet.css";

import IMG1 from "../../img/A320.png";
import IMG2 from "../../img/A321.png";
import IMG3 from "../../img/A330.png";
import IMG4 from "../../img/A350.png";
import IMG5 from "../../img/B737.png";
import IMG6 from "../../img/B777.png";
import IMG7 from "../../img/B787.png";

const Fleet = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const fleetInfo = [
      { title: "Airbus A320", text: "x2", imgSrc: IMG1 },
      { title: "Airbus A321", text: "x2", imgSrc: IMG2 },
      { title: "Airbus A330", text: "x2", imgSrc: IMG3 },
      { title: "Airbus A350", text: "x2", imgSrc: IMG4 },
      { title: "Boeing B737", text: "x2", imgSrc: IMG5 },
      { title: "Boeing B777", text: "x4", imgSrc: IMG6 },
      { title: "Boeing B787", text: "x4", imgSrc: IMG7 },
  ];

  const handlePrevClick = () => {
    setCurrentIndex((prevIndex) => (prevIndex === 0 ? fleetInfo.length - 1 : prevIndex - 1));
  };

  const handleNextClick = () => {
    setCurrentIndex((prevIndex) => (prevIndex === fleetInfo.length - 1 ? 0 : prevIndex + 1));
  };

  return (
    <div>
      <Navbar />
      <div className="container-fleet">
        <div className="fleet-cards">
          <button className="arrow left-arrow" onClick={handlePrevClick}>
            <FontAwesomeIcon icon={faChevronLeft} />
          </button>
          <Plane
            title={fleetInfo[currentIndex].title}
            text={fleetInfo[currentIndex].text}
            imgSrc={fleetInfo[currentIndex].imgSrc}
          />
          <button className="arrow right-arrow" onClick={handleNextClick}>
            <FontAwesomeIcon icon={faChevronRight} />
          </button>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Fleet;
