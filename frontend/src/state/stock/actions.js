export const STOCK_FETCH_START = '/stock/fetch/start';
export const STOCK_FETCH_DONE = '/stock/fetch/done';
export const STOCK_FETCH_FAILED = '/stock/fetch/failed';
export const STOCK_FETCH_COMPLETED = '/stock/fetch/completed';

export const startFetchingStockList = ({ redirectTo } = {}) =>  ({ type: STOCK_FETCH_START, redirectTo });

export const doneFetchingStockList = (stock) => ({type: STOCK_FETCH_DONE, stock});
export const fetchingStockListError = (error) => ({type: STOCK_FETCH_FAILED, error});
export const fetchingStockListCompleted = () => ({ type: STOCK_FETCH_COMPLETED });

export {
	startFetchingStockList as stock
};

