export const FETCH_ALL_ACTION = 'logistics/externalise/fetchAll';
export const FETCH_ALL_SUCCESS = 'logistics/externalise/fetchAll/success';
export const FETCH_ALL_ERROR = 'logistics/externalise/fetchAll/error';
export const SET_VALIDATIONS = 'logistics/externalise/validations';
export const FETCH_ALL_FINALLY = 'logistics/externalise/fetchAll/finally';

export const CREATE_ACTION = 'logistics/externalise/create';
export const CREATE_SUCCESS = 'logistics/externalise/create/success';
export const CREATE_ERROR = 'logistics/externalise/create/error';
export const CREATE_FINALLY = 'logistics/externalise/create/finally';

export const NEW_ACTION = 'logistics/externalise/new';
export const SET_FIELD_ACTION = 'logistics/externalise/setField';

export const fetchAllAction = () => ({ type: FETCH_ALL_ACTION });
export const fetchAllSuccess = externalisations => ({ type: FETCH_ALL_SUCCESS,
	externalisations });
export const setValidations = validations => ({ type: SET_VALIDATIONS,
	validations });
export const fetchAllError = reason => ({ type: FETCH_ALL_ERROR,
	reason });
export const fetchAllFinally = () => ({ type: FETCH_ALL_FINALLY });

export const createAction = externalise => ({ type: CREATE_ACTION,
	externalise });
export const createSuccess = externalise => ({ type: CREATE_SUCCESS,
	externalise });
export const createError = error => ({ type: CREATE_ERROR,
	error });

export const createFinally = () => ({ type: CREATE_FINALLY });

export const newAction = () => ({ type: NEW_ACTION });
export const setFieldAction = (field, value) => ({ type: SET_FIELD_ACTION,
	field,
	value });
