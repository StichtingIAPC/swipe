export function startFetchingSuppliers({redirectTo} = {}) {
	return { type: 'SUPPLIER_FETCH_START', redirectTo };
}

export function doneFetchingSuppliers(suppliers) {
	return { type: 'SUPPLIER_FETCH_DONE', suppliers };
}

export function createSupplier(supplier) {
	return { type: 'SUPPLIER_CREATE', supplier };
}

export function updateSupplier(supplier) {
	return { type: 'SUPPLIER_UPDATE', supplier };
}

export function deleteSupplier(supplier) {
	return { type: 'SUPPLIER_DELETE', supplier };
}

export function supplierFetchError(error) {
	return { type: 'SUPPLIER_FETCH_ERROR', error };
}

export function supplierInputError(error) {
	return { type: 'SUPPLIER_INPUT_ERROR', error };
}

export {
	startFetchingSuppliers as suppliers
}
