/* eslint-disable no-undefined,no-undef */

import {
	SALES_PAYMENT_TYPES_ADD_TO_RECEIPT,
	SALES_PAYMENT_TYPE_REMOVE_FROM_RECEIPT,
	removePaymentType,
	addPaymentType
} from './actions';

describe('Action tests for sales.payments', () => {
	test('addPaymentType', () => {
		expect(addPaymentType('MAESTRO', 4)).toEqual({ type: SALES_PAYMENT_TYPES_ADD_TO_RECEIPT,
			paymentType: 'MAESTRO',
			amount: 4 });
	});
	test('deletePaymentType', () => {
		expect(removePaymentType('MAESTRO')).toEqual({ type: SALES_PAYMENT_TYPE_REMOVE_FROM_RECEIPT,
			paymentType: 'MAESTRO' });
	});
});
