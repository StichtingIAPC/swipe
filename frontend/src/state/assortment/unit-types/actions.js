export const ASSORTMENT_UNIT_TYPES_FETCH_ALL_START = 'assortment/unit_types/fetch/all/start';
export const ASSORTMENT_UNIT_TYPES_FETCH_ALL_SUCCESS = 'assortment/unit_types/fetch/all/success';
export const ASSORTMENT_UNIT_TYPES_FETCH_ALL_FAIL = 'assortment/unit_types/fetch/all/fail';
export const ASSORTMENT_UNIT_TYPES_FETCH_ALL_FINALLY = 'assortment/unit_types/fetch/all/finally';

export const ASSORTMENT_UNIT_TYPES_FETCH_START = 'assortment/unit_types/fetch/start';
export const ASSORTMENT_UNIT_TYPES_FETCH_SUCCESS = 'assortment/unit_types/fetch/success';
export const ASSORTMENT_UNIT_TYPES_FETCH_FAIL = 'assortment/unit_types/fetch/fail';
export const ASSORTMENT_UNIT_TYPES_FETCH_FINALLY = 'assortment/unit_types/fetch/finally';

export const ASSORTMENT_UNIT_TYPES_CREATE_START = 'assortment/unit_types/create/start';
export const ASSORTMENT_UNIT_TYPES_CREATE_SUCCESS = 'assortment/unit_types/create/success';
export const ASSORTMENT_UNIT_TYPES_CREATE_FAIL = 'assortment/unit_types/create/fail';
export const ASSORTMENT_UNIT_TYPES_CREATE_FINALLY = 'assortment/unit_types/create/finally';

export const ASSORTMENT_UNIT_TYPES_UPDATE_START = 'assortment/unit_types/update/start';
export const ASSORTMENT_UNIT_TYPES_UPDATE_SUCCESS = 'assortment/unit_types/update/success';
export const ASSORTMENT_UNIT_TYPES_UPDATE_FAIL = 'assortment/unit_types/update/fail';
export const ASSORTMENT_UNIT_TYPES_UPDATE_FINALLY = 'assortment/unit_types/update/finally';

export const ASSORTMENT_UNIT_TYPES_DELETE_START = 'assortment/unit_types/delete/start';
export const ASSORTMENT_UNIT_TYPES_DELETE_SUCCESS = 'assortment/unit_types/delete/success';
export const ASSORTMENT_UNIT_TYPES_DELETE_FAIL = 'assortment/unit_types/delete/fail';
export const ASSORTMENT_UNIT_TYPES_DELETE_FINALLY = 'assortment/unit_types/delete/finally';

export const ASSORTMENT_UNIT_TYPES_SET_FIELD = 'assortment/unit_types/setField';


export const fetchAllUnitTypes = redirectTo => ({
	type: ASSORTMENT_UNIT_TYPES_FETCH_ALL_START,
	redirectTo,
});

export const fetchAllUnitTypesDone = unitTypes => ({
	type: ASSORTMENT_UNIT_TYPES_FETCH_ALL_SUCCESS,
	unitTypes,
});

export const fetchAllUnitTypesFailed = reason => ({
	type: ASSORTMENT_UNIT_TYPES_FETCH_ALL_FAIL,
	reason,
});

export const fetchAllUnitTypesFinally = () => ({
	type: ASSORTMENT_UNIT_TYPES_FETCH_ALL_FINALLY,
});

export const fetchUnitType = id => ({
	type: ASSORTMENT_UNIT_TYPES_FETCH_START,
	id,
});

export const fetchUnitTypeDone = unitType => ({
	type: ASSORTMENT_UNIT_TYPES_FETCH_SUCCESS,
	unitType,
});

export const fetchUnitTypeFailed = (id, reason) => ({
	type: ASSORTMENT_UNIT_TYPES_FETCH_FAIL,
	id,
	reason,
});

export const fetchUnitTypeFinally = () => ({
	type: ASSORTMENT_UNIT_TYPES_FETCH_FINALLY,
});

export const createUnitType = unitType => ({
	type: ASSORTMENT_UNIT_TYPES_CREATE_START,
	unitType,
});

export const createUnitTypeDone = unitType => ({
	type: ASSORTMENT_UNIT_TYPES_CREATE_SUCCESS,
	unitType,
});

export const createUnitTypeFailed = (unitType, reason) => ({
	type: ASSORTMENT_UNIT_TYPES_CREATE_FAIL,
	unitType,
	reason,
});

export const createUnitTypeFinally = () => ({
	type: ASSORTMENT_UNIT_TYPES_CREATE_FINALLY,
});

export const updateUnitType = unitType => ({
	type: ASSORTMENT_UNIT_TYPES_UPDATE_START,
	unitType,
});

export const updateUnitTypeDone = unitType => ({
	type: ASSORTMENT_UNIT_TYPES_UPDATE_SUCCESS,
	unitType,
});

export const updateUnitTypeFailed = (unitType, reason) => ({
	type: ASSORTMENT_UNIT_TYPES_UPDATE_FAIL,
	unitType,
	reason,
});

export const updateUnitTypeFinally = () => ({
	type: ASSORTMENT_UNIT_TYPES_UPDATE_FINALLY,
});

export const deleteUnitType = id => ({
	type: ASSORTMENT_UNIT_TYPES_DELETE_START,
	id,
});

export const deleteUnitTypeDone = id => ({
	type: ASSORTMENT_UNIT_TYPES_DELETE_SUCCESS,
	id,
});

export const deleteUnitTypeFailed = (id, reason) => ({
	type: ASSORTMENT_UNIT_TYPES_DELETE_FAIL,
	id,
	reason,
});

export const deleteUnitTypeFinally = () => ({
	type: ASSORTMENT_UNIT_TYPES_DELETE_FINALLY,
});

export const setUnitTypeField = (field, value) => ({
	type: ASSORTMENT_UNIT_TYPES_SET_FIELD,
	field,
	value,
});

