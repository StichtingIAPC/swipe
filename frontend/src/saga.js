import { takeEvery } from 'redux-saga';
import { login } from './sagas/auth.js';

export default function* rootSaga() {
	yield takeEvery('AUTH_START_LOGIN', login);
};
