import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { currencyFetchError, currencyInputError, doneFetchingCurrencies, startFetchingCurrencies } from './actions';
import { get, post, put as api_put } from '../../../api.js';

function* fetchCurrencies({ redirectTo }) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/money/currency/',
		)).json();

		yield put(doneFetchingCurrencies(data));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}

		yield put(currencyFetchError(msg));
	}
}

function* createCurrency({ curr }) {
	const currency = { ...curr };
	let msg = null;

	try {
		const data = yield (yield call(
			post,
			'/money/currency/',
			currency,
		)).json();

		yield put(startFetchingCurrencies({ redirectTo: `/money/currency/${data.iso}/` }));
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = yield e.json();
		}

		yield put(currencyInputError(msg));
	}
}

function* updateCurrency({ curr }) {
	const currency = { ...curr };
	let msg = null;

	try {
		const data = yield (yield call(
			api_put,
			`/money/currency/${currency.iso}/`,
			currency,
		)).json();

		yield put(startFetchingCurrencies({ redirectTo: `/money/currency/${data.iso}/` }));
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = yield e.json();
		}

		yield put(currencyInputError(msg));
	}
}

export default function* saga() {
	yield takeLatest('CURRENCY_FETCH_START', fetchCurrencies);
	yield takeEvery('CURRENCY_CREATE', createCurrency);
	yield takeEvery('CURRENCY_UPDATE', updateCurrency);
}
