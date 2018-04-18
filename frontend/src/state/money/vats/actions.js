export const MONEY_VATS_FETCH_ALL_START = 'money/vats/fetchAll/start';
export const MONEY_VATS_FETCH_ALL_SUCCESS = 'money/vats/fetchAll/success';
export const MONEY_VATS_FETCH_ALL_FAIL = 'money/vats/fetchAll/fail';
export const MONEY_VATS_FETCH_ALL_FINALLY = 'money/vats/fetchAll/finally';

export const MONEY_VATS_FETCH_START = 'money/vats/fetch/start';
export const MONEY_VATS_FETCH_SUCCESS = 'money/vats/fetch/success';
export const MONEY_VATS_FETCH_FAIL = 'money/vats/fetch/fail';
export const MONEY_VATS_FETCH_FINALLY = 'money/vats/fetch/finally';

export const MONEY_VATS_CREATE_START = 'money/vats/create/start';
export const MONEY_VATS_CREATE_SUCCESS = 'money/vats/create/success';
export const MONEY_VATS_CREATE_FAIL = 'money/vats/create/fail';
export const MONEY_VATS_CREATE_FINALLY = 'money/vats/create/finally';

export const MONEY_VATS_UPDATE_START = 'money/vats/update/start';
export const MONEY_VATS_UPDATE_SUCCESS = 'money/vats/update/success';
export const MONEY_VATS_UPDATE_FAIL = 'money/vats/update/fail';
export const MONEY_VATS_UPDATE_FINALLY = 'money/vats/update/finally';

export const MONEY_VATS_DELETE_START = 'money/vats/delete/start';
export const MONEY_VATS_DELETE_SUCCESS = 'money/vats/delete/success';
export const MONEY_VATS_DELETE_FAIL = 'money/vats/delete/fail';
export const MONEY_VATS_DELETE_FINALLY = 'money/vats/delete/finally';

export const MONEY_VATS_SET_FIELD = 'money/vats/setField';
export const MONEY_VATS_NEW_VAT = 'money/vats/newVat';

export const fetchAllVatsStart = redirectTo => ({
	type: MONEY_VATS_FETCH_ALL_START,
	redirectTo,
});

export const fetchAllVatsDone = vats => ({
	type: MONEY_VATS_FETCH_ALL_SUCCESS,
	vats,
});

export const fetchAllVatsFail = reason => ({
	type: MONEY_VATS_FETCH_ALL_FAIL,
	reason,
});

export const fetchAllVatsFinally = () => ({
	type: MONEY_VATS_FETCH_ALL_FINALLY,
});

export const fetchVatStart = id => ({
	type: MONEY_VATS_FETCH_START,
	id,
});

export const fetchVatDone = vat => ({
	type: MONEY_VATS_FETCH_SUCCESS,
	vat,
});

export const fetchVatFail = (id, reason) => ({
	type: MONEY_VATS_FETCH_FAIL,
	id,
	reason,
});

export const fetchVatFinally = () => ({
	type: MONEY_VATS_FETCH_FINALLY,
});

export const createVatStart = vat => ({
	type: MONEY_VATS_CREATE_START,
	vat,
});

export const createVatDone = vat => ({
	type: MONEY_VATS_CREATE_SUCCESS,
	vat,
});

export const createVatFail = (vat, reason) => ({
	type: MONEY_VATS_CREATE_FAIL,
	vat,
	reason,
});

export const createVatFinally = () => ({
	type: MONEY_VATS_CREATE_FINALLY,
});

export const updateVatStart = vat => ({
	type: MONEY_VATS_UPDATE_START,
	vat,
});

export const updateVatDone = vat => ({
	type: MONEY_VATS_UPDATE_SUCCESS,
	vat,
});

export const updateVatFail = (vat, reason) => ({
	type: MONEY_VATS_UPDATE_FAIL,
	vat,
	reason,
});

export const updateVatFinally = () => ({
	type: MONEY_VATS_UPDATE_FINALLY,
});

export const deleteVatStart = id => ({
	type: MONEY_VATS_DELETE_START,
	id,
});

export const deleteVatDone = id => ({
	type: MONEY_VATS_DELETE_SUCCESS,
	id,
});

export const deleteVatFail = (id, reason) => ({
	type: MONEY_VATS_DELETE_FAIL,
	id,
	reason,
});

export const deleteVatFinally = () => ({
	type: MONEY_VATS_DELETE_FINALLY,
});

export const setVatField = (field, value) => ({
	type: MONEY_VATS_SET_FIELD,
	field,
	value,
});

export const resetVat = () => ({
	type: MONEY_VATS_NEW_VAT,
});

