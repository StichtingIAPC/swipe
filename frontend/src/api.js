import fetch from "isomorphic-fetch";
import config from "./config";

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
	return Promise(
		accept => {
			if (TOKEN == null) {
				listeners.append(accept);
			} else {
				accept(TOKEN)
			}
		}
	)
}


export async function get(url, {headers = {}, ...rest} = {}) {
	const token = await getToken();
	const result = await fetch(
		config.baseurl + url,
		{
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${token}`,
				...headers,
			},
			...rest,
		}
	);
	if (result.ok) return result;
	throw result;
}

export async function post(url, object, {headers = {}, ...rest} = {}) {
	const token = await getToken();
	const result = await fetch(
		config.baseurl + url,
		{
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${token}`,
				...headers,
			},
			body: JSON.stringify(object),
			...rest,
		}
	);
	if (result.ok) return result;
	throw result;
}

export async function put(url, object, {headers = {}, ...rest} = {}) {
	const token = await getToken();
	const result = await fetch(
		config.baseurl + url,
		{
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${token}`,
				...headers,
			},
			body: JSON.stringify(object),
			...rest,
		}
	);
	if (result.ok) return result;
	throw result;
}

/* named `del` as `delete` is a keyword in js */
export async function del(url, object, {headers = {}, ...rest} = {}) {
	const token = await getToken();
	const result = await fetch(
		config.baseurl + url,
		{
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${token}`,
				...headers,
			},
			body: JSON.stringify(object),
			...rest,
		}
	);
	if (result.ok) return result;
	throw result;
}
