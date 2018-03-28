import paymentTypeSaga from './payment-types/saga';
import registerSaga from './registers/saga';
import { call, put, takeLatest } from 'redux-saga/effects';
import { get } from '../../api';
import { doneFetchingRegisterOpen, errorFetchingRegisterOpen } from './actions';


function* fetchRegisterOpen() {
	try {
		const data = yield (yield call(
			get,
			`/register/opened/`,
		)).json();

		yield put(doneFetchingRegisterOpen(data !== null && data.length !== 0));
	} catch (e) {
		yield put(errorFetchingRegisterOpen());
	}
}


export default function* saga() {
	yield* paymentTypeSaga();
	yield* registerSaga();
	yield takeLatest('REGISTER_OPEN_FETCH_START', fetchRegisterOpen);
}
