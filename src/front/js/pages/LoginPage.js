import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import cabin from "../../img/cabin.jpeg";
import InputComponent from "../component/landingPageComponents/reusableComponents/InputComponent";
import { Link, useNavigate } from "react-router-dom";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Swal from "sweetalert2";
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>


export const LoginPage = () => {
    const { store, actions } = useContext(Context);
    const [departments, setDepartments] = useState([])
    const [employee, setEmployee] = useState({
        department_id: 0,
        crew_id: "",
        password: ""
    })
    const navigate = useNavigate();


    useEffect(()=>{
        const fetchDepartments = async() => {
            const departmentsData = await actions.getDepartments()
            setDepartments(departmentsData)
        }

        fetchDepartments();
    }, [])

    const handleInputChange = (event) => {
        const {name, value} = event.target; 
        setEmployee({...employee, [name]: value})
    }

    const handleSelectChange = (event) => {
        const {name, value} = event.target
        setEmployee({...employee, [name]: parseInt(value, 10)})
    }

    useEffect(()=>{
        console.log(employee);
    }, [employee])



    const login = async() => {
        try {
            const resp = await fetch(`${process.env.BACKEND_URL}/api/login`, {
                method: "POST",
                headers: {"Content-Type": "application/json"}, 
                body: JSON.stringify(employee)
            });
    
            if(!resp.ok) {
                throw new Error("Incorrect crew_id or password");
            }
    
            const data = await resp.json()
            //Guarda el token en el local Storage
            //También deberías almacenar el usuario en la store utilizando la función setItem
            localStorage.setItem("jwt-token", data.token);
    
            console.log("Login successful")
            console.log(`${data.token}`)
            navigate("/worker")
    
            return data
        } catch (error) {
            // Si hay un error, muestra la alerta de error
            Swal.fire({
                title: "Error",
                text: error.message,
                icon: "error",
                button: "Ok"
            });
        }
    }
    


    return (
        <div style={{backgroundImage: `url(${cabin})`, width: "100vw", height: "100vh", backgroundSize: "cover", display: "flex", alignItems: "center", justifyContent: "center"}}>
            <div style={{textAlign: "center"}}>
                <p className="mb-5" style={{fontSize: "10vh", color: "white"}}>LOGIN</p>
                <div className="form">
                    <InputComponent label="Crew ID" name="crew_id" handleScript={handleInputChange}/>
                    <InputComponent label="Password" name="password" handleScript={handleInputChange}/>
                </div>
                <button type="button" onClick={login} className="btn btn-success">Log in</button>
            </div>
        </div>
    );
};

export default LoginPage;