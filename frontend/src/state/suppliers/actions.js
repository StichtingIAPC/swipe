export const SUPPLIERS_FETCH_ALL_START = 'suppliers/fetchAll/start';
export const SUPPLIERS_FETCH_ALL_SUCCESS = 'suppliers/fetchAll/success';
export const SUPPLIERS_FETCH_ALL_FAIL = 'suppliers/fetchAll/fail';
export const SUPPLIERS_FETCH_ALL_FINALLY = 'suppliers/fetchAll/finally';

export const SUPPLIERS_FETCH_START = 'suppliers/fetch/start';
export const SUPPLIERS_FETCH_SUCCESS = 'suppliers/fetch/success';
export const SUPPLIERS_FETCH_FAIL = 'suppliers/fetch/fail';
export const SUPPLIERS_FETCH_FINALLY = 'suppliers/fetch/finally';

export const SUPPLIERS_CREATE_START = 'suppliers/create/start';
export const SUPPLIERS_CREATE_SUCCESS = 'suppliers/create/success';
export const SUPPLIERS_CREATE_FAIL = 'suppliers/create/fail';
export const SUPPLIERS_CREATE_FINALLY = 'suppliers/create/finally';

export const SUPPLIERS_UPDATE_START = 'suppliers/update/start';
export const SUPPLIERS_UPDATE_SUCCESS = 'suppliers/update/success';
export const SUPPLIERS_UPDATE_FAIL = 'suppliers/update/fail';
export const SUPPLIERS_UPDATE_FINALLY = 'suppliers/update/finally';

export const SUPPLIERS_DELETE_START = 'suppliers/delete/start';
export const SUPPLIERS_DELETE_SUCCESS = 'suppliers/delete/success';
export const SUPPLIERS_DELETE_FAIL = 'suppliers/delete/fail';
export const SUPPLIERS_DELETE_FINALLY = 'suppliers/delete/finally';

export const SUPPLIERS_SET_FIELD = 'suppliers/setField';
export const SUPPLIERS_NEW_SUPPLIER = 'suppliers/newSupplier';

export const fetchAllSuppliers = redirectTo => ({
	type: SUPPLIERS_FETCH_ALL_START,
	redirectTo,
});

export const fetchAllSuppliersDone = suppliers => ({
	type: SUPPLIERS_FETCH_ALL_SUCCESS,
	suppliers,
});

export const fetchAllSuppliersFailed = reason => ({
	type: SUPPLIERS_FETCH_ALL_FAIL,
	reason,
});

export const fetchAllSuppliersFinally = () => ({ type: SUPPLIERS_FETCH_ALL_FINALLY });

export const fetchSupplier = id => ({
	type: SUPPLIERS_FETCH_START,
	id,
});

export const fetchSupplierDone = supplier => ({
	type: SUPPLIERS_FETCH_SUCCESS,
	supplier,
});

export const fetchSupplierFailed = (id, reason) => ({
	type: SUPPLIERS_FETCH_FAIL,
	id,
	reason,
});

export const fetchSupplierFinally = () => ({
	type: SUPPLIERS_FETCH_FINALLY,
});

export const createSupplier = supplier => ({
	type: SUPPLIERS_CREATE_START,
	supplier,
});

export const createSupplierDone = supplier => ({
	type: SUPPLIERS_CREATE_SUCCESS,
	supplier,
});

export const createSupplierFailed = (supplier, reason) => ({
	type: SUPPLIERS_CREATE_FAIL,
	supplier,
	reason,
});

export const createSupplierFinally = () => ({
	type: SUPPLIERS_CREATE_FINALLY,
});

export const updateSupplier = supplier => ({
	type: SUPPLIERS_UPDATE_START,
	supplier,
});

export const updateSupplierDone = supplier => ({
	type: SUPPLIERS_UPDATE_SUCCESS,
	supplier,
});

export const updateSupplierFailed = (supplier, reason) => ({
	type: SUPPLIERS_UPDATE_FAIL,
	supplier,
	reason,
});

export const updateSupplierFinally = () => ({
	type: SUPPLIERS_UPDATE_FINALLY,
});

export const deleteSupplier = id => ({
	type: SUPPLIERS_DELETE_START,
	id,
});

export const deleteSupplierDone = id => ({
	type: SUPPLIERS_DELETE_SUCCESS,
	id,
});

export const deleteSupplierFailed = (id, reason) => ({
	type: SUPPLIERS_DELETE_FAIL,
	id,
	reason,
});

export const deleteSupplierFinally = () => ({
	type: SUPPLIERS_DELETE_FINALLY,
});

export const setSupplierField = (field, value) => ({
	type: SUPPLIERS_SET_FIELD,
	field,
	value,
});

export const newSupplier = () => ({
	type: SUPPLIERS_NEW_SUPPLIER,
});

