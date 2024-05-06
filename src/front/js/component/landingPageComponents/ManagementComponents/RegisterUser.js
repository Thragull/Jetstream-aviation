import React, {useState, useContext, useEffect, useRef } from "react";
import { Context } from "../../../store/appContext";
import InputComponent from "../reusableComponents/InputComponent";
import { any } from "prop-types";
<script src="https://cdnjs.cloudflare.com/ajax/libs/air-datepicker/2.2.3/js/i18n/datepicker.en.js"></script>



export const RegisterUser = (props) => {
   
    const { store, actions } = useContext(Context);
    const datepickerRef = useRef(null);

    const [roles, setRoles] = useState([]);
    const [departments, setDepartments] = useState([])
    const [crewIDEmployees, setCrewIdEmployees] = useState([])
    const [newEmployee, setNewEmployee ]= useState({
        name: "",
        surname: "",
        email: "",
        password: "",
        crew_id: null,
        role_id: null,
        department_id: null,
        gender: null,

    })
    const [errors, setErrors] = useState({});


    useEffect(()=> {
        const fetchRoles = async () => {
            const rolesData = await actions.getRoles();
            setRoles(rolesData);
        };
    
        fetchRoles();

        const fetchDepartments = async () => {
            const departmentsData = await actions.getDepartments();
            setDepartments(departmentsData)
        }

        fetchDepartments();

        const fetchEmployeesbyCrewID = async() => {
        const crewIDEmployeesData = await actions.getEmployeesByCrewId();
        setCrewIdEmployees(crewIDEmployeesData)
        }
        fetchEmployeesbyCrewID();
    },[]);

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setNewEmployee({ ...newEmployee, [name]: value });
    };

    const handleSelectChange = (event) => {
        const {name, value} = event.target;
        setNewEmployee({...newEmployee, [name]: value})
    }

    useEffect(()=>{
        console.log(newEmployee);
    }, [newEmployee])


    const validateForm = () => {
        let valid = true;
        const errors = {};

        // Ejemplo de validación básica para el campo de correo electrónico
        if (!newEmployee.email || !/^\S+@\S+\.\S+$/.test(newEmployee.email)) {
            errors.email = "Please enter a valid email address";
            valid = false;
        }

        if(newEmployee.crew_id == null) {
            errors.crew_id = "Please fill in the Crew Id field"
            valid = false;
        }

        if(newEmployee.name.length == 0) {
            errors.name = "Please fill in the Name field"
            valid = false;
        }

        if(newEmployee.surname.length == 0) {
            errors.name = "Please fill in the Surname field"
            valid = false;
        }

        if(newEmployee.department_id == null || newEmployee.department_id.length > 1 ) {
            errors.department_id = "Please select a department"
            valid = false;
        }

        if(newEmployee.role_id==null  || newEmployee.role_id.length > 1) {
            errors.department_id = "Please select a role"
            valid = false;
        }
        
        const crewIdUsed = crewIDEmployees.some(employee => employee.crew_id === newEmployee.crew_id);
        if (crewIdUsed) {
            console.log('Crew ID used')
            errors.crew_id = "Crew ID already in use";
            valid = false;
        }
    
        // Agrega más validaciones para otros campos aquí

        setErrors(errors);
        return valid;
    };


    const createEmployeeFunction = async () => {
        if(validateForm()) {
        try {
            const response = await fetch(`${process.env.BACKEND_URL}/api/signupEmployee`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newEmployee),
            });
            if (response.ok) {
                console.log("Employee successfully added to database");
                // Limpiar el formulario o realizar cualquier otra acción necesaria
            } else {
                const data = await response.json();
                console.error(data.msg);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }
    };


    return (
        <div>
            <h1 className="mb-5">Edit Profile</h1>
            <div className="form">
                <div style={{display: "flex"}}>
                    <InputComponent label="Name" placeholder="Name" name="name" value={newEmployee.name} handleScript={handleInputChange}/> 
                    <InputComponent label="Surname" placeholder="Surname" name="surname" value={newEmployee.surname} handleScript={handleInputChange}/> 
                </div>
                <div style={{display: "flex"}}>
                   {/*  {errors.crew_id && <span className="text-danger">{errors.crew_id}</span>} */}
                    <InputComponent label="Id" placeholder="Id" name="crew_id" value={newEmployee.crew_id} handleScript={handleInputChange}/> 
                </div>
                <div style={{display: "flex"}}>
                    {/* {errors.email && <span className="text-danger">{errors.email}</span>} */}
                    <InputComponent label="e-mail" placeholder="email" name="email" value={newEmployee.email} handleScript={handleInputChange} /> 
                    <InputComponent label="Password" placeholder="Password" name="password" value={newEmployee.password} handleScript={handleInputChange}/> 
                </div>
                <div className="row">
                    <div className="col-5 mb-3 mx-3" style={{display: "flex", height: '6vh'}}>
                        <span className="input-group-text" id="basic-addon1">Role</span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '6vh', fontSize: '2vh'}}
                                name="role_id"
                                onChange={handleSelectChange}
                                >
                                <option selected>Select a Role</option>
                               {
                                    roles.map((role, index)=> (
                                        <option key={index} value={role.id}>{role.role}</option>
                                    ))
                                } 
                            </select>
                    </div>
                    <div className="col-5 mb-3 mx-3" style={{display: "flex", height: '6vh'}}>
                        <span className="input-group-text" id="basic-addon1">Department</span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '6vh', fontSize: '2vh'}}
                                name="department_id"
                                onChange={handleSelectChange}
                                >
                                <option selected>Select a Deparment</option>
                               {
                                    departments.map((department, index)=> (
                                        <option key={index} value={department.id}>{department.department}</option>
                                    ))
                                } 
                            </select>
                    </div>
                    <div className="col-5 mb-3 mx-3" style={{display: "flex", height: "6vh"}}>
                        <span className="input-group-text" id="basic-addon1">Gender</span>
                        <select 
                            className="form-select form-select-lg mb-3" 
                            aria-label="Large select example" 
                            style={{height: '6vh', fontSize: '2vh'}}
                            name="gender"
                            onChange={handleSelectChange}
                            >
                            <option selected value="Male">Male</option>
                            <option selected value="Female">Female</option>
                        </select>
                    </div>
                </div>
                <div className="my-5">
                    <button onClick={createEmployeeFunction} type="button" className="btn btn-warning">Save User</button>
                </div>
                    <div>
                         {
                             Object.entries(errors).map(([key, value], index) => (
                                 <div className="alert alert-danger" key={index} style={{height: "3vh", fontSize: "2vh"}}>{value}</div>
                             ))
                         }
                    </div>
            </div>
        </div>
    );
};

export default RegisterUser;
