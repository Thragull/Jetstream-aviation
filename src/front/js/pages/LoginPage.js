import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import cabin from "../../img/cabina-login.png";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import "../../styles/Login.css"

<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

export const LoginPage = () => {
    const { store, actions } = useContext(Context);
    const [departments, setDepartments] = useState([])
    const [employee, setEmployee] = useState({
        crew_id: "",
        password: ""
    })
    const navigate = useNavigate();

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setEmployee({ ...employee, [name]: value })
    }

    const login = async () => {
        try {
            const resp = await fetch(`${process.env.BACKEND_URL}/api/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(employee)
            });

            if (!resp.ok) {
                throw new Error("Incorrect crew_id or password");
            }

            const data = await resp.json()

            localStorage.setItem("jwt-token", data.token);

            actions.getEmployee()

            navigate("/worker")

            return data
        } catch (error) {
            Swal.fire({
                title: "Error",
                text: error.message,
                icon: "error",
                button: "Ok"
            });
        }
    }

    return (
        <div style={{ backgroundImage: `url(${cabin})`, width: "100vw", height: "100vh", backgroundSize: "cover", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <form className="form-login">
                <h2 className="login-title">Login</h2>
                <div className="form-group">
                    <label htmlFor="crew_id" className="form-label">Crew ID</label>
                    <input handleScript={handleInputChange} className="input-login" />
                </div>
                <div className="form-group">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input type="password" handleScript={handleInputChange} className="input-login" />
                </div>
                <button type="button" className="btn btn-secondary btn-full-width">Login</button>
            </form>
        </div>
    );
};

export default LoginPage;
