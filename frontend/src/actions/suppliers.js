import request from '../core/request';

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

export const FETCH_SUPPLIER = 'FETCH_SUPPLIER';
export function fetchSupplier(id) {
	return {
		type: FETCH_SUPPLIER,
		id,
	}
}

export const PUT_SUPPLIER = 'PUT_SUPPLIER';
export function putSupplier(supplier) {
	return {
		typs: PUT_SUPPLIER,
		supplier,
	}
}

export const UPDATE_SUPPLIER = 'UPDATE_SUPPLIER';
export function updateSupplier(supplier) {
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
		return request.get('/supplier/all/')
			.then(response => response.json())
			.then(json => dispatch(receiveSuppliers(json)))
			.catch(error => dispatch(invalidateSuppliers(error)))
	}
}
