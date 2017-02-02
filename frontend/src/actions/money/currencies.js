/**
 * Created by Matthias on 26/11/2016.
 */
export function startFetchingCurrencies({ redirectTo } = {}) {
	return { type: 'CURRENCY_FETCH_START', redirectTo };
}

export function doneFetchingCurrencies(currencies) {
	return { type: 'CURRENCY_FETCH_DONE', currencies };
}

export function createCurrency(currency) {
	return { type: 'CURRENCY_CREATE', curr: currency };
}

export function updateCurrency(currency) {
	return {	type: 'CURRENCY_UPDATE', curr: currency };
}

export function deleteCurrency(currency) {
	return { type: 'CURRENCY_DELETE', curr: currency };
}

export function currencyInputError(error) {
	return { type: 'CURRENCY_INPUT_ERROR', error: error }
}

export function currencyFetchError(error) {
	return { type: 'CURRENCY_FETCH_ERROR', error: error }
}

export {
	startFetchingCurrencies as currencies,
}
