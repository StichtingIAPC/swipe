import {call, put} from "redux-saga/effects";
import {push} from "react-router-redux";
import {
	startFetchCurrencies,
	invalidateCurrencies,
	receiveCurrencies,
	addCurrency,
	markCurrencyAsUpdating,
	changeCurrency
} from "../../actions/money/currencies";
import config from "../../config";
import fetch from "isomorphic-fetch";

export function* populateCurrencies() {
	yield put(startFetchCurrencies());
	try {
		const data = yield (yield call(
			fetch,
			config.baseurl + '/money/currency/',
			{
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
				},
			}
		)).json();
		yield put(receiveCurrencies(data))
	} catch (e) {
		put(invalidateCurrencies());
	}
}

export function* createCurrency({ curr }) {
	const currency = {...curr};
	yield put(invalidateCurrencies());
	try {
		const data = yield (yield call(
			fetch,
			config.baseurl + '/money/currency/',
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(currency),
			}
		)).json();
		yield put(addCurrency(data));
		yield put(push(`/money/currency/${data.iso}/`));
	} catch (e) {
		put(invalidateCurrencies(e));
	}
}

export function* updateCurrency({ curr }) {
	const currency = {...curr};
	yield put(markCurrencyAsUpdating(curr.iso));
	try {
		const data = yield (yield call(
			fetch,
			config.baseurl + `/money/currency/${currency.iso}/`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				data: JSON.stringify(currency),
			}
		)).json();
		yield put(changeCurrency(data));
		yield put(push(`/money/currency/${data.iso}/`));
	} catch (e) {
		yield put(invalidateCurrencies(e));
	}
}
