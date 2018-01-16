/* eslint-disable object-property-newline */
export const ADD_PAYMENT_TYPE = 'sales/payment/paymentType/add';
export const REMOVE_PAYMENT_TYPE = 'sales/payment/paymentType/add';

export const addPaymentType = (amount) => ({ type: ADD_PAYMENT_TYPE, amount });
export const removePaymentType = () => ({ type: REMOVE_PAYMENT_TYPE });

