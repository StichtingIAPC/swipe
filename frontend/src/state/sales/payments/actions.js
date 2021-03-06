/* eslint-disable object-property-newline */

export const SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT = 'sales/payments/paymentType/set';
export const TOGGLE_SPLIT_PAYMENT = 'sales/payments/paymentType/toggleSplit';
export const RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT = 'sales/payments/paymentType/reset';
export const SET_VALIDATIONS = 'sales/payments/paymentType/validations';

export const setAmountOfPaymentType = (paymentTypeID, amount) => ({
	type: SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT,
	field: paymentTypeID,
	value: amount,
});

export const resetAmountOfPaymentTypes = () => ({
	type: RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT,
});

export const toggleSplitPayment = () => ({
	type: TOGGLE_SPLIT_PAYMENT,
});

export const setValidations = validations => ({
	type: SET_VALIDATIONS,
	validations,
});
