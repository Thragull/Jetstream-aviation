import React, { useContext, useState, useEffect } from "react";
import { Context } from "../../store/appContext";
import { faBedPulse } from "@fortawesome/free-solid-svg-icons";
import RegisterUser from "./ManagementComponents/RegisterUser";


export const ManagementComponent = () => {
	const { store, actions } = useContext(Context);
    const[users,setUsers] = useState(true)
    const [addUser, setAddUser] = useState(false)
    const activeColor = 'rgba(21, 39, 53,0.95)'
    const inactiveColor = 'rgba(255, 255, 255,0.5)'
    const [roles, setRoles] = useState([]);
    const [selectedRole, setSelectedRole] = useState(1)
    const [employees, setEmployees] = useState([])

    const fetchEmployees = async () => {
        const employeesData = await actions.getEmployeesByRol(selectedRole)
        setEmployees(employeesData)
    }

    useEffect(()=> {
        const fetchRoles = async () => {
            const rolesData = await actions.getRoles();
            setRoles(rolesData);
        };
    
        fetchRoles();

        fetchEmployees();


    },[]);

    const handleSelect = async (event) => {
        const value = await event.target.value
        setSelectedRole(value)
        fetchEmployees()
    }


	return (
        <div style={{maxHeight: '90vh', overflowY: 'auto'}}>
            <h1 className="mb-5">Management</h1>
            
            {   addUser ? <RegisterUser saveUserFunction={()=> setAddUser(false)}/> : 
                <div>

                    <div className="my-5 mx-3" style={{ height: '6vh'}}>
                        <div className="row" >
                            <div className="col-5">
                                <span className="input-group-text" id="basic-addon1">Role</span>
                                    <select 
                                        className="form-select form-select-lg mb-3" 
                                        aria-label="Large select example" 
                                        style={{height: '6vh', fontSize: '2vh'}}
                                        name="role_id"
                                        onChange={handleSelect}
                                        >
                                        <option selected>Select a Role</option>
                                       {
                                            roles.map((role, index)=> (
                                                <option key={index} value={role.id}>{role.role}</option>
                                            ))
                                        } 
                                    </select>
                            </div>
                            <div className="col-5">
                            <button  type="button" style={{width: '15vw'}} className="mx-3 my-3 col-3 btn btn-success" onClick={()=>{setAddUser(true)}}>Add User</button>
                            </div>
                            </div>
                    </div>   

                <table className="table">
                  <thead>
                    <tr>
                      <th scope="col">#</th>
                      <th scope="col">Name</th>
                      <th scope="col">Surname</th>
                      <th scope="col">Crew Id</th>
                      <th scope="col">Start Date</th>
                      <th scope="col">Email</th>
                      <th scope="col">Phone Number</th>
                    </tr>
                  </thead>
                  <tbody>
                    {
                        employees.map((employee, index)=> (
                            <tr key={index + 1}>
                                <th scope="row">{index + 1}</th>
                                <td>{employee.name}</td>
                                <td>{employee.surname}</td>
                                <td>{employee.crew_id}</td>
                                <td>{employee.entry_date}</td>
                                <td>{employee.email}</td>
                                <td>{employee.phone}</td>
                            </tr>
                        ))
                    }
                  
                  </tbody>
                </table>           
            </div>}
        </div>
	);
};

export default ManagementComponent; 