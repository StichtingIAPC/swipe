import { call, put, select } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { loginSuccess, loginError, setRouteAfterAuthentication } from '../actions/auth.js';
import config from '../config.js';
import fetch from 'isomorphic-fetch';

export function* login({ username, password }) {
	const form = new FormData();
	form.append('username', username);
	form.append('password', password);
	try {
		const data = yield (yield call(fetch, config.baseurl + '/auth/login/', {
			method: 'POST',
			body: form,
		})).json();

		yield put(loginSuccess(data.token, data.user));

		const nextRoute = yield select(state => state.auth.nextRoute);
		console.log('nextRoute', nextRoute);
		if (nextRoute != null) {
			yield put(push(nextRoute));
			yield put(setRouteAfterAuthentication('/'));
		}
	} catch (e) {
		yield put(loginError(e));
	}
};
