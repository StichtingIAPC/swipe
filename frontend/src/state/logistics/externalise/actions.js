export const LOGISTICS_EXTRNALIZE_FETCH_ALL_START = 'logistics/externalise/fetchAll/start';
export const LOGISTICS_EXTRNALIZE_FETCH_ALL_SUCCESS = 'logistics/externalise/fetchAll/success';
export const LOGISTICS_EXTRNALIZE_FETCH_ALL_FAIL = 'logistics/externalise/fetchAll/fail';
export const LOGISTICS_EXTRNALIZE_FETCH_ALL_FINALLY = 'logistics/externalise/fetchAll/finally';

export const LOGISTICS_EXTRNALIZE_CREATE_START = 'logistics/externalise/create/start';
export const LOGISTICS_EXTRNALIZE_CREATE_SUCCESS = 'logistics/externalise/create/success';
export const LOGISTICS_EXTRNALIZE_CREATE_FAIL = 'logistics/externalise/create/fail';
export const LOGISTICS_EXTRNALIZE_CREATE_FINALLY = 'logistics/externalise/create/finally';

export const LOGISTICS_EXTRNALIZE_SET_LOADING = 'logistics/externalise/setLoading';
export const LOGISTICS_EXTRNALIZE_SET_VALIDATIONS = 'logistics/externalise/validations';
export const LOGISTICS_EXTRNALIZE_NEW = 'logistics/externalise/new';
export const LOGISTICS_EXTRNALIZE_SET_FIELD = 'logistics/externalise/setField';


export const fetchAllExternalizesStart = () => ({
	type: LOGISTICS_EXTRNALIZE_FETCH_ALL_START,
});

export const fetchAllExternalizesSuccess = externalisations => ({
	type: LOGISTICS_EXTRNALIZE_FETCH_ALL_SUCCESS,
	externalisations,
});

export const fetchAllExternalizesFail = reason => ({
	type: LOGISTICS_EXTRNALIZE_FETCH_ALL_FAIL,
	reason,
});

export const fetchAllExternalizesFinally = () => ({
	type: LOGISTICS_EXTRNALIZE_FETCH_ALL_FINALLY,
});

export const createExternalizeStart = externalise => ({
	type: LOGISTICS_EXTRNALIZE_CREATE_START,
	externalise,
});

export const createExternalizeSuccess = externalise => ({
	type: LOGISTICS_EXTRNALIZE_CREATE_SUCCESS,
	externalise,
});

export const createExternalizeFail = error => ({
	type: LOGISTICS_EXTRNALIZE_CREATE_FAIL,
	error,
});

export const createExternalizeFinally = () => ({
	type: LOGISTICS_EXTRNALIZE_CREATE_FINALLY,
});

export const setValidations = validations => ({
	type: LOGISTICS_EXTRNALIZE_SET_VALIDATIONS,
	validations,
});

export const newExternalize = () => ({
	type: LOGISTICS_EXTRNALIZE_NEW,
});

export const setLoadingAction = () => ({
	type: LOGISTICS_EXTRNALIZE_SET_LOADING,
});

export const setField = (field, value) => ({
	type: LOGISTICS_EXTRNALIZE_SET_FIELD,
	field,
	value,
});
