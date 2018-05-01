/* eslint-disable no-undefined,no-undef */


import {
	getPaymentsOnReceipt,
	getPaymentTypes,
	getPaymentsOnReceiptAsListForAPI,
	getIsPaymentSplit
} from './selectors';

describe('Testing selector for state.payments', () => {
	test('getPaymentTypes', () => {
		const state = { register: { paymentTypes: { paymentTypes: [{
			id: '7',
			name: 'Meastro',
			is_invoicing: false,
		}]}}};

		expect(getPaymentTypes(state)).toEqual([{
			id: '7',
			name: 'Meastro',
			is_invoicing: false,
		}]);
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
