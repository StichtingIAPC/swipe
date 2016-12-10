import {call, put} from "redux-saga/effects";
import {push} from "react-router-redux";
import fetch from "isomorphic-fetch";
import {receiveSuppliers, invalidateSuppliers, addSupplier, changeSupplier} from "../actions/suppliers";
import config from "../config";

export function* populateSuppliers() {
	try {
		const data = yield (yield call(
			fetch,
			config.baseurl + '/supplier/',
			{
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
				},
			}
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
			fetch,
			config.baseurl + '/supplier/',
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(supplier),
			}
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
			fetch,
			config.baseurl + `/supplier/${supplier.id}/`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(supplier),
			}
		)).json();
		yield put(changeSupplier(data));
		yield put(push(`/supplier/${data.id}/`))
	} catch (e) {
		yield put(invalidateSuppliers(e));
	}
}


