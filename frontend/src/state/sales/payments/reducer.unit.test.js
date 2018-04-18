/* eslint-disable no-undefined,no-undef */

import paymentReducer from './reducer.js';
import { SALES_PAYMENT_TYPES_ADD_TO_RECEIPT, SALES_PAYMENT_TYPE_REMOVE_FROM_RECEIPT } from './actions';
describe('Tests reducer for sales.payments', () => {
	test('undefined', () => {
		expect(paymentReducer(undefined, {})).toEqual({});
	});
	test('undefined', () => {
		expect(paymentReducer(undefined, { type: SALES_PAYMENT_TYPES_ADD_TO_RECEIPT,
			paymentType: 'MAESTRO',
			amount: 4 })).toEqual({ MAESTRO: 4 });
	});

	test('undefined', () => {
		expect(paymentReducer({ MAESTRO: 4 }, { type: SALES_PAYMENT_TYPE_REMOVE_FROM_RECEIPT,
			paymentType: 'MAESTRO' })).toEqual({});
	});

	test('undefined', () => {
		expect(paymentReducer({ MAESTRO: 6 }, { type: SALES_PAYMENT_TYPES_ADD_TO_RECEIPT,
			paymentType: 'MAESTRO',
			amount: 4 })).toEqual({ MAESTRO: 4 });
	});
});
