import React, { useRef } from "react";
import Navbar from "./Navbar";
import Plane from "./Plane";
import { Footer } from "./footer";
import "../../styles/Fleet.css";

const Fleet = () => {
  const fleetContainerRef = useRef(null);

  let fleetInfo = [
    { title: "Airbus A320", text: "x2", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201260/samples/JetStream/A320Img_yhjrg9.jpg", },
    { title: "Airbus A321", text: "x2", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201851/samples/JetStream/A321_ras1af.jpg" },
    { title: "Airbus A330", text: "x2", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201266/samples/JetStream/A330Img_alcwcm.jpg" },
    { title: "Airbus A350", text: "x2", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201270/samples/JetStream/A350Img_l1bxjk.jpg" },
    { title: "Boeing B737", text: "x2", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201273/samples/JetStream/B737Img_ux5pvn.jpg" },
    { title: "Boeing B777", text: "x4", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201279/samples/JetStream/B777Img_iyj7da.jpg" },
    { title: "Boeing B787", text: "x4", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201277/samples/JetStream/B787Img_bar9qe.jpg" },
  ];

  return (
    <div>
      <Navbar />
      <div className="container-fleet">
        <div className="fleet-cards" ref={fleetContainerRef}>
          {fleetInfo.map((value, index) => (
            <Plane
              key={index}
              title={value.title}
              text={value.text}
              imgSrc={value.imgSrc}
            />
          ))}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Fleet;
