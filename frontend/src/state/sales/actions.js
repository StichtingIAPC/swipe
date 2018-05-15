/* eslint-disable object-property-newline */
export const SET_CUSTOMER = 'sales/setCustomer';

export const setCustomer = customer => ({ type: SET_CUSTOMER, customer });
export const resetCustomer = () => ({ type: SET_CUSTOMER, customer: null });
