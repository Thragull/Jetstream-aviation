import { Context } from "../../../store/appContext";
import React, { useContext, useState, useEffect } from "react";


export const FlightsTable = (props) => {
	const { store, actions } = useContext(Context);

	return (
     <div className="input-group mb-3 mx-3">
        <table className="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Aircraft</th>
      <th scope="col">Departure Airport</th>
      <th scope="col">Arrival Airport</th>
      <th scope="col">LT Dep:</th>
      <th scope="col">LT Arr:</th>
      <th scope="col">Flight Number</th>
    </tr>
  </thead>
  <tbody>
    {props.map()}
  </tbody>
</table>
     </div>
	);
};

export default FlightsTable; 
