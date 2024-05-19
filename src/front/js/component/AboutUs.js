import React from "react";
import Navbar from "./Navbar";
import CabinCrew from "../../img/cabina-about.png";
import { Footer } from "./footer";
import "../../styles/AboutUs.css";

const AboutUs = () => {
  return (
    <div>
      <Navbar />
      <div className="about-us-container">
        <div className="overlay">
        <img src={CabinCrew} className="about-us-background" alt="CabinCrew" />
          <div className="p-4">
            <p>
              Welcome to JetStream, your gateway to bespoke air travel experiences.
              At JetStream, we pride ourselves on being more than just a
              charter airline. We're pioneers of personalized aviation. With a
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
            <p>
              Our ethos is rooted in a deep understanding of the transformative
              power of travel. Beyond merely transporting passengers from one
              destination to another, we believe in fostering connections, creating
              memories, and unlocking new horizons. With JetStream, each flight
              is an opportunity to embark on a journey of discovery, where the sky
              is not just a destination, but an infinite canvas of possibilities.
            </p>
            <p>
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
      </div>
      <Footer />
    </div>
  );
};

export default AboutUs;
