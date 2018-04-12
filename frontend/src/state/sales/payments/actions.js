/* eslint-disable object-property-newline */
export const SALES_PAYMENT_TYPES_ADD_TO_RECEIPT = 'sales/payments/paymentType/add';
export const SALES_PAYMENT_TYPE_REMOVE_FROM_RECEIPT = 'sales/payments/paymentType/remove';

export const addPaymentType = (paymentType, amount) => ({ type: SALES_PAYMENT_TYPES_ADD_TO_RECEIPT, paymentType, amount });
export const removePaymentType = paymentType => ({ type: SALES_PAYMENT_TYPE_REMOVE_FROM_RECEIPT, paymentType });

