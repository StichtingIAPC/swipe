export const STOCK_FETCH_START = '/stock/fetch/start';
export const STOCK_FETCH_DONE = '/stock/fetch/done';
export const STOCK_FETCH_FAILED = '/stock/fetch/failed';

export function startFetchingStockList({ redirectTo } = {}) {
	return {
		type: STOCK_FETCH_START,
		redirectTo,
	};
}

export function doneFetchingStockList(stock) {
	return {
		type: STOCK_FETCH_DONE,
		stock,
	};
}


export function fetchingStockListError(error) {
	return {
		type: STOCK_FETCH_FAILED,
		error,
	};
}


export {
	startFetchingStockList as stock
};

