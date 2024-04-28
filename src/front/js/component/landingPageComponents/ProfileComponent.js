import React, { useContext, useEffect, useState } from "react";
import { Context } from "../../store/appContext";
import InfoComponent from "./reusableComponents/InfoComponent";
import EditProfile from "./ProfileComponents/EditProfile";
import "./ProfileComponents/profile_component.css";
import InflightProfile from "./ProfileComponents/InflightProfile";


export const ProfileComponent = () => {
	const { store, actions } = useContext(Context);

    const [editProfile, setEditProfile] = useState(false)
    const [seeinflight, setSeeInflight] = useState(false)
    const activeTabColor = 'rgba(21, 39, 53,0.95)'
    const inactiveTabColor = 'rgba(255,255,255,0.5)'
    const activeProfileColor = seeinflight ? 'rgba(255,255,255,0.5)' : activeTabColor
    const activeInflightColor = seeinflight ? activeTabColor : inactiveTabColor
    const activeTabProfileTextColor = seeinflight ?  'rgba(21, 39, 53,0.95)' : 'white'
    const activeTabInflightTextColor = seeinflight ? 'white' : 'rgba(21, 39, 53,0.95)'
    const [department, setDepartment] = useState(null)
    const [role, setRole] = useState(null)
    const [country, setCountry] = useState(null)
    const [state, setState] = useState(null)


    useEffect(() => {
        const fetchDepartment = async () => {
            console.log('departmemts')
            try {
                const departmentData = await actions.getDepartmentById(store.loggedInEmployee.department);
                setDepartment(departmentData);
            } catch (error) {
                console.error('Error fetching department:', error);
            }
        };
        const fetchRole = async() => {
            try{
                const roleData = await actions.getRoleById(store.loggedInEmployee.role);
                setRole(roleData);
                
            } catch (error) {
                console.error('Error fetching department:', error);
            }
        }
        const fetchCountry = async() => {
            try{
                const countryData = await actions.getCountryById(store.loggedInEmployee.country)
                setCountry(countryData)

            } catch (error) {
                console.log(error)
            }
        }
        const fetchState = async ()=>{
            try {
                const stateData = await actions.getStateById(store.loggedInEmployee.state)
                setState(stateData)
            } catch (error) {
                console.log(error)
            }
        }

            const fetchInflight = async () => {
                try{
                     await actions.getInflight(store.loggedInEmployee.id)
                    
                }
                catch(error) {
                    error
                }
            }
            fetchInflight();
 
    
        fetchDepartment();
        fetchRole();
        fetchCountry();
        fetchState();
   


    }, []);
    
    

    const Divider = ({ width, height, color, margin }) => {
        const dividerStyle = {
          width:   "100%",
          height:  "2px",
          backgroundColor: "rgba(255,255,255,0.2)",
          margin: "0"
        };
      
        return <div style={dividerStyle}></div>;
      };

	return (
       editProfile ?   
            <EditProfile saveChangesFunction={()=> setEditProfile(false)}/>    
                 :  
        <div>
            <h1 className="mb-5">Profile</h1>
                <div className="row" style={{justifyContent: "space-between"}}>
                <div className="tab col-6" style={{background: `${activeProfileColor}`, color: `${activeTabProfileTextColor}`  }} onClick={()=> setSeeInflight(false)}>
                    Profile
                </div>
                <div onClick={()=> setSeeInflight(true)}  className="tab col-6" style={{background: `${activeInflightColor}`, color: `${activeTabInflightTextColor}`  }} >
                    Inflight
                </div>
            </div>
            {seeinflight ? <InflightProfile/> : 
                <div>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Name" name={store.loggedInEmployee.name}/>
                        <InfoComponent label="Sirname" name={store.loggedInEmployee.surname}/>
                        { store.loggedInEmployee.birthday != null ? 
                        <InfoComponent label="Birthday" name={store.loggedInEmployee.birthday}/> : <></>}
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Email" name={store.loggedInEmployee.email}/>
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Department" name={department ? department : ''}/>
                        <InfoComponent label="Role" name={role ? role : ''}/>
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Nationality" name={store.loggedInEmployee.nationality ? store.loggedInEmployee.nationality : '' }/>
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Adress" name={store.loggedInEmployee.address ? store.loggedInEmployee.address : '' }/>
                        <InfoComponent label="ZipCode" name={store.loggedInEmployee.zipcode ? store.loggedInEmployee.zipcode : '' }/>
                    </div>
                    <Divider/>
                    <div style={{display: "flex"}}>
                        <InfoComponent label="Country" name={country ? country : ''}/>
                        <InfoComponent label="State" name={state ? state : ''}/>
                        <InfoComponent label="City" name={store.loggedInEmployee.city ? store.loggedInEmployee.city : '' }/>
                    </div>
                    <Divider/> 
                    <div className="my-5">
                        <button onClick={()=> setEditProfile(true)} type="button" className="btn btn-info">Edit Profile</button>
                    </div> 
                </div> 
}
        </div>
	);
};

export default ProfileComponent; 