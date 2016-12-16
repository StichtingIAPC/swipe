export function startFetchingSuppliers() {
	return {	type: 'SUPPLIER_FETCH_START' };
}

export function doneFetchingSuppliers(suppliers) {
	return { type: 'SUPPLIER_FETCH_DONE', suppliers };
}

export function createSupplier(supplier) {
	return { type: 'SUPPLIER_CREATE', supplier };
}

export function updateSupplier(supplier) {
	return {	type: 'SUPPLIER_UPDATE', supplier };
}

export function deleteSupplier(supplier) {
	return { type: 'SUPPLIER_DELETE', supplier };
}
