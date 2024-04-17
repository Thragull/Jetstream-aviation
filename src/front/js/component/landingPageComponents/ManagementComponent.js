import React, { useContext, useState } from "react";
import { Context } from "../../store/appContext";
import { faBedPulse } from "@fortawesome/free-solid-svg-icons";
import RegisterUser from "./ManagementComponents/RegisterUser";


export const ManagementComponent = () => {
	const { store, actions } = useContext(Context);
    const[users,setUsers] = useState(true)
    const [addUser, setAddUser] = useState(false)
    const activeColor = 'rgba(21, 39, 53,0.95)'
    const inactiveColor = 'rgba(255, 255, 255,0.5)'

	return (
        <div>
            <h1>Management</h1>
            
            {   addUser ? <RegisterUser saveUserFunction={()=> setAddUser(false)}/> : 
                <div className="row">
                <button type="button" className="col-5 btn" onClick={()=> setUsers(true)}
                    style={{color: `${users ?  "white" : "black"}`,
                            backgroundColor:  `${users ?  activeColor : inactiveColor}`
                        }} >Users</button>
                <button type="button" className="col-5 btn" onClick={()=> setUsers(false)}
                    style={{color: `${users ?  "black" : "white"}`,
                            backgroundColor:  `${users ?  inactiveColor : activeColor}`
                    }}>Projects</button>
            <button type="button" className="mx-3 my-3 col-3 btn btn-success" onClick={()=>{setAddUser(true)}}>Add User</button>
            </div>}
        </div>
	);
};

export default ManagementComponent; 