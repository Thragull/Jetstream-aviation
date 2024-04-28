import { Context } from "../../../store/appContext";
import React, { useContext, useState, useEffect } from "react";
import InfoComponent from "../reusableComponents/InfoComponent";
import EditInflight from "./EditInflight";


export const InflightProfile = (props) => {
	const { store, actions } = useContext(Context);
    const [airport, setAirport] = useState(null)
    const [certificates, setCertificates] = useState({
        certificate1: null, 
        certificate2: '',
        certificate3: '',
        certificate4: '',
    })
   

    const [editInflight, setEditInflight] = useState(false)

    useEffect(()=> {
        const fetchAirport = async() => {
            try{
                const airportData = await actions.getAirportById(store.inflightEmployee.home_base)
                setAirport(airportData)

            } catch (error) {
                console.log(error)
            }
        }
        const fetchModel = async (modelId, certificate) => {
            try {
                const modelData = await actions.getModelById(modelId);
                setCertificates(prevState => ({
                    ...prevState,
                    [certificate]: modelData
                }));
            } catch (error) {
                console.log(error);
            }
        };
        fetchAirport()
        if(store.inflightEmployee.certificate_id != null) {
            fetchModel(store.inflightEmployee.certificate_id, "certificate1")
        }
        if(store.inflightEmployee.certificate_id2 != null) {
            fetchModel(store.inflightEmployee.certificate_id2, "certificate2")
        }
        if(store.inflightEmployee.certificate_id3 != null) {
            fetchModel(store.inflightEmployee.certificate_id3, "certificate3")
        }
        if(store.inflightEmployee.certificate_id4 != null) {
            fetchModel(store.inflightEmployee.certificate_id4, "certificate4")
        }
    }, [])

	return (
        <div>
            {editInflight ? <EditInflight/> : 
             <div>
                <div style={{display: "flex"}}>
                    <InfoComponent label="License" name={store.inflightEmployee.license}/>
                    <InfoComponent label="Passport" name={store.inflightEmployee.passport} />
                    <InfoComponent label="Pass exporation" name={store.inflightEmployee.pass_expiration}/>
                </div>
                <div style={{display: "flex"}}>
                    <InfoComponent label="Certificate" name={certificates.certificate1 ? certificates.certificate1 : ''}/>
                    <InfoComponent label="Certificate expiration" name={store.inflightEmployee.cert_expiration}/>
                </div>
                {store.inflightEmployee.certificate_id2 ?
                        <div style={{display: "flex"}}>
                            <InfoComponent label="Certificate" name={certificates.certificate2}/>
                            <InfoComponent label="Certificate expiration" name={store.inflightEmployee.cert_expiration2}/>
                        </div>
                        : <></>
                 }
                {store.inflightEmployee.certificate_id3 ?
                        <div style={{display: "flex"}}>
                            <InfoComponent label="Certificate" name={certificates.certificate3}/>
                            <InfoComponent label="Certificate expiration" name={store.inflightEmployee.cert_expiration3}/>
                        </div>
                        : <></>
                 }
                {store.inflightEmployee.certificate_id4 ?
                        <div style={{display: "flex"}}>
                            <InfoComponent label="Certificate" name={certificates.certificate4}/>
                            <InfoComponent label="Certificate expiration" name={store.inflightEmployee.cert_expiration4}/>
                        </div>
                        : <></>
                 }
                <div style={{display: "flex"}}>
                    <InfoComponent label="Home Base" name = {airport ? airport : ''}/>
                </div>
                <div style={{display: "flex"}}>
                    <InfoComponent label="Roster Asigned"/>
                </div>
                <div style={{display: "flex"}}>
                    <InfoComponent label="Monthly BH" name={store.inflightEmployee.monthly_BH}/>
                    <InfoComponent label="Yearly BH" name={store.inflightEmployee.yearly_BH}/>
                    <InfoComponent label="Total BH" name={store.inflightEmployee.total_BH}/>
                </div>
                <div style={{display: "flex"}}>
                    <InfoComponent label="Monthly DH" name={store.inflightEmployee.monthly_DH} />
                    <InfoComponent label="Yearly DH" name={store.inflightEmployee.yearly_DH}/>
                    <InfoComponent label="Total DH" name={store.inflightEmployee.yearly_DH}/>
                </div>
            </div>}
            <button type="button" className="btn btn-success" onClick={()=> {setEditInflight(!editInflight)}}>{editInflight ? "Save" : "Edit"}</button>
        </div>
        
	);
};
export default InflightProfile; 
