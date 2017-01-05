import { call, put } from "redux-saga/effects";
import { push } from "react-router-redux";
import { get, post, put as api_put } from "../api";
import { startFetchingSuppliers, doneFetchingSuppliers } from "../actions/suppliers";

function renameProp(item, original, target) {
	const newitem = { ...item };
	newitem[target] = newitem[original];
	delete newitem[original];
	return newitem;
}

export function* fetchSuppliers() {
	try {
		const data = yield (yield call(
			get,
			'/supplier/',
		)).json();
		yield put(doneFetchingSuppliers(data.map(s => renameProp(s, 'search_url', 'searchUrl'))));
	}	catch (e) {
		// TODO: error handling
		//yield put(invalidateSuppliers(e));
	}
}

export function* createSupplier({ supplier }) {
	// Fix for diff in python naming vs JS naming
	const document = { ...supplier, search_url: supplier.searchUrl };
	delete document['searchUrl'];

	try {
		const data = yield (yield call(
			post,
			'/supplier/',
			document,
		)).json();

		// Routing over here is ugly, since that couples UI with business logic,
		// but I also do not know of a better way currently...
		yield put(startFetchingSuppliers());
		yield put(push(`/supplier/${data.id}/`));
	} catch (e) {
		// TODO: error handling
		//yield put(invalidateSuppliers(e));
	}
}

export function* updateSupplier({ supplier }) {
	// Fix for diff in python naming vs JS naming
	const document = { ...supplier, search_url: supplier.searchUrl };
	delete document['searchUrl'];

	try {
		const data = yield (yield call(
			api_put,
			`/supplier/${supplier.id}/`,
			supplier,
		)).json();

		yield put(startFetchingSuppliers())
		yield put(push(`/supplier/${data.id}/`))
	} catch (e) {
		// TODO: error handling
		//yield put(invalidateSuppliers(e));
	}
}
