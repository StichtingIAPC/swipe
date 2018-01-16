/* eslint-disable object-property-newline */
export const ADD_PAYMENT_TYPE = 'sales/payments/paymentType/add';
export const REMOVE_PAYMENT_TYPE = 'sales/payments/paymentType/add';

export const addPaymentType = (paymentType, amount) => ({ type: ADD_PAYMENT_TYPE, paymentType, amount });
export const removePaymentType = (paymentType) => ({ type: REMOVE_PAYMENT_TYPE, paymentType });

