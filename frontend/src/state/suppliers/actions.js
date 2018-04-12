export const SET_VALIDATIONS = 'suppliers/validations';

export const setValidations = validations => ({ type: SET_VALIDATIONS,
	validations });

export function fetchAllSuppliers(redirectTo) {
	return {
		type: 'suppliers/FETCH_ALL',
		redirectTo,
	};
}

export function fetchAllSuppliersDone(suppliers) {
	return {
		type: 'suppliers/FETCH_ALL_DONE',
		suppliers,
	};
}

export function fetchAllSuppliersFailed(reason) {
	return {
		type: 'suppliers/FETCH_ALL_FAILED',
		reason,
	};
}

export function fetchAllSuppliersFinally() {
	return {
		type: 'suppliers/FETCH_ALL_FINALLY',
	};
}

export function fetchSupplier(id) {
	return {
		type: 'suppliers/FETCH',
		id,
	};
}

export function fetchSupplierDone(supplier) {
	return {
		type: 'suppliers/FETCH_DONE',
		supplier,
	};
}

export function fetchSupplierFailed(id, reason) {
	return {
		type: 'suppliers/FETCH_FAILED',
		id,
		reason,
	};
}

export function fetchSupplierFinally() {
	return { type: 'suppliers/FETCH_FINALLY' };
}

export function createSupplier(supplier) {
	return {
		type: 'suppliers/CREATE',
		supplier,
	};
}

export function createSupplierDone(supplier) {
	return {
		type: 'suppliers/CREATE_DONE',
		supplier,
	};
}

export function createSupplierFailed(supplier, reason) {
	return {
		type: 'suppliers/CREATE_FAILED',
		supplier,
		reason,
	};
}

export function createSupplierFinally() {
	return { type: 'suppliers/CREATE_FINALLY' };
}

export function updateSupplier(supplier) {
	return {
		type: 'suppliers/UPDATE',
		supplier,
	};
}

export function updateSupplierDone(supplier) {
	return {
		type: 'suppliers/UPDATE_DONE',
		supplier,
	};
}

export function updateSupplierFailed(supplier, reason) {
	return {
		type: 'suppliers/UPDATE_FAILED',
		supplier,
		reason,
	};
}

export function updateSupplierFinally() {
	return {
		type: 'suppliers/UPDATE_FINALLY',
	};
}

export function deleteSupplier(id) {
	return {
		type: 'suppliers/DELETE',
		id,
	};
}

export function deleteSupplierDone(id) {
	return {
		type: 'suppliers/DELETE_DONE',
		id,
	};
}

export function deleteSupplierFailed(id, reason) {
	return {
		type: 'suppliers/DELETE_FAILED',
		id,
		reason,
	};
}

export function deleteSupplierFinally() {
	return { type: 'suppliers/DELETE_FINALLY' };
}

export function setSupplierField(field, value) {
	return {
		type: 'suppliers/SET_FIELD',
		field,
		value,
	};
}

export function newSupplier() {
	return {
		type: 'suppliers/NEW_SUPPLIER',
	};
}

export default fetchAllSuppliers;
export {
	fetchAllSuppliers as suppliers
};
