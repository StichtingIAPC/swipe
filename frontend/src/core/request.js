import fetch from 'isomorphic-fetch';
import auth from './auth';

function validateResponse(response) {
	if (response.status == 200) {
		return response;
	}
	return Promise.reject(response.json());
}

function authenticatedRequest(addr, {headers, ...options}, token) {
	if (headers['Authorization'])
		return Promise.reject(new Error("You may not set any authorization headers"));

	headers = {
		...headers,
		Authorization: `Token ${token}`,
	};
	return new Promise(
		(accept, reject) => (
			fetch(window.location.origin + addr, {headers, ...options})
				.then(validateResponse)
				.then(response => response.json())
				.catch(reject)
		)
	)
}

export function request(addr, options) {
	if (auth.isAuthenticated()) {
		return new Promise((accept, reject) => {
			authenticatedRequest(addr, options, auth.getToken())
		})
	} else {
		return Promise.reject(new Error("You are not authenticated. Please fix"));
	}
}

function authRequest(username, password) {
	return fetch(
		window.location.origin + '/auth/login/', {
			body: {
				username,
				password,
			},
		})
		.then(validateResponse)
		.then()
}

function requestAuth() {
	return new Promise((accept, reject) => {

	})
}

['get', 'head', 'post', 'put', 'delete', 'options', 'trace', 'connect', 'patch'].forEach(
	(mehtod) => (
		request[mehtod] = (address, {...rest}) => (
			request(address, {...rest, method: mehtod.toUpperCase()})
		)
	)
);

export default request;
