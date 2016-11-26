import auth from '../core/auth';

/**
 * Created by Matthias on 18/11/2016.
 */

export const ADD_SUPPLIER = 'ADD_SUPPLIER';
export function addSupplier(supplier) {
	return {
		type: ADD_SUPPLIER,
		supplier,
	}
}

export const REMOVE_SUPPLIER = 'REMOVE_SUPPLIER';
export function removeSupplier(id) {
	return {
		type: REMOVE_SUPPLIER,
		id,
	}
}

export const MARK_SUPPLIER_AS_UPDATING = 'MARK_SUPPLIER_AS_UPDATING';
export function fetchSupplier(id) {
	return {
		type: MARK_SUPPLIER_AS_UPDATING,
		id,
	}
}

export const UPDATE_SUPPLIER = 'UPDATE_SUPPLIER';
export function changeSupplier(supplier) {
	return {
		type: UPDATE_SUPPLIER,
		supplier,
	}
}

export const FETCH_SUPPLIERS = 'FETCH_SUPPLIERS';
export function fetchSuppliers() {
	return {
		type: FETCH_SUPPLIERS,
	}
}

export const INVALIDATE_SUPPLIERS = 'INVALIDATE_SUPPLIERS';
export function invalidateSuppliers(error) {
	return {
		type: INVALIDATE_SUPPLIERS,
		error: error,
	}
}

export const RECEIVE_SUPPLIERS = 'RECEIVE_SUPPLIERS';
export function receiveSuppliers(suppliers) {
	return {
		type: RECEIVE_SUPPLIERS,
		suppliers,
		date: new Date(),
	}
}

export function populateSuppliers() {
	return function(dispatch) {
		dispatch(fetchSuppliers());
		return auth.fetch('/supplier/', {method: 'GET'})
			.then(response => response.json())
			.then(json => dispatch(receiveSuppliers(json)))
			.catch(error => dispatch(invalidateSuppliers(error)))
	}
}

export function createSupplier(suppl) {
	return function(dispatch) {
		const supplier = {...suppl, search_url: suppl.searchUrl}; delete supplier.searchUrl;
		dispatch(invalidateSuppliers());
		auth.fetch('/supplier/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(supplier),
		})
			.then((request) => request.json())
			.then((json) => dispatch(addSupplier(json)))
			.catch(() => populateSuppliers())
	}
}

export function updateSupplier(suppl) {
	return function(dispatch) {
		const supplier = {...suppl, search_url: suppl.searchUrl}; delete supplier.searchUrl;
		dispatch(fetchSupplier(supplier.id));
		auth.fetch(`/supplier/${supplier.id}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(supplier),
		})
			.then((request) => request.json())
			.then((json) => dispatch(changeSupplier({...json, searchUrl: json.search_url })))
	}
}
