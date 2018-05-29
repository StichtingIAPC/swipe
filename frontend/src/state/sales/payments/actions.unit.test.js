/* eslint-disable no-undefined,no-undef */

import {
	SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT,
	RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT,
	TOGGLE_SPLIT_PAYMENT,
	resetAmountOfPaymentTypes,
	setAmountOfPaymentType,
	toggleSplitPayment,
} from './actions';

describe('Action tests for sales.payments', () => {
	test('setAmountOfPaymentType', () => {
		expect(setAmountOfPaymentType('7', { amount: '5' })).toEqual({
			type: SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT,
			field: '7',
			value: { amount: '5' },
		});
	});

	test('resetPaymentTypes', () => {
		expect(resetAmountOfPaymentTypes()).toEqual({
			type: RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT,
		});
	});

	test('toggleSplitPayment', () => {
		expect(toggleSplitPayment()).toEqual({
			type: TOGGLE_SPLIT_PAYMENT,
		});
	});
});
