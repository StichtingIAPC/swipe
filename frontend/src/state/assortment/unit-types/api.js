import api from '../../../api';

export const ENDPOINT = '/assortment/unittypes/';

export function getAll() {
	return api('GET', ENDPOINT);
}

export function get(id) {
	return api('GET', `${ENDPOINT}${id}`);
}

export function post(data) {
	return api('POST', ENDPOINT, data);
}

export function put(id, data) {
	return api('PUT', `${ENDPOINT}${id}`, data);
}

export function del(id) {
	return api('DELETE', `${ENDPOINT}${id}`);
}
