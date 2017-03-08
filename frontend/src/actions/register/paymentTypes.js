export function startFetchingPaymentTypes({redirectTo} = {}) {
	return { type: 'PAYMENT_TYPE_FETCH_START', redirectTo };
}

export function doneFetchingPaymentTypes(paymentTypes) {
	return { type: 'PAYMENT_TYPE_FETCH_DONE', paymentTypes };
}

export function createPaymentType(paymentType) {
	return { type: 'PAYMENT_TYPE_CREATE', paymentType };
}

export function updatePaymentType(paymentType) {
	return { type: 'PAYMENT_TYPE_UPDATE', paymentType };
}

export function deletePaymentType(paymentType) {
	return { type: 'PAYMENT_TYPE_DELETE', paymentType };
}

export function paymentTypeFetchError(error) {
	return { type: 'PAYMENT_TYPE_FETCH_ERROR', error };
}

export function paymentTypeInputError(error) {
	return { type: 'PAYMENT_TYPE_INPUT_ERROR', error };
}

export {
	startFetchingPaymentTypes as paymentTypes,
}
