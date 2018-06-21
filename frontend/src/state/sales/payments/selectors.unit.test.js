/* eslint-disable no-undefined,no-undef */


import { getPaymentsOnReceipt, getPaymentTypes } from './selectors';
describe('Testing selector for state.payments', () => {
	test('addPaymentType', () => {
		const state = { register: { paymentTypes: { paymentTypes: [ 'maestro' ]}}};

		expect(getPaymentTypes(state)).toEqual([ 'maestro' ]);
	});
	test('getPaymentsOnReceipt', () => {
		const state = { sales: { payments: 'A' }};

		expect(getPaymentsOnReceipt(state)).toEqual('A');
	});
});
