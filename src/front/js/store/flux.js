const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			inflightEmployee: null,
			loggedInEmployee: null,
			roles: null,
			departments: null, 
			message: null,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},
			checkToken: () => {

			},
			getMessage: async () => {
				try {
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				} catch (error) {
					console.log("Error loading message from backend", error)
				}
			}, 
			getModels: async () => {
				let allModels = [];
				try{ 
					const resp = await fetch(
						process.env.BACKEND_URL + "/api/models")
					const data = await resp.json()
 					allModels = data; 
 					console.log(allModels)
					return allModels;   
				} catch(error) {
					console.log(error)
				}
			},
			getModelById: async(model_id) => {
				try{
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/models?id=${model_id}`
					)
					const data = await resp.json()
					const model = data[0].model
					return model
				} catch(error) {
					console.log(error)
				}
			},
			getConfigurations: async (modelyId) => {
				try {
					const resp = await fetch(`${process.env.BACKEND_URL}api/configurations?model_id=${modelId}`, {
						method: 'GET',
						headers: {
							'Content-Type': 'application/json'
						}
					});
					const data = await resp.json();
					console.log(data);
					return data;
				} catch(error) {
					console.log(error);
				}
			},
			getInflight: async (employee_id) => {
				let inflight; 
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(`${process.env.BACKEND_URL}/api/inflight?employee_id=${employee_id}`, {
						method: 'GET', 
						headers: {
							'Content-Type': 'application/json',
							Authorization: `Bearer ${authToken}`
						}

					})
					const data = await resp.json()
					inflight = data
					setStore({inflightEmployee: inflight})
					return inflight; 
				} catch (error) {
					console.log(error)
				}
			},
			getFleet: async (modelId) => {
				try {
					const resp = await fetch(`${process.env.BACKEND_URL}api/fleet?model_id=${modelId}`, {
						method: 'GET',
						headers: {
							'Content-Type': 'application/json'
						}
					});
					const data = await resp.json();
					console.log(data);
					return data;
				} catch(error) {
					console.log(error);
				}
			},
			getCountries: async () => {
				let allCountries = [];
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + "/api/countries")
					const data = await resp.json()
					allCountries = data;
					console.log(allCountries)
					return allCountries;
				} catch (error) {
					console.log(error)
				}
			},
			getCountryById: async (country_id) => {
				try{
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/countries?id=${country_id}`
					)
					const data = await resp.json()
					const country = data[0].country
					return country
				} catch(error) {
					console.log(error)
				}

			},
			getAirports: async() => {
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + "/api/airports"
					)
					const data = await resp.json()
					const airports = data
					return airports
				} catch (error) {
					console.log(error)
				}
			},
			getAirportById: async (airport_id) => {
				try{
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/airports?id=${airport_id}`
					)
					const data = await resp.json()
					const airport = data[0].airport
					return airport
				} catch(error) {
					console.log(error)
				}
			},
			getStates: async (countryId) => {
				try {
					const resp = await fetch(`${process.env.BACKEND_URL}/api/states?country_id=${countryId}`, {
						method: 'GET',
						headers: {
							'Content-Type': 'application/json'
						}

					});
					const data = await resp.json();
					return data;
				} catch (error) {
					console.log(error);
				}
			},
			getStateById: async (stateId) => {
				let state
				try {
					const resp = await fetch(process.env.BACKEND_URL + `/api/states?id=${stateId}`)
					const data = await resp.json()
					state = data[0].state
					return state; 
				} catch (error) {
					console.log(error)
				}
			},
			getNationalities: async () => {
				let allNationalities
				try {
					const resp = await fetch(process.env.BACKEND_URL + `/api/nationalities`)
					const data = await resp.json()
					allNationalities = data
					return allNationalities
				} catch (error) {
					console.log(error)
					
				}
			}, 
			getRoles: async () => {
				let allRoles = [];
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + "/api/roles" , {headers: {
							Authorization: `Bearer ${authToken}`
						}}
					)
					const data = await resp.json()
					allRoles = data;
					/* console.log(allRoles) */
					return allRoles;
				} catch (error) {
					console.log(error)
				}
			},
			getRoleById: async(role_id) => {
				let role
				const authToken = localStorage.getItem("jwt-token");
				try{
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/roles?id=${role_id}`, {headers: {
							Authorization: `Bearer ${authToken}`
						}}

					)
					const data = await resp.json()
					console.log(JSON.stringify(data))
					role = data[0].role
					return role; 
				} catch(error) {
					console.log(error)
				}
			},
			getDepartments: async () => {
				let allDepartments = []
				const authToken = localStorage.getItem("jwt-token");
				console.log(authToken)
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + "/api/departments", {
							headers: {
								Authorization: `Bearer ${authToken}`
							}})
					const data = await resp.json()
					allDepartments = data;
					/* console.log(allDepartments) */
					return allDepartments;
				} catch (error) {
					console.log(error)
				}
			},
			getDepartmentById: async (department_id) => {
				let department
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/departments?id=${department_id}`, {
							headers: {
								Authorization: `Bearer ${authToken}`
							}})
					const data = await resp.json()
					department = data[0].department; 
					return department; 
				} catch (error) {
					console.log(error)
				}
			},
			getEmployeesByCrewId: async () => {
				let allEmployees = []
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + "/api/crew_id", {
							headers: {
								Authorization: `Bearer ${authToken}`
							}})
					const data = await resp.json()
					allEmployees = data;
					console.log(allEmployees)
					return allEmployees;
				} catch (error) {

				}
			},
			getEmployee: async () => {
				let employee = {}
				const authToken = localStorage.getItem("jwt-token");
				if (authToken != null) {
					try {
						const resp = await fetch(
							process.env.BACKEND_URL + `/api/employee`, {
							headers: {
								Authorization: `Bearer ${authToken}`
							}
						}
						)
						const data = await resp.json()
						employee = data
						console.log('employee')
						setTimeout(() => {
							setStore({ loggedInEmployee: employee });
						}, 5000);
						return employee
					} catch (error) {

					}
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			}
		}
	};
};

export default getState;
