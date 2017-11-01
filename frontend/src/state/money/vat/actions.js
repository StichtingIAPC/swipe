export function startFetchingVATs({ redirectTo } = {}) {
	return {
		type: 'VAT_FETCH_START',
		redirectTo,
	};
}

export function doneFetchingVATs(vats) {
	return {
		type: 'VAT_FETCH_DONE',
		vats,
	};
}

export function createVAT(vat) {
	return {
		type: 'VAT_CREATE',
		vat,
	};
}

export function updateVAT(VAT) {
	return {
		type: 'VAT_UPDATE',
		vat: VAT,
	};
}

export function deleteVAT(VAT) {
	return {
		type: 'VAT_DELETE',
		vat: VAT,
	};
}

export function VATInputError(error) {
	return {
		type: 'VAT_INPUT_ERROR',
		error,
	};
}

export function VATFetchError(error) {
	return {
		type: 'VAT_FETCH_ERROR',
		error,
	};
}

export {
	startFetchingVATs as vats,
};
