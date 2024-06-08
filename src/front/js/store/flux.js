const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			inflightEmployee: null,
			loggedInEmployee: null,
			roles: null,
			departments: null, 
			message: null,
			budgets: [],
			pendingBudgets: true,
			acceptedBudgets: true,
			singleBudget: null
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},
			checkToken: () => {

			},
			getBudgets: (params) =>{
				const authToken = localStorage.getItem("jwt-token");
				let url = process.env.BACKEND_URL + '/api/budgets';

				if (params) {
					const urlParams = Object.keys(params).map(key => `${key}=${params[key]}`).join('&');
					url += `?${urlParams}`
				}

				fetch(url, {
						headers: {
							Authorization: `Bearer ${authToken}`
						}
				})
				.then((response)=> response.json())
				.then((data) => {setStore({budgets: data})})
				.catch((err) => err)
			},
			getSingleBudget: (id) => {
				const authToken = localStorage.getItem("jwt-token");
				let url = process.env.BACKEND_URL + `/api/budgets?id=${id}`;
				return new Promise((resolve, reject) =>{
					fetch(url, {
							headers: {
								Authorization: `Bearer ${authToken}`
							}
					})
					.then((response)=> response.json())
					.then((data) => {setStore({singleBudget: data[0]})
									resolve()})
					.catch((err) => reject(err))
				})
			},
			setSingleBudget: (value) => {
				setStore({singleBudget: value})
			},
			setPendingBudgets: (value) => {
                setStore({ pendingBudgets: value });
            },
            setAcceptedBudgets: (value) => {
                setStore({ acceptedBudgets: value });
            },
			getMessage: async () => {
				try {
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
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
			getConfigurations: async (modelId) => {
				try {
					const resp = await fetch(`${process.env.BACKEND_URL}/api/configurations?model=${modelId}`, {
						method: 'GET',
						headers: {
							'Content-Type': 'application/json'
						}
					});
					const data = await resp.json();
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
					const resp = await fetch(`${process.env.BACKEND_URL}/api/fleet?model_id=${modelId}`, {
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
			getAllFleet: async () => {
				try {
					const resp = await fetch(`${process.env.BACKEND_URL}/api/fleet`, {
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
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + "/api/countries")
					const data = await resp.json()
					return data;
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
					return data
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
			getNationalityById: async (nationality_id) => {
				try {
					const resp = await fetch(process.env.BACKEND_URL + `/api/nationalities?id=${nationality_id}`)
					const data = await resp.json()
					return data[0].nationality
				} catch (error) {
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
			getAirportDataById: async (airport_id) => {
				try{
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/airports?id=${airport_id}`
					)
					const data = await resp.json()
					const airport = data[0]
					return airport
				} catch(error) {
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
			getAirportsByCountry: async(country_id) => {
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/airports?country_id=${country_id}`
					)
					const data = await resp.json()
					console.log(data)
					return data
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
					role = data.role
					console.log(role)
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
					console.log(error)
				}
			},
			getEmployeeById: async (employee_id) => {
				let employee = []
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/filterEmployees?id=${employee_id}`, {
							headers: {
								Authorization: `Bearer ${authToken}`
							}})
					const data = await resp.json()
					employee = data[0];
					console.log(employee)
					return employee
				} catch (error) {
					console.log(error)
				}
			},
			getEmployeesByRol: async (role_id) => {
				let employeesByRol = []
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/filterEmployees?role_id=${role_id}`, {
							headers: {
								Authorization: `Bearer ${authToken}`
							}})
					const data = await resp.json()
					employeesByRol = data;
					console.log(employeesByRol)
					return employeesByRol;
				} catch (error) {

				}
			},
			getEmployeesByDepartment: async (department_id) => {
				let employeesByDepartment = []
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/filterEmployees?department_id=${department_id}`, {
							headers: {
								Authorization: `Bearer ${authToken}`
							}})
					const data = await resp.json()
					employeesByDepartment = data;
					console.log(employeesByDepartment)
					return employeesByDepartment;
				} catch (error) {
					console.log(error)
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
						setStore({ loggedInEmployee: employee });
						setTimeout(() => {
							
						}, 5000);
						return employee
					} catch (error) {

					}
				}
			},
			getEmployeeRoster: async(employee_id) => {
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/roster?employee_id=${employee_id}`, {
							headers: {
								Authorization: `Bearer ${authToken}`
							}
						}
						
					)
					const data = await resp.json()
					console.log(data)
					return data
				} catch (error) {
					console.log(error)
				}
			},
			getDutiesById: async (duty_id) => {
				let duty
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/duties?id=${duty_id}`, {
							headers: {
								Authorization: `Bearer ${authToken}`
							}})
					const data = await resp.json()
					duty = data[0].duty; 
					return duty; 
				} catch (error) {
					console.log(error)
				}
			},
			getFlightById: async (flight_id) => {
				let flight
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(
						process.env.BACKEND_URL + `/api/flights?id=${flight_id}`, {
							headers: {
								Authorization: `Bearer ${authToken}`
							}})
					const data = await resp.json()
					flight = data[0]; 
					return flight 
				} catch (error) {
					console.log(error)
				}
			},
			logout: async () => {
				const authToken = localStorage.getItem("jwt-token");
				try {
					const resp = await fetch(process.env.BACKEND_URL + '/api/logout', {
						headers: {
							Authorization: `Bearer ${authToken}`
						}
					})
				} catch (error) {
					console.log(error)
				}
				localStorage.removeItem('jwt-token');
				setStore({loggedInEmployee: null})
				setStore({inflightEmployee: null})
				setStore({roles: null})
				setStore({departments: null})
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
