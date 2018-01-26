export const FETCH_ALL_ACTION = 'logistics/externalise/fetchAll';
export const FETCH_ALL_SUCCESS = 'logistics/externalise/fetchAll/success';
export const FETCH_ALL_ERROR = 'logistics/externalise/fetchAll/error';
export const FETCH_ALL_FINALLY = 'logistics/externalise/fetchAll/finally';

export const fetchAll = () => ({ type: FETCH_ALL_ACTION });
export const fetchAllSuccess = externalisations => ({ type: FETCH_ALL_SUCCESS,
	externalisations });
export const fetchAllError = reason => ({ type: FETCH_ALL_ERROR,
	reason });
export const fetchAllFinally = () => ({ type: FETCH_ALL_FINALLY });
