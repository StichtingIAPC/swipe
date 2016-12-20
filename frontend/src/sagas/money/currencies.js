import { call, put } from "redux-saga/effects";
import { push } from "react-router-redux";
import {
	startFetchingCurrencies,
	doneFetchingCurrencies,
	currencyInputError,
	currencyFetchError
} from "../../actions/money/currencies";
import { get, post } from "../../api";

export function* fetchCurrencies({ redirectTo }) {
	try {
		const data = yield (yield call(
			get,
			'/money/currency/',
		)).json();
		yield put(doneFetchingCurrencies(data));
		if (redirectTo)
			yield put(push(redirectTo));
	} catch (e) {
		console.log(e);
		yield put(currencyFetchError(e.message));
	}
}

export function* createCurrency({ curr }) {
	const currency = {...curr};
	try {
		const data = yield (yield call(
			post,
			'/money/currency/',
			currency,
		)).json();
		yield put(startFetchingCurrencies({
			redirectTo: `/money/currency/${data.iso}/`,
		}));
	} catch (e) {
		console.log(e);
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield call(e.json.bind(e));
		yield put(currencyInputError(msg));
	}
}

export function* updateCurrency({ curr }) {
	const currency = {...curr};
	try {
		const data = yield (yield call(
			post,
			`/money/currency/${currency.iso}/`,
			currency,
		)).json();
		yield put(startFetchingCurrencies({
			redirectTo: `/money/currency/${data.iso}/`,
		}));
	} catch (e) {
		console.log(e);
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = yield call(e.json.bind(e));
		yield put(currencyInputError(msg));
	}
}
