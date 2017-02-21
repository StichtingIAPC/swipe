/**
 * Created by Matthias on 26/11/2016.
 */
export function startFetchingVATPeriods({ redirectTo } = {}) {
	return { type: 'VAT_PERIOD_FETCH_START', redirectTo };
}

export function doneFetchingVATPeriods(VATPeriods) {
	return { type: 'VAT_PERIOD_FETCH_DONE', VATPeriods };
}

export function createVATPeriod(VATPeriod) {
	return { type: 'VAT_PERIOD_CREATE', curr: VATPeriod };
}

export function updateVATPeriod(VATPeriod) {
	return {	type: 'VAT_PERIOD_UPDATE', curr: VATPeriod };
}

export function deleteVATPeriod(VATPeriod) {
	return { type: 'VAT_PERIOD_DELETE', curr: VATPeriod };
}

export function VATPeriodInputError(error) {
	return { type: 'VAT_PERIOD_INPUT_ERROR', error: error }
}

export function VATPeriodFetchError(error) {
	return { type: 'VAT_PERIOD_FETCH_ERROR', error: error }
}

export {
	startFetchingVATPeriods as VATPeriods,
}
