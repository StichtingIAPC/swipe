/**
 * Created by Matthias on 26/11/2016.
 */
export function startFetchingVATs({ redirectTo } = {}) {
	return { type: 'VAT_FETCH_START', redirectTo };
}

export function doneFetchingVATs(VATs) {
	return { type: 'VAT_FETCH_DONE', VATs };
}

export function createVAT(VAT) {
	return { type: 'VAT_CREATE', vat: VAT };
}

export function updateVAT(VAT) {
	return {	type: 'VAT_UPDATE', vat: VAT };
}

export function deleteVAT(VAT) {
	return { type: 'VAT_DELETE', vat: VAT };
}

export function VATInputError(error) {
	return { type: 'VAT_INPUT_ERROR', error: error }
}

export function VATFetchError(error) {
	return { type: 'VAT_FETCH_ERROR', error: error }
}

export {
	startFetchingVATs as VATs,
}
