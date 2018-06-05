import Big from 'big.js';
import { getDummySalesTotal } from '../selectors';

export const getPaymentsOnReceipt = state => state.sales.payments.paymentTypes;
export const getPaymentsOnReceiptAsListForAPI = state => Object.keys(getPaymentsOnReceipt(state))
	.map(id => ({
		money: getPaymentsOnReceipt(state)[id],
		payment_type: id,
	}))
	.filter(it => !new Big(it.money.amount).eq(0));
// ATTENTION: getPaymentsOnReceiptDeficit depends on a working Receipt.
// The workings of this function are wrong as long as Receipt and getSalesTotal has not been implemented
export const getPaymentsOnReceiptDeficit = state => new Big(getDummySalesTotal(state).amount)
	.minus(Object.values(getPaymentsOnReceipt(state))
		.reduce((accumulator, payment) => accumulator.plus(payment.amount), new Big(0)))
	.toFixed(5);
export const getIsPaymentSplit = state => state.sales.payments.paymentIsSplit;
export const getPaymentTypesTotalValidations = state => state.sales.payments.validations;
