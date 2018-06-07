/* eslint-disable no-undefined */
import config from './config';

let TOKEN = null;
let listeners = [];

export function setToken(token) {
	TOKEN = token;
	for (const listener of listeners) {
		listener(token);
	}

	listeners = [];
}

export function getToken() {
	return new Promise(
		accept => {
			if (TOKEN === null) {
				listeners.push(accept);
			} else {
				accept(TOKEN);
			}
		}
	);
}

export function __unsafeGetToken() {
	return TOKEN;
}

async function request(method, url, object) {
	const token = await getToken();
	const result = await fetch(
		config.backendUrl + url,
		{
			method,
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${token}`,
			},
			body: object ? JSON.stringify(object) : undefined,
		}
	);

	if (result.ok) {
		return result;
	}
	throw result.json();
}


export default function api(method, endpoint, body) {
	return request(method, endpoint, body);
}
