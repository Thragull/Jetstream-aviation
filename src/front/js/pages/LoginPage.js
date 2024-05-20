import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import cabin from "../../img/login-employe.webp";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import "../../styles/Login.css";

<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

export const LoginPage = () => {
    const { store, actions } = useContext(Context);
    const [employee, setEmployee] = useState({
        crew_id: "",
        password: ""
    });
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setEmployee({ ...employee, [name]: value });
    };

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

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

            const data = await resp.json();

            localStorage.setItem("jwt-token", data.token);

            actions.getEmployee();

            navigate("/worker");

            return data;
        } catch (error) {
            Swal.fire({
                title: "Error",
                text: error.message,
                icon: "error",
                button: "Ok"
            });
        }
    };

    return (
        <div className="page-login" style={{backgroundImage: `url(${cabin})`,}}>
            <form className="form-login">
                <h2 className="login-title">Login</h2>
                <div className="form-group">
                    <label htmlFor="crew_id" className="form-label">Crew ID</label>
                    <input
                        type="text"
                        name="crew_id"
                        value={employee.crew_id}
                        onChange={handleInputChange}
                        className="input-login"
                        placeholder="Enter your Crew ID"
                    />
                </div>
                <div className="form-group password-group">
                    <label htmlFor="password" className="form-label">Password</label>
                        <input
                            type={showPassword ? "text" : "password"}
                            name="password"
                            value={employee.password}
                            onChange={handleInputChange}
                            className="input-login password-input"
                            placeholder="Enter your password"
                        />
                        <span
                            className="password-toggle-icon"
                            onClick={togglePasswordVisibility}
                        >
                            <i className={showPassword ? "fas fa-eye-slash" : "fas fa-eye"}></i>
                        </span>
                </div>
                <button type="button" onClick={login} className="btn btn-secondary btn-full-width">Login</button>
            </form>
        </div>
    );    
};

export default LoginPage;
