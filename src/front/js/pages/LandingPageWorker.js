import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import airplanebackground from "../../img/aviondesdeabajo.jpeg";
import "../../styles/landing_page_worker.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCalendarCheck, faHouse, faUser, faMoneyBills, faUserGraduate, faFile, faUmbrellaBeach, faBarsProgress, faFileInvoice } from '@fortawesome/free-solid-svg-icons'
import DashboardComponent from "../component/landingPageComponents/DashboardComponent.js"
import ProfileComponent from "../component/landingPageComponents/ProfileComponent.js"
import PayslipComponent from "../component/landingPageComponents/PayslipComponent.js"
import DocumentComponent from "../component/landingPageComponents/DocumentComponent.js"
import MoodelsComponent from "../component/landingPageComponents/MoodelsComponent.js"
import HolidaysComponent from "../component/landingPageComponents/HolidayComponent.js"
import RosterComponent from "../component/landingPageComponents/RosterComponent.js";
import ManagementComponent from "../component/landingPageComponents/ManagementComponent.js";
import Lottie from "react-lottie";
import animationData from "../../img/animation_data.json";
import CrewControllerComponent from "../component/landingPageComponents/CrewControllerComponent.js";
import Budgets from "../component/Budgets/Budgets.js";







export const LandingPageWorker = () => {

      const defaultOptions = {
            loop: true,
            autoplay: true,
            animationData: animationData, 
            renderSettings: {
                preserveAspectRatio: "xMidYMid slice"
            }
    }
    

    const { store, actions } = useContext(Context);

    const [manager, setManager] = useState(false)
    const [activeComponent, setActiveComponent] = useState('Roster')
    const [colorProfile, setColorProfile] = useState('transparent')
    const [colorDashboard, setColorDashboard] = useState('transparent')
    const [colorPayslip, setColorPayslip] = useState('transparent')
    const [colorDocuments, setColorDocuments] = useState('transparent')
    const [colorMoodels, setColorMoodels] = useState('transparent')
    const [colorHolidays, setColorHolidays] = useState('transparent')
    const [colorRoster, setColorRoster] = useState('transparent')
    const [dashboardRadius, setDashboardRadius] = useState(activeRadius);
    const [profileRadius, setProfileRadius] = useState(activeRadius);
    const [roosterRadius, setRosterRadius] = useState(activeRadius);
    const [payslipRadius, setPayslipRadius] = useState(activeRadius);
    const [documentsRadius, setDocumentsRadius] = useState(activeRadius);
    const [moodelsRadius, setMoodelsRadius] = useState(activeRadius);
    const [holidaysRadius, setHolidaysRadius] = useState(activeRadius);
    const [textColorProfile, setTextColorProfile] = useState('white')
    const [textColorDashboard, setTextColorDashboard] = useState('white')
    const [textColorPayslip, setTextColorPayslip] = useState('white')
    const [textColorDocuments, setTextColorDocuments] = useState('white')
    const [textColorMoodels, setTextColorMoodels] = useState('whitet')
    const [textColorHolidays, setTextColorHolidays] = useState('white')
    const [textColorRoster, setTextColorRoster] = useState('white')


    const inactiveRadius = '0px'
    const activeRadius = '30px'

    const activeColor = 'transparent';
    const inactiveColor = 'rgba(21, 39, 53,0.95)'
    const activeTextColor = inactiveColor
    const inactiveTextColor = 'white'

    useEffect(() => {
        setColorDashboard(activeComponent === 'Dashboard' ? activeColor : inactiveColor);
        setDashboardRadius(activeComponent === 'Dashboard' ? activeRadius : inactiveRadius);
        setTextColorDashboard(activeComponent === 'Dashboard' ? activeTextColor : inactiveTextColor);

        setColorProfile(activeComponent === 'Profile' ? activeColor : inactiveColor);
        setProfileRadius(activeComponent === 'Profile' ? activeRadius : inactiveRadius);
        setTextColorProfile(activeComponent === 'Profile' ? activeTextColor : inactiveTextColor);

        setColorPayslip(activeComponent === 'Payslip' ? activeColor : inactiveColor);
        setPayslipRadius(activeComponent === 'Payslip' ? activeRadius : inactiveRadius);
        setTextColorPayslip(activeComponent === 'Payslip' ? activeTextColor : inactiveTextColor);

        setColorDocuments(activeComponent === 'Documents' ? activeColor : inactiveColor);
        setDocumentsRadius(activeComponent === 'Documents' ? activeRadius : inactiveRadius);
        setTextColorDocuments(activeComponent === 'Documents' ? activeTextColor : inactiveTextColor);

        setColorMoodels(activeComponent === 'Moodels' ? activeColor : inactiveColor);
        setMoodelsRadius(activeComponent === 'Moodels' ? activeRadius : inactiveRadius);
        setTextColorMoodels(activeComponent === 'Moodels' ? activeTextColor : inactiveTextColor);

        setColorHolidays(activeComponent === 'Holidays' ? activeColor : inactiveColor);
        setHolidaysRadius(activeComponent === 'Holidays' ? activeRadius : inactiveRadius);
        setTextColorHolidays(activeComponent === 'Holidays' ? activeTextColor : inactiveTextColor);

        setColorRoster(activeComponent === 'Roster' ? activeColor : inactiveColor);
        setRosterRadius(activeComponent === 'Roster' ? activeRadius : inactiveRadius);
        setTextColorRoster(activeComponent === 'Roster' ? activeTextColor : inactiveTextColor);
    }, [activeComponent]);





    const renderComponent = () => {
        switch (activeComponent) {
            case 'Dashboard': 
            if (store.loggedInEmployee.department_id == 1){
                return <Budgets />
            }
            else{
                return <DashboardComponent />;
            }
            case 'Profile': {
                return <ProfileComponent />
            }
            case 'Payslip':
                return <PayslipComponent />
            case 'Documents':
                return <DocumentComponent />
            case 'Moodels':
                return <MoodelsComponent />
            case 'Holidays':
                return <HolidaysComponent />
            case 'Roster':
                if (store.loggedInEmployee.department_id == 3) {
                    return <RosterComponent />
                } else if(store.loggedInEmployee.department_id == 2)
                     { return  <CrewControllerComponent/> 
                } 
                    else {
                    return <ManagementComponent/>
                }
            default:
                return <DashboardComponent />

        }

    }
    console.log(store.loggedInEmployee)
    return (
        <>
            {store.loggedInEmployee == null ? 
            <div>
                <Lottie
                    options={defaultOptions}
                    height={400}
                    width={400}
                />
            </div> :
                <div className="text-center" style={{ backgroundImage: `url(${airplanebackground})`, backgroundSize: "100% 100%" }}>
                    <div className="row" id="board">
                        <div className="col-3" id="verticalNavbar" >
                            <div className="py-2" style={{ backgroundColor: `${inactiveColor}`, borderTopLeftRadius: "50px" }}>
                                <div className="py-3 mx-auto ProfileImageContainer">
                                    <p>Image</p>
                                </div>
                            </div>
                            <p className="infoUser" style={{ margin: "0", fontSize: "3vh", backgroundColor: `${inactiveColor}` }}>{store.loggedInEmployee.name}</p>
                            <div style={{ display: "inline-block", width: "100%", margin: "0" }}>
                                <div className="navbarComponent" style={{ color: `${textColorDashboard}`, backgroundColor: `${colorDashboard}`, borderBottomRightRadius: `${profileRadius}` }} onClick={() => setActiveComponent('Dashboard')}>
                                    <div className="mx-auto navbar-icon-text col-2" >
                                        {store.loggedInEmployee.department_id == 1 ?
                                        <FontAwesomeIcon icon={faFileInvoice} />:
                                        <FontAwesomeIcon icon={faHouse} />}
                                        <div className="mx-1"></div>
                                        {store.loggedInEmployee.department_id ==1 ? <p>Budgets</p> :
                                        <p>Dashboard</p>}
                                    </div>
                                </div>
                                <div className="navbarComponent" style={{ color: `${textColorProfile}`, backgroundColor: `${colorProfile}`, borderTopRightRadius: `${dashboardRadius}`, borderBottomRightRadius: `${roosterRadius}` }} onClick={() => setActiveComponent('Profile')}>
                                    <div className="mx-auto navbar-icon-text">
                                        <FontAwesomeIcon icon={faUser} />
                                        <div className="mx-1"></div>
                                        <p>Profile</p>
                                    </div>
                                </div>
                                <div className="navbarComponent" style={{ color: `${textColorRoster}`, backgroundColor: `${colorRoster}`, borderTopRightRadius: `${profileRadius}`, borderBottomRightRadius: `${payslipRadius}` }} onClick={() => setActiveComponent('Roster')}>
                                    <div className="mx-auto navbar-icon-text">
                                        {store.loggedInEmployee.departments_id == 1 ? 
                                        <FontAwesomeIcon icon={faBarsProgress} /> :
                                        <FontAwesomeIcon icon={faCalendarCheck} />}
                                        <div className="mx-1"></div>
                                        {store.loggedInEmployee.department_id ==3 ? <p>Roster</p> : 
                                        store.loggedInEmployee.department_id == 2 ? <p>Crew Control</p> : 
                                        <p>Management</p>}
                                    </div>
                                </div>
                                <div className="navbarComponent" style={{ color: `${textColorPayslip}`, backgroundColor: `${colorPayslip}`, borderTopRightRadius: `${roosterRadius}`, borderBottomRightRadius: `${documentsRadius}` }} onClick={() => setActiveComponent('Payslip')}>
                                    <div className="mx-auto navbar-icon-text">
                                        <FontAwesomeIcon icon={faMoneyBills} />
                                        <div className="mx-1"></div>
                                        <p>Payslip</p>
                                    </div>
                                </div>
                                <div className="navbarComponent" style={{ color: `${textColorDocuments}`, backgroundColor: `${colorDocuments}`, borderTopRightRadius: `${payslipRadius}`, borderBottomRightRadius: `${moodelsRadius}` }} onClick={() => setActiveComponent('Documents')}>
                                    <div className="mx-auto navbar-icon-text">
                                        <FontAwesomeIcon icon={faFile} />
                                        <div className="mx-1"></div>
                                        <p>Documents</p>
                                    </div>
                                </div>
                                <div className="navbarComponent" style={{ color: `${textColorMoodels}`, backgroundColor: `${colorMoodels}`, borderTopRightRadius: `${documentsRadius}`, borderBottomRightRadius: `${holidaysRadius}` }} onClick={() => setActiveComponent('Moodels')}>
                                    <div className="mx-auto navbar-icon-text">
                                        <FontAwesomeIcon icon={faUserGraduate} />
                                        <div className="mx-1"></div>
                                        <p>Moodels</p>
                                    </div>
                                </div>
                                <div className="navbarComponent" style={{ color: `${textColorHolidays}`, backgroundColor: `${colorHolidays}`, borderTopRightRadius: `${moodelsRadius}`, borderBottomRightRadius: `${inactiveRadius}` }} onClick={() => setActiveComponent('Holidays')}>
                                    <div className="mx-auto navbar-icon-text">
                                        <FontAwesomeIcon icon={faUmbrellaBeach} />
                                        <div className="mx-1"></div>
                                        <p>Holidays</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-8 component">
                            {renderComponent()}
                        </div>
                    </div>
                </div>
            }
        </>
    );

};

export default LandingPageWorker
