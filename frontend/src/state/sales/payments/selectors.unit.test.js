/* eslint-disable no-undefined,no-undef */

import Big from 'big.js';

import {
	getPaymentsOnReceipt,
	getPaymentsOnReceiptDeficit,
	getPaymentsOnReceiptAsListForAPI,
	getIsPaymentSplit
} from './selectors';

describe('Testing selector for state.payments', () => {
	// ATTENTION: getPaymentsOnReceiptDeficit Test:
	// The workings of this test are wrong as long as Receipt has not been implemented
	 test('getPaymentsOnReceiptDeficit', () => {
		const state = { sales: { payments: { paymentTypes: { 7: { amount: '10' }}}}};
		const test = getPaymentsOnReceiptDeficit(state);

		expect(new Big(getPaymentsOnReceiptDeficit(state)).eq('6959.420')).toBe(true);
	});

	test('getPaymentsOnReceipt', () => {
		const state = { sales: { payments: { paymentTypes: { 7: { amount: '10' }}}}};

		expect(getPaymentsOnReceipt(state)).toEqual({ 7: { amount: '10' }});
	});

	test('getPaymentsOnReceiptAsListForAPI', () => {
		const state = { sales: { payments: { paymentTypes: {
			7: { amount: '10' },
			8: { amount: '0' }},
		}}};

		expect(getPaymentsOnReceiptAsListForAPI(state))
			.toEqual([{ money: { amount: '10' },
				payment_type: '7',
			}]);
	});

	test('getIsPaymentSplit', () => {
		const state = { sales: { payments: { paymentIsSplit: true }}};

		expect(getIsPaymentSplit(state)).toEqual(true);
	});
});
