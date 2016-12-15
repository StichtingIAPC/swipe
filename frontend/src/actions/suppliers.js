// TODO: rewrite from Thunk to sagas

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
		error,
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
	return {
		type: 'SUPPLIER_POPULATE_SUPPLIERS',
	}
}

export function createSupplier(suppl) {
	return {
		type: 'SUPPLIER_CREATE_SUPPLIER',
		suppl,
	}
}

export function updateSupplier(suppl) {
	return {
		type: 'SUPPLIER_UPDATE_SUPPLIER',
		suppl,
	}
}
