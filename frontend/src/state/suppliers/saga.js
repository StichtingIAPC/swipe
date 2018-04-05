import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import * as actions from './actions.js';
import * as api from './api';
import { cleanErrorMessage } from '../../tools/sagaHelpers';

function* fetchAllSuppliers({ redirectTo }) {
	try {
		const suppliers = yield (yield call(api.getAll)).json();

		yield put(actions.fetchAllSuppliersDone(suppliers));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		yield put(actions.fetchAllSuppliersFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchAllSuppliersFinally());
	}
}

function* fetchSupplier({ id }) {
	try {
		const newSupplier = yield (yield call(api.get, id)).json();

		yield put(actions.fetchSupplierDone(newSupplier));
	} catch (e) {
		yield put(actions.fetchSupplierFailed(id, cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchSupplierFinally());
	}
}

function* createSupplier({ supplier }) {
	const document = { ...supplier };

	try {
		const newSupplier = yield (yield call(api.post, document)).json();

		yield put(actions.createSupplierDone(newSupplier));
		yield put(actions.fetchAllSuppliers(`/supplier/${newSupplier.id}/`));
	} catch (e) {
		yield put(actions.createSupplierFailed(supplier, cleanErrorMessage(e)));
	} finally {
		yield put(actions.createSupplierFinally());
	}
}

function* updateSupplier({ supplier }) {
	const document = { ...supplier };

	try {
		const newSupplier = yield (yield call(api.put, supplier.id, document)).json();

		yield put(actions.updateSupplierDone(newSupplier));
		yield put(actions.fetchAllSuppliers(`/supplier/${newSupplier.id}/`));
	} catch (e) {
		yield put(actions.updateSupplierFailed(supplier, cleanErrorMessage(e)));
	} finally {
		yield put(actions.updateSupplierFinally());
	}
}

function* deleteSupplier({ supplier }) {
	const document = { ...supplier };

	try {
		const newSupplier = yield (yield call(api.del, supplier.id, document)).json();

		yield put(actions.deleteSupplierDone(newSupplier));
		yield put(actions.fetchAllSuppliers(`/supplier/${newSupplier.id}/`));
	} catch (e) {
		yield put(actions.deleteSupplierFailed(supplier, cleanErrorMessage(e)));
	} finally {
		yield put(actions.deleteSupplierFinally());
	}
}

export default function* saga() {
	yield takeLatest('suppliers/FETCH_ALL', fetchAllSuppliers);
	yield takeLatest('suppliers/FETCH', fetchSupplier);
	yield takeEvery('suppliers/CREATE', createSupplier);
	yield takeEvery('suppliers/UPDATE', updateSupplier);
	yield takeEvery('suppliers/DELETE', deleteSupplier);
}
