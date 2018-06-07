export const PAYMENT_TYPE_FETCH_START = 'register/payment_types/fetchAll/start';
export const PAYMENT_TYPE_FETCH_DONE = 'register/payment_types/fetchAll/done';
export const PAYMENT_TYPE_CREATE = 'register/payment_types/create';
export const PAYMENT_TYPE_UPDATE = 'register/payment_types/update';
export const PAYMENT_TYPE_FETCH_ERROR = 'register/payment_types/fetchAll/error';
export const PAYMENT_TYPE_INPUT_ERROR = 'register/payment_types/fetchAll/inputError';

export function startFetchingPaymentTypes({ redirectTo } = {}) {
	return {
		type: PAYMENT_TYPE_FETCH_START,
		redirectTo,
	};
}

export function doneFetchingPaymentTypes(paymentTypes) {
	return {
		type: PAYMENT_TYPE_FETCH_DONE,
		paymentTypes,
	};
}

export function createPaymentType(paymentType) {
	return {
		type: PAYMENT_TYPE_CREATE,
		paymentType,
	};
}

export function updatePaymentType(paymentType) {
	return {
		type: PAYMENT_TYPE_UPDATE,
		paymentType,
	};
}

export function paymentTypeFetchError(error) {
	return {
		type: PAYMENT_TYPE_FETCH_ERROR,
		error,
	};
}

export function paymentTypeInputError(error) {
	return {
		type: PAYMENT_TYPE_INPUT_ERROR,
		error,
	};
}

export {
	startFetchingPaymentTypes as paymentTypes,
};
