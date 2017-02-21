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
	return { type: 'VAT_CREATE', curr: VAT };
}

export function updateVAT(VAT) {
	return {	type: 'VAT_UPDATE', curr: VAT };
}

export function deleteVAT(VAT) {
	return { type: 'VAT_DELETE', curr: VAT };
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
