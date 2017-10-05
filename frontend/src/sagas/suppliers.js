import { call, put } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { get, post, put as api_put } from '../api';
import {
	doneFetchingSuppliers,
	startFetchingSuppliers,
	supplierFetchError,
	supplierInputError
} from '../actions/suppliers';

function renameProp(item, original, target) {
	const newitem = { ...item };

	newitem[target] = newitem[original];
	delete newitem[original];
	return newitem;
}

export function* fetchSuppliers({ redirectTo }) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/supplier/',
		)).json();

		yield put(doneFetchingSuppliers(data.map(s => renameProp(s, 'search_url', 'searchUrl'))));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	}	catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}
		yield put(supplierFetchError(msg));
	}
}

export function* createSupplier({ supplier }) {
	// Fix for diff in python naming vs JS naming
	const document = {
		...supplier,
		search_url: supplier.searchUrl,
	};
	let msg = null;

	delete document['searchUrl'];

	try {
		const data = yield (yield call(
			post,
			'/supplier/',
			document,
		)).json();

		yield put(startFetchingSuppliers({ redirectTo: `/supplier/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}
		yield put(supplierInputError(msg));
	}
}

export function* updateSupplier({ supplier }) {
	// Fix for diff in python naming vs JS naming
	const document = {
		...supplier,
		search_url: supplier.searchUrl,
	};
	let msg = null;

	delete document['searchUrl'];

	try {
		const data = yield (yield call(
			api_put,
			`/supplier/${supplier.id}/`,
			document,
		)).json();

		yield put(startFetchingSuppliers({ redirectTo: `/supplier/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error) {
			msg = e.message;
		}
		if (e instanceof Response) {
			msg = e.json();
		}
		yield put(supplierInputError(msg));
	}
}
