export function startFetchingStockList({ redirectTo } = {}) {
	return {
		type: 'STOCK_FETCH_START',
		redirectTo,
	};
}

export function doneFetchingStockList(stock) {
	return {
		type: 'STOCK_FETCH_DONE',
		stock,
	};
}


export function fetchingStockListError(error) {
	return {
		type: 'STOCK_FETCH_ERROR',
		error,
	};
}


export {
	startFetchingStockList as stock
};

