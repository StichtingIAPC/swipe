export const ASSORTMENT_LABEL_TYPES_FETCH_ALL_START = 'assortment/label_types/fetchAll/start';
export const ASSORTMENT_LABEL_TYPES_FETCH_ALL_SUCCESS = 'assortment/label_types/fetchAll/success';
export const ASSORTMENT_LABEL_TYPES_FETCH_ALL_FAIL = 'assortment/label_types/fetchAll/fail';
export const ASSORTMENT_LABEL_TYPES_FETCH_ALL_FINALLY = 'assortment/label_types/fetchAll/finally';

export const ASSORTMENT_LABEL_TYPES_FETCH_START = 'assortment/label_types/fetch/start';
export const ASSORTMENT_LABEL_TYPES_FETCH_SUCCESS = 'assortment/label_types/fetch/success';
export const ASSORTMENT_LABEL_TYPES_FETCH_FAIL = 'assortment/label_types/fetch/fail';
export const ASSORTMENT_LABEL_TYPES_FETCH_FINALLY = 'assortment/label_types/fetch/finally';

export const ASSORTMENT_LABEL_TYPES_CREATE_START = 'assortment/label_types/create/start';
export const ASSORTMENT_LABEL_TYPES_CREATE_SUCCESS = 'assortment/label_types/create/success';
export const ASSORTMENT_LABEL_TYPES_CREATE_FAIL = 'assortment/label_types/create/fail';
export const ASSORTMENT_LABEL_TYPES_CREATE_FINALLY = 'assortment/label_types/create/finally';

export const ASSORTMENT_LABEL_TYPES_UPDATE_START = 'assortment/label_types/update/start';
export const ASSORTMENT_LABEL_TYPES_UPDATE_SUCCESS = 'assortment/label_types/update/success';
export const ASSORTMENT_LABEL_TYPES_UPDATE_FAIL = 'assortment/label_types/update/fail';
export const ASSORTMENT_LABEL_TYPES_UPDATE_FINALLY = 'assortment/label_types/update/finally';

export const ASSORTMENT_LABEL_TYPES_DELETE_START = 'assortment/label_types/delete/start';
export const ASSORTMENT_LABEL_TYPES_DELETE_SUCCESS = 'assortment/label_types/delete/success';
export const ASSORTMENT_LABEL_TYPES_DELETE_FAIL = 'assortment/label_types/delete/fail';
export const ASSORTMENT_LABEL_TYPES_DELETE_FINALLY = 'assortment/label_types/delete/finally';

export const ASSORTMENT_LABEL_TYPES_SET_FIELD = 'assortment/label_types/setField';

export const fetchAllLabelTypesStart = redirectTo => ({
	type: ASSORTMENT_LABEL_TYPES_FETCH_ALL_START,
	redirectTo,
});

export const fetchAllLabelTypesSuccess = labelTypes => ({
	type: ASSORTMENT_LABEL_TYPES_FETCH_ALL_SUCCESS,
	labelTypes,
});

export const fetchAllLabelTypesFail = reason => ({
	type: ASSORTMENT_LABEL_TYPES_FETCH_ALL_FAIL,
	reason,
});

export const fetchAllLabelTypesFinally = () => ({
	type: ASSORTMENT_LABEL_TYPES_FETCH_ALL_FINALLY,
});

export const fetchLabelTypeStart = id => ({
	type: ASSORTMENT_LABEL_TYPES_FETCH_START,
	id,
});

export const fetchLabelTypeSuccess = labelType => ({
	type: ASSORTMENT_LABEL_TYPES_FETCH_SUCCESS,
	labelType,
});

export const fetchLabelTypeFail = (id, reason) => ({
	type: ASSORTMENT_LABEL_TYPES_FETCH_FAIL,
	id,
	reason,
});

export const fetchLabelTypeFinally = () => ({
	type: ASSORTMENT_LABEL_TYPES_FETCH_FINALLY,
});
export const createLabelTypeStart = labelType => ({
	type: ASSORTMENT_LABEL_TYPES_CREATE_START,
	labelType,
});

export const createLabelTypeSuccess = labelType => ({
	type: ASSORTMENT_LABEL_TYPES_CREATE_SUCCESS,
	labelType,
});

export const createLabelTypeFail = (labelType, reason) => ({
	type: ASSORTMENT_LABEL_TYPES_CREATE_FAIL,
	labelType,
	reason,
});

export const createLabelTypeFinally = () => ({
	type: ASSORTMENT_LABEL_TYPES_CREATE_FINALLY,
});

export const updateLabelTypeStart = labelType => ({
	type: ASSORTMENT_LABEL_TYPES_UPDATE_START,
	labelType,
});

export const updateLabelTypeSuccess = labelType => ({
	type: ASSORTMENT_LABEL_TYPES_UPDATE_SUCCESS,
	labelType,
});

export const updateLabelTypeFail = (labelType, reason) => ({
	type: ASSORTMENT_LABEL_TYPES_UPDATE_FAIL,
	labelType,
	reason,
});

export const updateLabelTypeFinally = () => ({
	type: ASSORTMENT_LABEL_TYPES_UPDATE_FINALLY,
});

export const deleteLabelTypeStart = id => ({
	type: ASSORTMENT_LABEL_TYPES_DELETE_START,
	id,
});

export const deleteLabelTypeSuccess = id => ({
	type: ASSORTMENT_LABEL_TYPES_DELETE_SUCCESS,
	id,
});

export const deleteLabelTypeFail = (id, reason) => ({
	type: ASSORTMENT_LABEL_TYPES_DELETE_FAIL,
	id,
	reason,
});

export const deleteLabelTypeFinally = () => ({
	type: ASSORTMENT_LABEL_TYPES_DELETE_FINALLY,
});

export const setLabelTypeField = (field, value) => ({
	type: ASSORTMENT_LABEL_TYPES_SET_FIELD,
	field,
	value,
});
