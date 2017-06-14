import { call, put } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { get, post, put as api_put } from '../../api';
import {
	doneFetchingUnitTypes,
	startFetchingUnitTypes,
	unitTypeFetchError,
	unitTypeInputError
} from '../../actions/assortment/unitTypes';

export function* fetchUnitTypes({ redirectTo } = {}) {
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

export function* createUnitType({ unitType } = {}) {
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

export function* updateUnitType({ unitType }) {
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
