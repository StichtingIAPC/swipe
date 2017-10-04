import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { get, post, put as api_put } from '../../../api.js';
import {
	doneFetchingUnitTypes,
	startFetchingUnitTypes,
	unitTypeFetchError,
	unitTypeInputError,
} from '../../../state/assortment/unit-types/actions';

function* fetchUnitTypes({ redirectTo } = {}) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/assortment/unittypes/',
		)).json();

		yield put(doneFetchingUnitTypes(data));
		if (redirectTo)
			yield put(push(redirectTo));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(unitTypeFetchError(msg));
	}
}

function* createUnitType({ unitType } = {}) {
	const document = { ...unitType };
	let msg = null;

	try {
		const data = yield (yield call(
			post,
			'/assortment/unittypes/',
			document
		)).json();

		yield put(startFetchingUnitTypes({ redirectTo: `/assortment/unittypes/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(unitTypeInputError(msg));
	}
}

function* updateUnitType({ unitType }) {
	const document = { ...unitType };
	let msg = null;

	try {
		const data = yield (yield call(
			api_put,
			`/assortment/unittypes/`,
			document,
		)).json();

		yield put(startFetchingUnitTypes({ redirectTo: `/assortment/unittypes/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(unitTypeInputError(msg));
	}
}


export default function* () {
	yield takeLatest('UNIT_TYPE_FETCH_START', fetchUnitTypes);
	yield takeEvery('UNIT_TYPE_CREATE', createUnitType);
	yield takeEvery('UNIT_TYPE_UPDATE', updateUnitType);
}
