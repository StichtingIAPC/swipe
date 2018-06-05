export const FETCH_CUSTOMERS_ACTION = 'crm/customers/fetchAll';
export const FETCH_CUSTOMERS_SUCCESS = 'crm/customers/success';
export const FETCH_CUSTOMERS_ERROR = 'crm/customers/error';
export const FETCH_CUSTOMERS_FINALLY = 'crm/customers/finally';
export const FETCH_CUSTOMERS_IS_LOADING = 'crm/customers/loading';


export const fetchCustomersAction = () => ({ type: FETCH_CUSTOMERS_ACTION });
export const fetchCustomersSuccess = (customers) => ({ type: FETCH_CUSTOMERS_SUCCESS, customers });
export const fetchCustomersError = (error) => ({ type: FETCH_CUSTOMERS_ERROR, error });
export const fetchCustomersFinally = () => ({ type: FETCH_CUSTOMERS_FINALLY });
export const fetchCustomersIsLoading = () => ({ type: FETCH_CUSTOMERS_IS_LOADING });
