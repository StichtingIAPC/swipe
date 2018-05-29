import api from '../../api';

export const ENDPOINT = '/crm/customers/';

export function getAll() {
	return api('GET', ENDPOINT);
}
