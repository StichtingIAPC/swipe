import fetch from "isomorphic-fetch";
import config from "./config";
import {getState} from "./app";

export function get(url, {headers = {}, ...rest}) {
	return fetch(
		config.baseurl + url,
		{
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${getState().auth.token}`,
				...headers,
			},
			...rest,
		}
	).then((response) => response.ok ? response : Promise.reject(response))
}

export function post(url, object, {headers = {}, ...rest}) {
	return fetch(
		config.baseurl + url,
		{
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${getState().auth.token}`,
				...headers,
			},
			body: JSON.stringify(object),
			...rest,
		}
	).then((response) => response.ok ? response : Promise.reject(response))
}

export function patch(url, object, {headers = {}, ...rest}) {
	return fetch(
		config.baseurl + url,
		{
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Token ${getState().auth.token}`,
			},
			body: JSON.stringify(object),
		}
	).then((response) => response.ok ? response : Promise.reject(response));
}