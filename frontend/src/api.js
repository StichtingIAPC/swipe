/* eslint-disable no-undefined */
import fetch from 'isomorphic-fetch';
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
				listeners.append(accept);
			} else {
				accept(TOKEN);
			}
		}
	);
}

async function request(method, url, { headers = {}, ...rest } = {}, object) {
	const token = await getToken();
	const result = await fetch(
		config.backendUrl + url,
		{
			method,
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${token}`,
				...headers,
			},
			body: object ? JSON.stringify(object) : undefined,
			...rest,
		}
	);

	if (result.ok) {
		return result;
	}
	throw result;
}

export function get(url, info) {
	return request('GET', url, info);
}

export function post(url, object, info) {
	return request('POST', url, info, object);
}

export function put(url, object, info) {
	return request('PUT', url, info, object);
}

/* named `del` as `delete` is a keyword in js */
export function del(url, object, info) {
	return request('DELETE', url, info, object);
}

export function patch(url, object, info) {
	return request('PATCH', url, info, object);
}
