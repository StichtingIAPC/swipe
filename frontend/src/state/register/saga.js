import paymentTypeSaga from './payment-types/saga';
import registerSaga from './registers/saga';
import { call, put } from 'redux-saga/effects';
import { get } from '../../api';
import { doneFetchingRegisterOpen, errorFetchingRegisterOpen } from './actions';


function* festchRegisterOpen() {
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
	yield* festchRegisterOpen();
}
