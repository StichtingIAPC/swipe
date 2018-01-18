/* eslint-disable no-undefined,no-undef */

import {
	ADD_PAYMENT_TYPE,
	REMOVE_PAYMENT_TYPE,
	removePaymentType,
	addPaymentType
} from './actions';

describe('Action tests for sales.payments', () => {
	test('addPaymentType', () => {
		expect(addPaymentType('MAESTRO', 4)).toEqual({ type: ADD_PAYMENT_TYPE,
			paymentType: 'MAESTRO',
			amount: 4 });
	});
	test('deletePaymentType', () => {
		expect(removePaymentType('MAESTRO')).toEqual({ type: REMOVE_PAYMENT_TYPE,
			paymentType: 'MAESTRO' });
	});
});
