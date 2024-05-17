import React from "react";
import LogoJetstream from "../../img/LogoJetstream.png";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faInstagram, faTwitter, faFacebook } from '@fortawesome/free-brands-svg-icons';

export const Footer = () => (
  <div className="FooterBar">
    <footer className="footer-dad">
      <div className="footer">
        <div className="footer-section text-center">
          <img
            src={LogoJetstream}
            alt="Logo"
            className="footer-logo"
          />
        </div>
        <div className="footer-section">
          <h2 className="footer-heading">Address</h2>
          <p className="footer-text">
            1234 Willow Street <br />
            Oakwood, TX 78901 <br />
            United States
          </p>
        </div>
        <div className="footer-section">
          <h2 className="footer-heading">Social Media</h2>
          <div className="social-icons text-center">
            <a href="https://www.instagram.com">
              <FontAwesomeIcon icon={faInstagram} className="icon" />
            </a>
            <a href="https://www.twitter.com">
              <FontAwesomeIcon icon={faTwitter} className="icon" />
            </a>
            <a href="https://www.facebook.com">
              <FontAwesomeIcon icon={faFacebook} className="icon" />
            </a>
          </div>
        </div>
        <div className="footer-section">
          <h2 className="footer-heading">Support</h2>
          <p className="footer-text">Lorem ipsum dolor sit amet.</p>
        </div>
        <div className="footer-section">
          <h2 className="footer-heading">Work with Us</h2>
          <p className="footer-text">Lorem ipsum dolor sit amet.</p>
        </div>
      </div>
      <div className="copy-right">
        <p>&copy; {new Date().getFullYear()} JetStream. All rights reserved.</p>
      </div>
    </footer>
  </div>
);
