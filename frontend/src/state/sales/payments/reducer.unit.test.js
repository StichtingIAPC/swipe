/* eslint-disable no-undefined,no-undef */

import paymentReducer from './reducer.js';
import { ADD_PAYMENT_TYPE, REMOVE_PAYMENT_TYPE } from './actions';
describe('Tests reducer for sales.payments', () => {
	test('undefined', () => {
		expect(paymentReducer(undefined, {})).toEqual({});
	});
	test('undefined', () => {
		expect(paymentReducer(undefined, { type: ADD_PAYMENT_TYPE,
			paymentType: 'MAESTRO',
			amount: 4 })).toEqual({ MAESTRO: 4 });
	});

	test('undefined', () => {
		expect(paymentReducer({ MAESTRO: 4 }, { type: REMOVE_PAYMENT_TYPE,
			paymentType: 'MAESTRO' })).toEqual({});
	});

	test('undefined', () => {
		expect(paymentReducer({ MAESTRO: 6 }, { type: ADD_PAYMENT_TYPE,
			paymentType: 'MAESTRO',
			amount: 4 })).toEqual({ MAESTRO: 4 });
	});
});
