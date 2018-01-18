/* eslint-disable no-undefined,no-undef */

import {
	SALES_ADD_PRODUCT,
	addToSalesListAction
} from './actions';

describe('Action tests for sales.payments', () => {
	test('addToSalesList', () => {
		expect(addToSalesListAction('article', 4, 6)).toEqual({ type: SALES_ADD_PRODUCT,
			article: 'article',
			count: 4,
			currentAmount: 6 });
	});

});
