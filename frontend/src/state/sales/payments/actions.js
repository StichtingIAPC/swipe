/* eslint-disable object-property-newline */

export const SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT = 'sales/payments/paymentType/set';
export const TOGGLE_SPLIT_PAYMENT = 'sales/payments/paymentType/toggleSplit';
export const RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT = 'sales/payments/paymentType/reset';

export const setAmountOfPaymentType = (paymentType, amount) => ({
	type: SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT,
	field: paymentType.id,
	value: amount,
});

export const resetPaymentTypes = () => ({
	type: RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT,
});

export const toggleSplitPayment = () => ({
	type: TOGGLE_SPLIT_PAYMENT,
});
