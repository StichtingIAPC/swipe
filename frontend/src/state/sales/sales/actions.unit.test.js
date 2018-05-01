/* eslint-disable no-undefined,no-undef */

import {
	SALES_MUTATE_SALES_LINE,
	mutateSalesLineOfArticle
} from './actions';

describe('Action tests for sales.actions', () => {
	test('mutateSalesLineOfArticle add', () => {
		expect(mutateSalesLineOfArticle('article', 4)).toEqual({
			type: SALES_MUTATE_SALES_LINE,
			article: 'article',
			amount: 4 });
	});

	test('mutateSalesLineOfArticle subtract', () => {
		expect(mutateSalesLineOfArticle('article', -4)).toEqual({
			type: SALES_MUTATE_SALES_LINE,
			article: 'article',
			amount: -4 });
	});
});
