import { call, put, select } from 'redux-saga/effects';

import { cleanErrorMessage } from '../../../tools/sagaHelpers';
import * as api from '../../../api';
import { SALES_COMMIT_CREATE, salesCommitCreateDone, salesCommitCreateFailed, salesCommitCreateFinally } from './actions';
import { takeEvery } from 'redux-saga';
import { getPaymentsOnReceiptAsListForAPI } from '../payments/selectors';
import { getSales } from '../sales/selectors';
import { getCurrentUser } from '../../auth/selectors';

function* createSalesTransaction() {
	const document = {
		payments: yield select(getPaymentsOnReceiptAsListForAPI),
		transactionlines: yield select(getSales),
		user: (yield select(getCurrentUser)).id,
	};

	try {
		const result = yield (yield call(
			api,
			'POST',
			'/sales/transactions/create/',
			document,
		)).json();

		yield put(salesCommitCreateDone(result));
	} catch (e) {
		yield put(salesCommitCreateFailed(document, cleanErrorMessage(e)));
	} finally {
		yield put(salesCommitCreateFinally());
	}
}

export default function* saga() {
	yield takeEvery(SALES_COMMIT_CREATE, createSalesTransaction);
}
