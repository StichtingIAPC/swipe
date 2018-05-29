import { call, put, takeEvery, select } from 'redux-saga/effects';


import * as api from './api';
import * as actions from './actions';
import { getCustomerListIsLoading } from './selectors';

function* fetchAll() {
	if (yield select(getCustomerListIsLoading)) {
		return;
	}
	try {
		yield put(actions.fetchCustomersIsLoading());
		const customers = yield (yield call(api.getAll)).json();
		yield put(actions.fetchCustomersSuccess(customers));
	} catch (e) {
		console.error(e);
		yield put(actions.fetchCustomersError(e));
	} finally {
		yield put(actions.fetchCustomersFinally());
	}
}


export default function* saga() {
	yield takeEvery(actions.FETCH_CUSTOMERS_ACTION, fetchAll);
}
