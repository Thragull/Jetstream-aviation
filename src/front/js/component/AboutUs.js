import React from "react";
import Navbar from "./Navbar";
import CabinCrew from "../../img/CabinCrew.jpg";

const AboutUs = () => {
  return (
    <div>
      <Navbar />

      <div className="text-center mt-5 text-primary-emphasis">
        <h1> About us </h1>
      </div>
      <div className="p-5 text-center fs-4">
        <p>
          Welcome to JetStream, your gateway to bespoke air travel experiences.
          At [Airline Name], we pride ourselves on being more than just a
          charter airline – we're pioneers of personalized aviation. With a
          steadfast commitment to safety, reliability, and luxury, we redefine
          the art of flying, offering discerning travelers the freedom to soar
          to new heights in unparalleled comfort and style.
        </p>
        <p>
          At JetStream, our story is one of passion for aviation and dedication
          to our passengers. With a fleet of meticulously maintained aircraft
          and a team of seasoned professionals at the helm, we ensure every
          journey is a seamless fusion of efficiency and elegance. From intimate
          escapes to corporate retreats, we specialize in crafting bespoke
          itineraries that cater to the unique preferences and requirements of
          our clientele.
        </p>
      </div>
      <div>
        <img
          src={CabinCrew}
          className="CabinCrew text-center ms-5 ps-2 pb-4"
          alt="CabinCrew"
        />
      </div>
      <div>
        <p className="pb-2 text-center fs-4 ms-5 me-5">
          Our ethos is rooted in a deep understanding of the transformative
          power of travel. Beyond merely transporting passengers from one
          destination to another, we believe in fostering connections, creating
          memories, and unlocking new horizons. With JetStream, each flight
          is an opportunity to embark on a journey of discovery, where the sky
          is not just a destination, but an infinite canvas of possibilities.
        </p>
        <p className="pb-4 pt-2 text-center fs-4 ms-5 me-5">
          At JetStream, we embrace innovation and excellence at every
          turn. From our cutting-edge technology to our impeccable service
          standards, we continuously strive to set new benchmarks in the world
          of charter aviation. With a steadfast commitment to sustainability and
          environmental stewardship, we ensure our operations leave a positive
          impact on the planet, preserving the beauty of the skies for
          generations to come.
        </p>
      </div>
    </div>
  );
};

export default AboutUs;
