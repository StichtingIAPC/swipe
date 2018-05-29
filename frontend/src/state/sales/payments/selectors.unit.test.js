/* eslint-disable no-undefined,no-undef */

import Big from 'big.js';

import {
	getPaymentsOnReceipt,
	getPaymentsOnReceiptDeficit,
	getPaymentsOnReceiptAsListForAPI,
	getIsPaymentSplit
} from './selectors';

describe('Testing selector for state.payments', () => {
	test('getPaymentsOnReceiptDeficit', () => {
		const state = { sales: {
			sales: [{
				price: { amount: '100' },
				count: 2,
			}],
			payments: { paymentTypes: { 7: { amount: '10' }}}}};
		const test = getPaymentsOnReceiptDeficit(state);

		expect(new Big(getPaymentsOnReceiptDeficit(state)).eq(190)).toBe(true);
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
