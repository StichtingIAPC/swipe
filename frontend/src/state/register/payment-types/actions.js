export const REGISTER_PAYMENT_TYPES_FETCH_START = 'register/payment-types/fetch/start';
export const REGISTER_PAYMENT_TYPES_FETCH_SUCCESS = 'register/payment-types/fetch/success';
export const REGISTER_PAYMENT_TYPES_FETCH_FAIL = 'register/payment-types/fetch/fail';
export const REGISTER_PAYMENT_TYPES_FETCH_FINALLY = 'register/payment-types/fetch/finally';

export const REGISTER_PAYMENT_TYPES_CREATE_START = 'register/payment-types/create/start';
export const REGISTER_PAYMENT_TYPES_CREATE_SUCCESS = 'register/payment-types/create/success';
export const REGISTER_PAYMENT_TYPES_CREATE_FAIL = 'register/payment-types/create/fail';
export const REGISTER_PAYMENT_TYPES_CREATE_FINALLY = 'register/payment-types/create/finally';

export const REGISTER_PAYMENT_TYPES_UPDATE_START = 'register/payment-types/update/start';
export const REGISTER_PAYMENT_TYPES_UPDATE_SUCCESS = 'register/payment-types/update/success';
export const REGISTER_PAYMENT_TYPES_UPDATE_FAIL = 'register/payment-types/update/fail';
export const REGISTER_PAYMENT_TYPES_UPDATE_FINALLY = 'register/payment-types/update/finally';

export const REGISTER_PAYMENT_TYPES_DELETE_START = 'register/payment-types/delete/start';
export const REGISTER_PAYMENT_TYPES_DELETE_SUCCESS = 'register/payment-types/delete/success';
export const REGISTER_PAYMENT_TYPES_DELETE_FAIL = 'register/payment-types/delete/fail';
export const REGISTER_PAYMENT_TYPES_DELETE_FINALLY = 'register/payment-types/delete/finally';

export const REGISTER_PAYMENT_TYPES_INPUT_START = 'register/payment-types/input/start';
export const REGISTER_PAYMENT_TYPES_INPUT_SUCCESS = 'register/payment-types/input/success';
export const REGISTER_PAYMENT_TYPES_INPUT_FAIL = 'register/payment-types/input/fail';
export const REGISTER_PAYMENT_TYPES_INPUT_FINALLY = 'register/payment-types/input/finally';

export const doneFetchingPaymentTypes = paymentTypes => ({
	type: REGISTER_PAYMENT_TYPES_FETCH_SUCCESS,
	paymentTypes,
});

export const createPaymentType = paymentType => ({
	type: REGISTER_PAYMENT_TYPES_CREATE_START,
	paymentType,
});

export const updatePaymentType = paymentType => ({
	type: REGISTER_PAYMENT_TYPES_UPDATE_START,
	paymentType,
});

export const deletePaymentType = paymentType => ({
	type: REGISTER_PAYMENT_TYPES_DELETE_START,
	paymentType,
});

export const paymentTypeFetchError = error => ({
	type: REGISTER_PAYMENT_TYPES_FETCH_FAIL,
	error,
});

export const paymentTypeInputError = error => ({
	type: REGISTER_PAYMENT_TYPES_INPUT_FAIL,
	error,
});
