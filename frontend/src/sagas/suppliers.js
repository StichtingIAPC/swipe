import {call, put} from "redux-saga/effects";
import {push} from "react-router-redux";
import {receiveSuppliers, invalidateSuppliers, addSupplier, changeSupplier} from "../actions/suppliers";
import {get, post, patch} from "../api";

export function* populateSuppliers() {
	try {
		const data = yield (yield call(
			get,
			'/supplier/',
		)).json();
		yield put(receiveSuppliers(data));
	}	catch (e) {
		yield put(invalidateSuppliers(e));
	}
}

export function* createSupplier({ suppl }) {
	const supplier = {
		...suppl,
		search_url: suppl.searchUrl, // fix for diff in python naming vs JS naming
	};
	try {
		const data = yield (yield call(
			post,
			'/supplier/',
			supplier,
		)).json();
		yield put(addSupplier(data));
		yield put(push(`/supplier/${data.id}/`));
	} catch (e) {
		yield put(invalidateSuppliers(e));
	}
}

export function* updateSupplier({ suppl }) {
	const supplier = {
		...suppl,
		search_url: suppl.searchUrl,
	};
	try {
		const data = yield (yield call(
			patch,
			`/supplier/${supplier.id}/`,
			supplier,
		)).json();
		yield put(changeSupplier(data));
		yield put(push(`/supplier/${data.id}/`))
	} catch (e) {
		yield put(invalidateSuppliers(e));
	}
}


