import React, {useState, useContext, useEffect, useRef } from "react";
import { Context } from "../../../store/appContext";
import InputComponent from "../reusableComponents/InputComponent";

export const EditInflight = () => {
    const { store, actions } = useContext(Context);

    const [certificates, setCertificates] = useState({
        certificate1: null, 
        certificate2: '',
        certificate3: '',
        certificate4: '',
    })
    const [models, setModels] = useState([])
    const [airports, setAirports] = useState([])

    useEffect(()=> {
        const fetchModels = async() => {
            try {
                const modelsData = await actions.getModels()
                setModels(modelsData)
            } catch (error) {
                console.log(error)
            }
        }
        fetchModels()
        const fetchAirports = async() => {
            try{
                const allAirports = await actions.getAirports()
                setAirports(allAirports)
            } catch (error) {
                console.log(error)
            }
        }
        fetchAirports()
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
            <div style={{display: "flex"}}>
                <InputComponent label="License" placeholder={store.inflightEmployee.license} name="license"/>
                <InputComponent label="Passport" placeholder={store.inflightEmployee.passport} name="passport"/>
                {/* passport expiration */}
            </div>
            <div className="mb-3 mx-5" style={{display: "flex", justifyContent: "space-between"}}>
                <div className="col-5" style={{display: "flex"}}>
                    <span className="input-group-text" id="basic-addon1" style={{height: '4vh', fontSize: '1vw'}} >Certificate1</span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '4vh', fontSize: '1vw'}}
                                name = "model"
                                >
                                <option selected>{`${certificates.certificate1} (current)`}</option>
                                {
                                    models.map((model, index)=> (
                                        <option key={index} value={model.id}>{model.model}</option>
                                    ))
                                }
                            </select>
                </div>
                 <div style={{display: "flex", height: '4vh', fontSize: '1vw'}}>
                    <span className=" me-1 input-group-text" id="basic-addon1">Expiration date</span>
                    <input type='date' id='dateInput'></input>
                </div>           
            </div>
            <div className="mb-3 mx-5" style={{display: "flex", justifyContent: "space-between"}}>
                <div className="col-5" style={{display: "flex"}}>
                    <span className="input-group-text" id="basic-addon1" style={{height: '4vh', fontSize: '1vw'}} >Certificate2</span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '4vh', fontSize: '1vw'}}
                                name = "model"
                                >
                                <option selected>{`${certificates.certificate2} (current)`}</option>
                                {
                                    models.map((model, index)=> (
                                        <option key={index} value={model.id}>{model.model}</option>
                                    ))
                                }
                            </select>
                </div>
                 <div style={{display: "flex", height: '4vh', fontSize: '1vw'}}>
                    <span className=" me-1 input-group-text" id="basic-addon1">Expiration date</span>
                    <input type='date' id='dateInput'></input>
                </div>           
            </div>
            <div className="mb-3 mx-5" style={{display: "flex", justifyContent: "space-between"}}>
                <div className="col-5" style={{display: "flex"}}>
                    <span className="input-group-text" id="basic-addon1" style={{height: '4vh', fontSize: '1vw'}} >Certificate3</span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '4vh', fontSize: '1vw'}}
                                name = "model"
                                >
                                <option selected>{`${certificates.certificate3} (current)`}</option>
                                {
                                    models.map((model, index)=> (
                                        <option key={index} value={model.id}>{model.model}</option>
                                    ))
                                }
                            </select>
                </div>
                 <div style={{display: "flex", height: '4vh', fontSize: '1vw'}}>
                    <span className=" me-1 input-group-text" id="basic-addon1">Expiration date</span>
                    <input type='date' id='dateInput'></input>
                </div>           
            </div>
            <div className="mb-3 mx-5" style={{display: "flex", justifyContent: "space-between"}}>
                <div className="col-5" style={{display: "flex"}}>
                    <span className="input-group-text" id="basic-addon1" style={{height: '4vh', fontSize: '1vw'}} >Certificate4</span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '4vh', fontSize: '1vw'}}
                                name = "model"
                                >
                                <option selected>{`${certificates.certificate4} (current)`}</option>
                                {
                                    models.map((model, index)=> (
                                        <option key={index} value={model.id}>{model.model}</option>
                                    ))
                                }
                            </select>
                </div>
                 <div style={{display: "flex", height: '4vh', fontSize: '1vw'}}>
                    <span className=" me-1 input-group-text" id="basic-addon1">Expiration date</span>
                    <input type='date' id='dateInput'></input>
                </div>           
            </div>
            <div className="mb-3 mx-3" style={{display: "flex"}}>
                <span className="input-group-text" id="basic-addon1" style={{height: '4vh', fontSize: '1vw'}} >Home Base</span>
                            <select 
                                className="form-select form-select-lg mb-3" 
                                aria-label="Large select example" 
                                style={{height: '4vh', fontSize: '1vw'}}
                                name = "home_base"
                                >
                                <option selected>Select a Homebase</option>
                                {
                                    airports.map((airport, index)=> (
                                        <option key={index} value={airport.id}>{airport.airport}</option>
                                    ))
                                }
                            </select>
            </div>

        </div>
    )
}

export default EditInflight;