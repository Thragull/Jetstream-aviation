import React from 'react'

// import A321Img from "../../img/A321Img.jpg";
// import A330Img from "../../img/A330Img.jpg";
// import A350Img from "../../img/A350Img.jpg";
// import B737Img from "../../img/B737Img.jpg";
// import B777Img from "../../img/B777Img.jpg";
// import B787Img from "../../img/B787Img.jpg";

const styles =() => {
    width:"18rem"
}
const Plane = (props) => {
  return (
    <div className="justify-content-center m-5">
      <div className="container">
        <div className="col-md-5">
          <div className="card" styles={styles}> 
          {/* o {{width:"18rem"}}> */}
            <img src={props.imgSrc} className="card-img-top text-center" />
            <div className="card-body">
              <h5 className="card-title text-center">{props.title}</h5>
              <p className="card-text text-center">{props.text}</p>
             
            </div>
          </div>
        </div>
        </div>
        </div>
  )
}

export default Plane;

{/* <div>
    <div><Navbar/></div>
    <div className="container mt-5 pt-5 pb-4">
      <div className="row">
        <div className="col-md-4">
          <div className="card mb-4">
            <img src="https://via.placeholder.com/150" className="card-img-top" alt="Placeholder" />
            <div className="card-body">
              <h5 className="card-title">Card 1</h5>
              <p className="card-text">This is a sample card.</p>
              <a href="#" className="btn btn-primary">Go somewhere</a>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card mb-4">
            <img src="https://via.placeholder.com/150" className="card-img-top" alt="Placeholder" />
            <div className="card-body">
              <h5 className="card-title">Card 2</h5>
              <p className="card-text">This is another sample card.</p>
              <a href="#" className="btn btn-primary">Go somewhere</a>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card mb-4">
            <img src="https://via.placeholder.com/150" className="card-img-top" alt="Placeholder" />
            <div className="card-body">
              <h5 className="card-title">Card 3</h5>
              <p className="card-text">This is yet another sample card.</p>
              <a href="#" className="btn btn-primary">Go somewhere</a>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card mb-4">
            <img src="https://via.placeholder.com/150" className="card-img-top" alt="Placeholder" />
            <div className="card-body">
              <h5 className="card-title">Card 4</h5>
              <p className="card-text">This is the final sample card.</p>
              <a href="#" className="btn btn-primary">Go somewhere</a>

            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card mb-4">
            <img src="https://via.placeholder.com/150" className="card-img-top" alt="Placeholder" />
            <div className="card-body">
              <h5 className="card-title">Card 4</h5>
              <p className="card-text">This is the final sample card.</p>
              <a href="#" className="btn btn-primary">Go somewhere</a>

            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card mb-4">
            <img src="https://via.placeholder.com/150" className="card-img-top" alt="Placeholder" />
            <div className="card-body">
              <h5 className="card-title">Card 4</h5>
              <p className="card-text">This is the final sample card.</p>
              <a href="#" className="btn btn-primary">Go somewhere</a>

            </div>
          </div>
        </div>

        
      </div>
    </div>
  </div>  
  );
}

export default Fleet; */}


// const Fleet = () => {
//   return (
//     <div>
//       <div>
//         <Navbar />
//       </div>
//       <div className="text-center mt-5 mb-5 text-primary-emphasis">
//         <h1>Fleet</h1>
//       </div>
//       <div className="row">
//         <div className="col">
//           <div className="card" style="width: 18rem;">
//             <img src={Avion1} className="card-img-top" alt="..." />
//             <div className="card-body">
//               <p className="card-text">
//                 Some quick example text to build on the card title and make up
//                 the bulk of the card's content.
//               </p>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };
