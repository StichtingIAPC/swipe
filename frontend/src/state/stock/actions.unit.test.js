/* eslint-disable no-undefined,no-undef */


import {
	doneFetchingStockList, fetchingStockListCompleted, fetchingStockListError, startFetchingStockList,
	STOCK_FETCH_FINALLY, STOCK_FETCH_DONE,
	STOCK_FETCH_FAIL,
	STOCK_FETCH_START
} from './actions';
describe('Action tests for sales.actions', () => {

	test('STOCK_FETCH_START without redirect adds no redirect', () => {
		expect(startFetchingStockList(undefined)).toEqual({ type: STOCK_FETCH_START });
	});
	test('STOCK_FETCH_START with redirectTo adds redirect', () => {
		expect(startFetchingStockList({ redirectTo: 'aa' })).toEqual({ type: STOCK_FETCH_START, redirectTo: 'aa' });
	});

	test('STOCK_FETCH_DONE', () => {
		expect(doneFetchingStockList([ 'a' ])).toEqual({ type: STOCK_FETCH_DONE, stock: [ 'a' ]});
	});

	test('STOCK_FETCH_FAIL', () => {
		expect(fetchingStockListError('something went wrong')).toEqual({ type: STOCK_FETCH_FAIL, error: 'something went wrong' });
	});

	test('STOCK_FETCH_FAIL', () => {
		expect(fetchingStockListCompleted()).toEqual({ type: STOCK_FETCH_FINALLY });
	});
});
