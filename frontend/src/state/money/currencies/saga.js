import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import * as actions from './actions.js';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';
import * as api from './api';
import { validate, validator } from '../../../tools/validations/validators';
import { select } from 'redux-saga/es/effects';

import { getCurrencyActiveObject } from './selectors';

function* fetchAllCurrencies({ redirectTo }) {
	try {
		const currencies = yield (yield call(api.getAll)).json();

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
		const newCurrency = yield (yield call(api.get, id)).json();

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
		const newCurrency = yield (yield call(api.post, document)).json();

		yield put(actions.createCurrencyDone(newCurrency));
		yield put(actions.fetchAllCurrencies(`/money/currency/${newCurrency.iso}`));
	} catch (e) {
		yield put(actions.createCurrencyFailed(currency, cleanErrorMessage(e)));
	} finally {
		yield put(actions.createCurrencyFinally());
	}
}

function* updateCurrency({ currency }) {
	const document = { ...currency };

	try {
		const newCurrency = yield (yield call(api.put, currency.iso, document)).json();

		yield put(actions.updateCurrencyDone(newCurrency));
		yield put(actions.fetchAllCurrencies(`/money/currency/${newCurrency.iso}`));
	} catch (e) {
		yield put(actions.updateCurrencyFailed(currency, cleanErrorMessage(e)));
	} finally {
		yield put(actions.updateCurrencyFinally());
	}
}

function* deleteCurrency({ currency }) {
	const document = { ...currency };

	try {
		// TODO: Check if document is really needed here
		const newCurrency = yield (yield call(api.del, currency.iso, document)).json();

		yield put(actions.deleteCurrencyDone(newCurrency));
		yield put(actions.fetchAllCurrencies(`/money/currency/${newCurrency.iso}`));
	} catch (e) {
		yield put(actions.deleteCurrencyFailed(currency, cleanErrorMessage(e)));
	} finally {
		yield put(actions.deleteCurrencyFinally());
	}
}

const validations = [
	validator('iso', 'ISO', memo => (memo.length == 3 ? null : () => ({
		type: 'error',
		text: 'ISO not 3 characters',
	}))),
	validator('name', 'Name', name => (name.length > 2 ? null : () => ({
		type: 'error',
		text: 'Currency name too short',
	}))),
	validator('digits', 'Digits', digits => (digits < 5 ? null : () => ({
		type: 'error',
		text: 'Too many digits.',
	}))),
	validator('digits', 'Digits', digits => (digits > -6 ? null : () => ({
		type: 'error',
		text: 'Too many negative digits.',
	}))),
	validator('digits', 'Digits', digits => (digits ? null : () => ({
		type: 'error',
		text: 'Not a number.',
	}))),
];

export function* moneyValidator() {
	const current = yield select(getCurrencyActiveObject);
	const res = validate(current, validations);
	yield put(actions.setValidations(res));
}

export default function* saga() {
	yield takeEvery('money/currencies/SET_FIELD', moneyValidator);

	yield takeLatest('money/currencies/FETCH_ALL', fetchAllCurrencies);
	yield takeLatest('money/currencies/FETCH', fetchCurrency);
	yield takeEvery('money/currencies/CREATE', createCurrency);
	yield takeEvery('money/currencies/UPDATE', updateCurrency);
	yield takeEvery('money/currencies/DELETE', deleteCurrency);
}
