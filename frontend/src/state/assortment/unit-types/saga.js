import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import * as actions from './actions.js';
import * as api from '../../../api';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';

function* fetchAllUnitTypes({ redirectTo }) {
	try {
		const unitTypes = yield (yield call(
			api.get,
			'/assortment/unittypes/',
		)).json();

		yield put(actions.fetchAllUnitTypesDone(unitTypes));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		yield put(actions.fetchAllUnitTypesFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchAllUnitTypesFinally());
	}
}

function* fetchUnitType({ id }) {
	try {
		const newUnitType = yield (yield call(
			api.get,
			`/assortment/unittypes/${id}`,
		)).json();

		yield put(actions.fetchUnitTypeDone(newUnitType));
	} catch (e) {
		yield put(actions.fetchUnitTypeFailed(id, e));
	} finally {
		yield put(actions.fetchUnitTypeFinally());
	}
}

function* createUnitType({ unitType }) {
	const document = { ...unitType };

	try {
		const newUnitType = yield (yield call(
			api.post,
			'/assortment/unittypes/',
			document,
		)).json();

		yield put(actions.createUnitTypeDone(newUnitType));
		yield put(actions.fetchAllUnitTypes(`/assortment/`));
	} catch (e) {
		yield put(actions.createUnitTypeFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.createUnitTypeFinally());
	}
}

function* updateUnitType({ unitType }) {
	const document = { ...unitType };

	try {
		const newUnitType = yield (yield call(
			api.put,
			`/assortment/unittypes/${unitType.id}/`,
			document,
		)).json();

		yield put(actions.updateUnitTypeDone(newUnitType));
		yield put(actions.fetchAllUnitTypes(`/assortment/`));
	} catch (e) {
		yield put(actions.updateUnitTypeFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.updateUnitTypeFinally());
	}
}

function* deleteUnitType({ unitType }) {
	const document = { ...unitType };

	try {
		const newUnitType = yield (yield call(
			api.del,
			`/assortment/unittypes/${unitType.id}/`,
			document,
		)).json();

		yield put(actions.deleteUnitTypeDone(newUnitType));
		yield put(actions.fetchAllUnitTypes(`/assortment/`));
	} catch (e) {
		yield put(actions.deleteUnitTypeFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.deleteUnitTypeFinally());
	}
}

export default function* saga() {
	yield takeLatest('assortment/unit-types/FETCH_ALL', fetchAllUnitTypes);
	yield takeLatest('assortment/unit-types/FETCH', fetchUnitType);
	yield takeEvery('assortment/unit-types/CREATE', createUnitType);
	yield takeEvery('assortment/unit-types/UPDATE', updateUnitType);
	yield takeEvery('assortment/unit-types/DELETE', deleteUnitType);
}
