import React from "react";
import Navbar from "./Navbar";
import Plane from "./Plane";
import A320Img from "../../img/A320Img.jpg";
import { Footer } from "./footer";

const Fleet = () => {
  let fleetInfo = [
    {
      title: "Airbus A320",
      text: "x2",
      imgSrc:
        "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201260/samples/JetStream/A320Img_yhjrg9.jpg",
    },
    { title: "Airbus A321", text: "x2", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201851/samples/JetStream/A321_ras1af.jpg" },
    { title: "Airbus A330", text: "x2", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201266/samples/JetStream/A330Img_alcwcm.jpg" },
    { title: "Airbus A350", text: "x2", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201270/samples/JetStream/A350Img_l1bxjk.jpg" },
    { title: "Boeing B737", text: "x2", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201273/samples/JetStream/B737Img_ux5pvn.jpg" },
    { title: "Boeing B777", text: "x4", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201279/samples/JetStream/B777Img_iyj7da.jpg" },
    { title: "Boeing B787", text: "x4", imgSrc: "https://res.cloudinary.com/dhwe9frkd/image/upload/v1713201277/samples/JetStream/B787Img_bar9qe.jpg" },
  ];
  return (
    <div>
      <div>
        <Navbar />
      </div>
      <div className="FleetCards row ">

        {fleetInfo.map((value, index) => {
          return (
            <div className="col-4">
              <Plane
              key={index}
              title={value.title}
              text={value.text}
              imgSrc={value.imgSrc}
            />
            </div>
          );
        })}
        {/* <Navbar/>
      <Plane title="Airbus A320" text="x2" />
      <Plane title="Airbus A321" text="x2" />
      <Plane title="Airbus A330" text="x2"/>
      <Plane title="Airbus A350" text="x2"/>
      <Plane title="Boeing 737" text="x2"/>
      <Plane title="Boeing 777" text="x4"/>
      <Plane title="Boeing 787" text="x4"/> */}
      </div>
      <Footer />
    </div>
  );
};

export default Fleet;

// https://asset.cloudinary.com/dhwe9frkd/8af75816aaa6b0737d52accbf97a236f (B777)
// https://asset.cloudinary.com/dhwe9frkd/5672727edd80076632f57d0d6534a1a8 (B787)
// https://asset.cloudinary.com/dhwe9frkd/04ee07bcb0754769eb10c7ecafdc126e (B737)
// https://asset.cloudinary.com/dhwe9frkd/7a8afebe3bee2e3ecaa14638b43743b0 (A350)
// https://asset.cloudinary.com/dhwe9frkd/ca739168a805ecf39cd0ddce3a009cb8 (A330)
// https://asset.cloudinary.com/dhwe9frkd/ca739168a805ecf39cd0ddce3a009cb8 (A320)
// https://asset.cloudinary.com/dhwe9frkd/a1bd1298d7454735b6903521c9bb67b9 (A321)
