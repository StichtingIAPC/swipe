import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import * as actions from './actions.js';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';
import * as api from '../../../api';

function* fetchAllCurrencies({ redirectTo }) {
	try {
		const currencies = yield (yield call(
			api.get,
			'/money/currency/',
		)).json();

		yield put(actions.fetchAllCurrenciesDone(currencies));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		yield put(actions.fetchAllCurrenciesFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchAllCurrenciesFinally());
	}
}

function* fetchCurrency({ id }) {
	try {
		const newCurrency = yield (yield call(
			api.get,
			`/money/currency/${id}`,
		)).json();

		yield put(actions.fetchCurrencyDone(newCurrency));
	} catch (e) {
		yield put(actions.fetchCurrencyFailed(id, cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchCurrencyFinally());
	}
}

function* createCurrency({ currency }) {
	const document = { ...currency };

	try {
		const newCurrency = yield (yield call(
			api.post,
			'/money/currency/',
			document,
		)).json();

		yield put(actions.createCurrencyDone(newCurrency));
		yield put(actions.fetchAllCurrencies(`/__FILL_IN__/${newCurrency.id}/`));
	} catch (e) {
		yield put(actions.createCurrencyFailed(currency, cleanErrorMessage(e)));
	} finally {
		yield put(actions.createCurrencyFinally());
	}
}

function* updateCurrency({ currency }) {
	const document = { ...currency };

	try {
		const newCurrency = yield (yield call(
			api.put,
			`/money/currency/${currency.id}/`,
			document,
		)).json();

		yield put(actions.updateCurrencyDone(newCurrency));
		yield put(actions.fetchAllCurrencies(`/__FILL_IN__/${newCurrency.id}/`));
	} catch (e) {
		yield put(actions.updateCurrencyFailed(currency, cleanErrorMessage(e)));
	} finally {
		yield put(actions.updateCurrencyFinally());
	}
}

function* deleteCurrency({ currency }) {
	const document = { ...currency };

	try {
		const newCurrency = yield (yield call(
			api.del,
			`/money/currency/${currency.id}/`,
			document,
		)).json();

		yield put(actions.deleteCurrencyDone(newCurrency));
		yield put(actions.fetchAllCurrencies(`/__FILL_IN__/${newCurrency.id}/`));
	} catch (e) {
		yield put(actions.deleteCurrencyFailed(currency, cleanErrorMessage(e)));
	} finally {
		yield put(actions.deleteCurrencyFinally());
	}
}

export default function* saga() {
	yield takeLatest('money/currencies/FETCH_ALL', fetchAllCurrencies);
	yield takeLatest('money/currencies/FETCH', fetchCurrency);
	yield takeEvery('money/currencies/CREATE', createCurrency);
	yield takeEvery('money/currencies/UPDATE', updateCurrency);
	yield takeEvery('money/currencies/DELETE', deleteCurrency);
}
