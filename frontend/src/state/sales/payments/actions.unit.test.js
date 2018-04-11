/* eslint-disable no-undefined,no-undef */

import {
	ADD_PAYMENT_TYPE_TO_RECEIPT,
	REMOVE_PAYMENT_TYPE_FROM_RECEIPT,
	removePaymentType,
	setAmountOfPaymentType
} from './actions';

describe('Action tests for sales.payments', () => {
	test('setAmountOfPaymentType', () => {
		expect(setAmountOfPaymentType('MAESTRO', 4)).toEqual({ type: ADD_PAYMENT_TYPE_TO_RECEIPT,
			paymentType: 'MAESTRO',
			amount: 4 });
	});
	test('deletePaymentType', () => {
		expect(removePaymentType('MAESTRO')).toEqual({ type: REMOVE_PAYMENT_TYPE_FROM_RECEIPT,
			paymentType: 'MAESTRO' });
	});
});
