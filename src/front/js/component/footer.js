import React, { Component } from "react";
import LogoJetstream from "../../img/LogoJetstream.png";

export const Footer = () => (
	
	<div className="FooterBar" >
	<footer className="footer mt-auto py-3 ms-5">
		<div className="row">
			<div className="col-5 text-white mt-5"> 
			<h1><b>Adress:</b></h1>
			<p className="fs-1">
1234 Willow Street
Oakwood, TX 78901
United States</p>
<h1><b> Social Medias:</b></h1>
			<p className="fs-1 ">
            Instagram
			</p>
			<p className="fs-1">Twitter</p>
			<p className="fs-1">Facebook</p>

			</div>

			<div className="col-4 text-white mt-5 ">
            <h1><b> Support</b></h1>
			<div>-</div>
			<h1><b> Work with Us</b></h1>
			<div>-</div>
			<h1><b>Terms and Conditions</b></h1>
			<div>-</div>
			<h1><b>Bagagge Policy</b></h1>
			<div>-</div>
			<h1><b>FAQs</b></h1>
			</div>
			
			<div className="col-3">
            <img
			        id="LogoFooter"
                    src={LogoJetstream}
                    
                  />
			</div>
		</div>
	</footer>
	</div>
	
);
