import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import * as actions from './actions.js';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';
import * as api from '../../../api';

function* fetchAllvats({ redirectTo }) {
	try {
		const vats = yield (yield call(
			api.get,
			'/money/vat/',
		)).json();

		yield put(actions.fetchAllvatsDone(vats));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		yield put(actions.fetchAllvatsFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchAllvatsFinally());
	}
}

function* fetchvat({ id }) {
	try {
		const newvat = yield (yield call(
			api.get,
			`/money/vat/${id}`,
		)).json();

		yield put(actions.fetchvatDone(newvat));
	} catch (e) {
		yield put(actions.fetchvatFailed(id, cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchvatFinally());
	}
}

function* createvat({ vat }) {
	const document = { ...vat };

	try {
		const newvat = yield (yield call(
			api.post,
			'/money/vat/',
			document,
		)).json();

		yield put(actions.createvatDone(newvat));
		yield put(actions.fetchAllvats(`/money/vat/${newvat.id}/`));
	} catch (e) {
		yield put(actions.createvatFailed(vat, cleanErrorMessage(e)));
	} finally {
		yield put(actions.createvatFinally());
	}
}

function* updatevat({ vat }) {
	const document = { ...vat };

	try {
		const newvat = yield (yield call(
			api.put,
			`/money/vat/${vat.id}/`,
			document,
		)).json();

		yield put(actions.updatevatDone(newvat));
		yield put(actions.fetchAllvats(`/money/vat/${newvat.id}/`));
	} catch (e) {
		yield put(actions.updatevatFailed(vat, cleanErrorMessage(e)));
	} finally {
		yield put(actions.updatevatFinally());
	}
}

function* deletevat({ vat }) {
	const document = { ...vat };

	try {
		const newvat = yield (yield call(
			api.del,
			`/money/vat/${vat.id}/`,
			document,
		)).json();

		yield put(actions.deletevatDone(newvat));
		yield put(actions.fetchAllvats(`/money/vat/${newvat.id}/`));
	} catch (e) {
		yield put(actions.deletevatFailed(vat, cleanErrorMessage(e)));
	} finally {
		yield put(actions.deletevatFinally());
	}
}

export default function* saga() {
	yield takeLatest('money/vats/FETCH_ALL', fetchAllvats);
	yield takeLatest('money/vats/FETCH', fetchvat);
	yield takeEvery('money/vats/CREATE', createvat);
	yield takeEvery('money/vats/UPDATE', updatevat);
	yield takeEvery('money/vats/DELETE', deletevat);
}
