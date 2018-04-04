/* eslint-disable no-undefined */
import fetch from 'isomorphic-fetch';
import config from './config';

let TOKEN = null;
let TOKEN_REFRESH_LOCK = null;
let refresh_listeners = [];
let listeners = [];

export function setToken(token) {
	TOKEN = token;
	for (const listener of listeners) {
		listener(token);
	}

	listeners = [];
}

export function __getTokenDangerous() {
	return TOKEN;
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

export async function refreshAuthToken(token) {
	if (TOKEN_REFRESH_LOCK) {
		await new Promise((resolve, reject) => {
			refresh_listeners.push(resolve);
		});
		return;
	}

	TOKEN_REFRESH_LOCK = true;

	// eslint-disable-next-line no-use-before-define
	const response = await post('/auth/token-refresh/', { token }, { token });

	if (response.ok) {
		setToken((await response.json()).token);
	}

	TOKEN_REFRESH_LOCK = false;
	refresh_listeners.forEach(resolver => resolver());
}

async function request(method, url, { headers = {}, token = false, ...rest } = {}, object) {
	const authToken = token ? token : await getToken();
	const result = await fetch(
		config.backendUrl + url,
		{
			method,
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `JWT ${authToken}`,
				...headers,
			},
			body: object ? JSON.stringify(object) : undefined,
			...rest,
		}
	);

	if (result.ok) {
		return result;
	}

	if (result.status === 400) {
		const data = await result.json();

		if (data.non_field_errors && data.non_field_errors.indexOf('Signature has expired.') > -1) {
			await refreshAuthToken(token);
			return request(method, url, {
				headers,
				token,
				...rest,
			}, object);
		}
		throw data;
	}
	throw await result.json();
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
