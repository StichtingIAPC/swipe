/**
 * Created by Matthias on 26/11/2016.
 */

export const ADD_CURRENCY = 'ADD_CURRENCY';
export function addCurrency(currency) {
	return {
		type: ADD_CURRENCY,
		currency,
	}
}

export const REMOVE_CURRENCY = 'REMOVE_CURRENCY';
export function removeCurrency(iso) {
	return {
		type: REMOVE_CURRENCY,
		iso,
	}
}

export const MARK_CURRENCY_AS_UPDATING = 'MARK_CURRENCY_AS_UPDATING';
export function markCurrencyAsUpdating(iso) {
	return {
		type: MARK_CURRENCY_AS_UPDATING,
		iso,
	}
}

export const CHANGE_CURRENCY = 'CHANGE_CURRENCY';
export function changeCurrency(currency) {
	return {
		type: CHANGE_CURRENCY,
		currency,
	}
}

export const START_FETCH_CURRENCIES = 'START_FETCH_CURRENCIES';
export function startFetchCurrencies() {
	return {
		type: START_FETCH_CURRENCIES,
	}
}

export const INVALIDATE_CURRENCIES = 'INVALIDATE_CURRENCIES';
export function invalidateCurrencies() {
	return {
		type: INVALIDATE_CURRENCIES,
	}
}

export const RECEIVE_CURRENCIES = 'RECEIVE_CURRENCIES';
export function receiveCurrencies(currencies) {
	return {
		type: RECEIVE_CURRENCIES,
		currencies,
		date: new Date(),
	}
}

export function populateCurrencies() {
	return {
		type: 'MONEY_POPULATE_CURRENCIES',
	}
}

export function createCurrency(curr) {
	return {
		type: 'MONEY_CREATE_CURRENCY',
		curr,
	}
}

export function updateCurrency(curr) {
	return {
		type: 'MONEY_UPDATE_CURRENCY',
		curr,
	}
}

export {
	populateCurrencies as currencies,
}
