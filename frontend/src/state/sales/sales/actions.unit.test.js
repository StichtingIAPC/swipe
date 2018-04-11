/* eslint-disable no-undefined,no-undef */

import {
	SALES_MUTATE_SALES_LINE,
	addToSalesListAction
} from './actions';

describe('Action tests for sales.actions', () => {
	test('addToSalesListAction', () => {
		expect(addToSalesListAction('article', 4, 6)).toEqual({
			type: SALES_MUTATE_SALES_LINE,
			article: 'article',
			count: 4,
			currentAmount: 6 });
	});
});
