export function fetchAllCurrencies(redirectTo) {
	return {
		type: 'money/currencies/FETCH_ALL',
		redirectTo,
	};
}

export function fetchAllCurrenciesDone(currencies) {
	return {
		type: 'money/currencies/FETCH_ALL_DONE',
		currencies,
	};
}

export function fetchAllCurrenciesFailed(reason) {
	return {
		type: 'money/currencies/FETCH_ALL_FAILED',
		reason,
	};
}

export function fetchAllCurrenciesFinally() {
	return {
		type: 'money/currencies/FETCH_ALL_FINALLY',
	};
}

export function fetchCurrency(id) {
	return {
		type: 'money/currencies/FETCH',
		id,
	};
}

export function fetchCurrencyDone(currency) {
	return {
		type: 'money/currencies/FETCH_DONE',
		currency,
	};
}

export function fetchCurrencyFailed(id, reason) {
	return {
		type: 'money/currencies/FETCH_FAILED',
		id,
		reason,
	};
}

export function fetchCurrencyFinally() {
	return { type: 'money/currencies/FETCH_FINALLY' };
}

export function createCurrency(currency) {
	return {
		type: 'money/currencies/CREATE',
		currency,
	};
}

export function createCurrencyDone(currency) {
	return {
		type: 'money/currencies/CREATE_DONE',
		currency,
	};
}

export function createCurrencyFailed(currency, reason) {
	return {
		type: 'money/currencies/CREATE_FAILED',
		currency,
		reason,
	};
}

export function createCurrencyFinally() {
	return { type: 'money/currencies/CREATE_FINALLY' };
}

export function updateCurrency(currency) {
	return {
		type: 'money/currencies/UPDATE',
		currency,
	};
}

export function updateCurrencyDone(currency) {
	return {
		type: 'money/currencies/UPDATE_DONE',
		currency,
	};
}

export function updateCurrencyFailed(currency, reason) {
	return {
		type: 'money/currencies/UPDATE_FAILED',
		currency,
		reason,
	};
}

export function updateCurrencyFinally() {
	return {
		type: 'money/currencies/UPDATE_FINALLY',
	};
}

export function deleteCurrency(id) {
	return {
		type: 'money/currencies/DELETE',
		id,
	};
}

export function deleteCurrencyDone(id) {
	return {
		type: 'money/currencies/DELETE_DONE',
		id,
	};
}

export function deleteCurrencyFailed(id, reason) {
	return {
		type: 'money/currencies/DELETE_FAILED',
		id,
		reason,
	};
}

export function deleteCurrencyFinally() {
	return { type: 'money/currencies/DELETE_FINALLY' };
}

export function setCurrencyField(field, value) {
	return {
		type: 'money/currencies/SET_FIELD',
		field,
		value,
	};
}
export function resetCurrency() {
	return {
		type: 'money/currencies/NEW_CURRENCY',
	};
}

export default fetchAllCurrencies;
export {
	fetchAllCurrencies as currencies
};
