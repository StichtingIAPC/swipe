import { getSalesTotal } from '../../assortment/articles/selectors';
import Big from 'big.js';

export const getPaymentsOnReceipt = state => state.sales.payments.paymentTypes;
export const getPaymentsOnReceiptAsListForAPI = state => Object.keys(getPaymentsOnReceipt(state))
	.map(id => ({
		money: getPaymentsOnReceipt(state)[id],
		payment_type: id,
	}))
	.filter(it => !(new Big(it.money.amount).eq(0)));
export const getPaymentsOnReceiptDeficit = state => {
	const result = new Big(getSalesTotal(state).amount)
		.minus(Object.values(getPaymentsOnReceipt(state))
			.reduce((accumulator, payment) => accumulator.plus(payment.amount), new Big(0)))
		.toFixed(5);
	return result;
};
export const getIsPaymentSplit = state => state.sales.payments.paymentIsSplit;
export const getPaymentTypesTotalValidations = state => state.sales.payments.validations;
