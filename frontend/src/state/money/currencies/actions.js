export const MONEY_CURRENCIES_FETCH_ALL_START = 'money/currencies/fetchAll/start';
export const MONEY_CURRENCIES_FETCH_ALL_SUCCESS = 'money/currencies/fetchAll/success';
export const MONEY_CURRENCIES_FETCH_ALL_FAIL = 'money/currencies/fetchAll/fail';
export const MONEY_CURRENCIES_FETCH_ALL_FINALLY = 'money/currencies/fetchAll/finally';

export const MONEY_CURRENCIES_FETCH_START = 'money/currencies/fetch/start';
export const MONEY_CURRENCIES_FETCH_SUCCESS = 'money/currencies/fetch/success';
export const MONEY_CURRENCIES_FETCH_FAIL = 'money/currencies/fetch/fail';
export const MONEY_CURRENCIES_FETCH_FINALLY = 'money/currencies/fetch/finally';

export const MONEY_CURRENCIES_CREATE_START = 'money/currencies/create/start';
export const MONEY_CURRENCIES_CREATE_SUCCESS = 'money/currencies/create/success';
export const MONEY_CURRENCIES_CREATE_FAIL = 'money/currencies/create/fail';
export const MONEY_CURRENCIES_CREATE_FINALLY = 'money/currencies/create/finally';

export const MONEY_CURRENCIES_UPDATE_START = 'money/currencies/update/start';
export const MONEY_CURRENCIES_UPDATE_SUCCESS = 'money/currencies/update/success';
export const MONEY_CURRENCIES_UPDATE_FAIL = 'money/currencies/update/fail';
export const MONEY_CURRENCIES_UPDATE_FINALLY = 'money/currencies/update/finally';

export const MONEY_CURRENCIES_DELETE_START = 'money/currencies/delete/start';
export const MONEY_CURRENCIES_DELETE_SUCCESS = 'money/currencies/delete/success';
export const MONEY_CURRENCIES_DELETE_FAIL = 'money/currencies/delete/fail';
export const MONEY_CURRENCIES_DELETE_FINALLY = 'money/currencies/delete/finally';

export const MONEY_CURRENCIES_SET_FIELD = 'money/currencies/setField';
export const MONEY_CURRENCIES_NEW_CURRENCY = 'money/currencies/newCurrency';

export const fetchAllCurrencies = redirectTo => ({
	type: MONEY_CURRENCIES_FETCH_ALL_START,
	redirectTo,
});

export const fetchAllCurrenciesDone = currencies => ({
	type: MONEY_CURRENCIES_FETCH_ALL_SUCCESS,
	currencies,
});

export const fetchAllCurrenciesFailed = reason => ({
	type: MONEY_CURRENCIES_FETCH_ALL_FAIL,
	reason,
});

export const fetchAllCurrenciesFinally = () => ({
	type: MONEY_CURRENCIES_FETCH_ALL_FINALLY,
});

export const fetchCurrency = id => ({
	type: MONEY_CURRENCIES_FETCH_START,
	id,
});

export const fetchCurrencyDone = currency => ({
	type: MONEY_CURRENCIES_FETCH_SUCCESS,
	currency,
});

export const fetchCurrencyFailed = (id, reason) => ({
	type: MONEY_CURRENCIES_FETCH_FAIL,
	id,
	reason,
});

export const createCurrency = currency => ({
	type: MONEY_CURRENCIES_CREATE_START,
	currency,
});

export const createCurrencyDone = currency => ({
	type: MONEY_CURRENCIES_CREATE_SUCCESS,
	currency,
});

export const createCurrencyFailed = (currency, reason) => ({
	type: MONEY_CURRENCIES_CREATE_FAIL,
	currency,
	reason,
});

export const updateCurrency = currency => ({
	type: MONEY_CURRENCIES_UPDATE_START,
	currency,
});

export const updateCurrencyDone = currency => ({
	type: MONEY_CURRENCIES_UPDATE_SUCCESS,
	currency,
});

export const updateCurrencyFailed = (currency, reason) => ({
	type: MONEY_CURRENCIES_UPDATE_FAIL,
	currency,
	reason,
});

export const updateCurrencyFinally = () => ({
	type: MONEY_CURRENCIES_UPDATE_FINALLY,
});

export const deleteCurrency = id => ({
	type: MONEY_CURRENCIES_DELETE_START,
	id,
});

export const deleteCurrencyDone = id => ({
	type: MONEY_CURRENCIES_DELETE_SUCCESS,
	id,
});

export const deleteCurrencyFailed = (id, reason) => ({
	type: MONEY_CURRENCIES_DELETE_FAIL,
	id,
	reason,
});

export const setCurrencyField = (field, value) => ({
	type: MONEY_CURRENCIES_SET_FIELD,
	field,
	value,
});

export const resetCurrency = () => ({
	type: MONEY_CURRENCIES_NEW_CURRENCY,
});

