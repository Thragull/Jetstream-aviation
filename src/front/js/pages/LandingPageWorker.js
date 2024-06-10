import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import { useNavigate, Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCalendarCheck, faDoorOpen, faHouse, faUser, faMoneyBills, faUserGraduate, faFile, faBarsProgress, faFileInvoice, faBars } from '@fortawesome/free-solid-svg-icons';
import DashboardComponent from "../component/landingPageComponents/DashboardComponent.js";
import ProfileComponent from "../component/landingPageComponents/ProfileComponent.js";
import PayslipComponent from "../component/landingPageComponents/PayslipComponent.js";
import DocumentComponent from "../component/landingPageComponents/DocumentComponent.js";
import MoodelsComponent from "../component/landingPageComponents/MoodelsComponent.js";
import HolidaysComponent from "../component/landingPageComponents/HolidayComponent.js";
import RosterComponent from "../component/landingPageComponents/RosterComponent.js";
import ManagementComponent from "../component/landingPageComponents/ManagementComponent.js";
import CrewControllerComponent from "../component/landingPageComponents/CrewControllerComponent.js";
import Budgets from "../component/Budgets/Budgets.js";
import "../../styles/landing_page_worker.css";
import Logo from "../../img/logoconfondo.jpeg";

export const LandingPageWorker = () => {
    const navigate = useNavigate();
    const { store, actions } = useContext(Context);
    const [activeComponent, setActiveComponent] = useState('Roster');
    const [menuOpen, setMenuOpen] = useState(false);

    useEffect(() => {
        if (localStorage.getItem('jwt-token') == null) {
            navigate("/login");
        }
    }, [navigate]);

    const renderComponent = () => {
        switch (activeComponent) {
            case 'Dashboard':
                return store.loggedInEmployee.department_id === 1 ? <Budgets /> : <DashboardComponent />;
            case 'Profile':
                return <ProfileComponent />;
            case 'Payslip':
                return <PayslipComponent />;
            case 'Documents':
                return <DocumentComponent />;
            case 'Moodels':
                return <MoodelsComponent />;
            case 'Holidays':
                return <HolidaysComponent />;
            case 'Roster':
                if (store.loggedInEmployee.department_id === 3) {
                    return <RosterComponent />;
                } else if (store.loggedInEmployee.department_id === 2) {
                    return <CrewControllerComponent />;
                } else {
                    return <ManagementComponent />;
                }
            default:
                return <DashboardComponent />;
        }
    };

    return (
        <div className="landing-page">
            {store.loggedInEmployee == null ?
                <div className="loading">Loading...</div> :
                <>
                    <div className="navbar">
                        <div className="navbar-header">
                            <img className="logo rounded-circle" src={Logo} alt="Logo" />
                            <p className="employee-name">{store.loggedInEmployee.name}</p>
                        </div>
                        <div className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
                            <FontAwesomeIcon icon={faBars} />
                        </div>
                        <div className={`menu ${menuOpen ? 'open' : ''}`}>
                            <div className={`menu-item ${activeComponent === 'Dashboard' ? 'active' : ''}`} onClick={() => { setActiveComponent('Dashboard'); setMenuOpen(false); }}>
                                <FontAwesomeIcon icon={store.loggedInEmployee.department_id === 1 ? faFileInvoice : faHouse} />
                                <p>{store.loggedInEmployee.department_id === 1 ? "Budgets" : "Dashboard"}</p>
                            </div>
                            <div className={`menu-item ${activeComponent === 'Profile' ? 'active' : ''}`} onClick={() => { setActiveComponent('Profile'); setMenuOpen(false); }}>
                                <FontAwesomeIcon icon={faUser} />
                                <p>Profile</p>
                            </div>
                            <div className={`menu-item ${activeComponent === 'Roster' ? 'active' : ''}`} onClick={() => { setActiveComponent('Roster'); setMenuOpen(false); }}>
                                <FontAwesomeIcon icon={store.loggedInEmployee.department_id === 1 ? faBarsProgress : faCalendarCheck} />
                                <p>{store.loggedInEmployee.department_id === 3 ? "Roster" : store.loggedInEmployee.department_id === 2 ? "Crew Control" : "Management"}</p>
                            </div>
                            <div className={`menu-item ${activeComponent === 'Payslip' ? 'active' : ''}`} onClick={() => { setActiveComponent('Payslip'); setMenuOpen(false); }}>
                                <FontAwesomeIcon icon={faMoneyBills} />
                                <p>Payslip</p>
                            </div>
                            <div className={`menu-item ${activeComponent === 'Documents' ? 'active' : ''}`} onClick={() => { setActiveComponent('Documents'); setMenuOpen(false); }}>
                                <FontAwesomeIcon icon={faFile} />
                                <p>Documents</p>
                            </div>
                            <div className={`menu-item ${activeComponent === 'Moodels' ? 'active' : ''}`} onClick={() => { setActiveComponent('Moodels'); setMenuOpen(false); }}>
                                <FontAwesomeIcon icon={faUserGraduate} />
                                <p>Moodels</p>
                            </div>
                            <Link to="/" onClick={() => { actions.logout(); setMenuOpen(false); }} className="menu-item logout">
                                <FontAwesomeIcon icon={faDoorOpen} />
                                <p>Log Out</p>
                            </Link>
                        </div>
                    </div>
                    <div className="main-content">
                        {renderComponent()}
                    </div>
                </>
            }
        </div>
    );
};

export default LandingPageWorker;
