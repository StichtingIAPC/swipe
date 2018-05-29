/* eslint-disable object-property-newline */
export const ADD_PAYMENT_TYPE_TO_RECEIPT = 'sales/payments/paymentType/add';
export const REMOVE_PAYMENT_TYPE_FROM_RECEIPT = 'sales/payments/paymentType/add';
export const SET_PAYMENT_TYPES = 'sales/payments/paymentType/set';

export const addPaymentType = (paymentType, amount) => ({ type: ADD_PAYMENT_TYPE_TO_RECEIPT, paymentType, amount });
export const removePaymentType = paymentType => ({ type: REMOVE_PAYMENT_TYPE_FROM_RECEIPT, paymentType });
export const setPaymentTypes = paymentTypes => ({ type: SET_PAYMENT_TYPES, paymentTypes });

