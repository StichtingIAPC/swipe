export const STOCK_FETCH_START = '/stock/fetch/start';
export const STOCK_FETCH_DONE = '/stock/fetch/done';
export const STOCK_FETCH_FAIL = '/stock/fetch/fail';
export const STOCK_FETCH_FINALLY = '/stock/fetch/finally';

export const startFetchingStockList = ({ redirectTo } = {}) => ({
	type: STOCK_FETCH_START,
	redirectTo,
});

export const doneFetchingStockList = stock => ({
	type: STOCK_FETCH_DONE,
	stock,
});

export const fetchingStockListError = error => ({
	type: STOCK_FETCH_FAIL,
	error,
});

export const fetchingStockListCompleted = () => ({
	type: STOCK_FETCH_FINALLY,
});

export {
	startFetchingStockList as stock,
};
