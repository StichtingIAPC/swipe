import { combineReducers } from 'redux';
import {
	booleanControlReducer, collectReducers, resetFieldReducer,
	setFieldReducer
} from '../../tools/reducerComponents';

const initialState = {
	currentUser: null,
	loading: false,
	error: null,
	token: null,
	nextRoute: '/',
};

// export default function TODO(state = initialState, action) {
// 	if (action.type === 'AUTH_LOGIN_SUCCESS') {
// 		setToken(action.data.token);
// 	}
// 	if (action.type === 'AUTH_LOGIN_ERROR') {
// 		setToken(null);
// 	}
// 	if (action.type === 'AUTH_LOGOUT_SUCCESS') {
// 		setToken(null);
// 	}
// 	if (action.type === 'AUTH_LOGOUT_ERROR') {
// 		setToken(null);
// 	}
// }

export default combineReducers({ // TODO: AUTH_LOGIN_SUCCESS: setToken(action.data.token), [AUTH_LOGIN_ERROR, AUTH_LOGOUT_*]: setToken(null)
	nextRoute: setFieldReducer([
		'AUTH_SET_ROUTE_AFTER_AUTH',
	], '/', 'route'),
	loading: booleanControlReducer({
		AUTH_START_LOGIN: true,
		AUTH_LOGIN_SUCCESS: false,
		AUTH_LOGIN_ERROR: false,
		AUTH_START_LOGOUT: true,
		AUTH_LOGOUT_SUCCESS: false,
		AUTH_LOGOUT_ERROR: false,
	}, false),
	token: collectReducers(
		resetFieldReducer([
			'AUTH_LOGIN_ERROR',
			'AUTH_LOGOUT_SUCCESS',
			'AUTH_LOGOUT_ERROR',
		], null),
		setFieldReducer([
			'AUTH_LOGIN_SUCCESS',
		], null, 'data.token')
	),
	currentUser: collectReducers(
		resetFieldReducer([
			'AUTH_LOGIN_ERROR',
			'AUTH_LOGOUT_SUCCESS',
			'AUTH_LOGOUT_ERROR',
		], null),
		setFieldReducer([
			'AUTH_LOGIN_SUCCESS',
		], null, 'data.user'),
	),
	error: collectReducers(
		setFieldReducer([
			'AUTH_LOGIN_ERROR',
			'AUTH_LOGOUT_ERROR',
		], null, 'error'),
		resetFieldReducer([
			'AUTH_LOGIN_SUCCESS',
			'AUTH_LOGOUT_SUCCESS',
		], null),
	),
});
