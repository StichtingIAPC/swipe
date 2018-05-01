/**
 * Created by nander on 16-1-18.
 */
export const getPaymentTypes = state => state.register.paymentTypes.paymentTypes;
export const getPaymentsOnReceipt = state => state.sales.payments.paymentTypes;
export const getPaymentsOnReceiptAsListForAPI = state => Object.keys(getPaymentsOnReceipt(state))
	.map(id => ({
		money: getPaymentsOnReceipt(state)[id],
		payment_type: id,
	}))
	.filter(it => it.money.amount !== 0 && it.money.amount !== '0');
export const getIsPaymentSplit = state => state.sales.payments.paymentIsSplit;
