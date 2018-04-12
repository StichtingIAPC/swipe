import {ARE_YOU_SURE_ACTION, areYouSureAction} from "../ui/actions";

export const AUTH_LOGIN_START = 'auth/login/start';
export const AUTH_LOGIN_RESTORE_START = 'auth/login/restore/start';
export const AUTH_LOGIN_SUCCESS = 'auth/login/success';
export const AUTH_LOGIN_FAIL = 'auth/login/fail';

export const AUTH_LOGOUT_START = 'auth/logout/start';
export const AUTH_LOGOUT_SUCCESS = 'auth/logout/success';
export const AUTH_LOGOUT_FAIL = 'auth/logout/fail';

export const AUTH_SET_TOKEN = 'auth/setToken';
export const AUTH_SET_ROUTE_AFTER_AUTH = 'auth/setRouteAfterAuth';

export function startLogin(username, password) {
	return {
		type: 'AUTH_START_LOGIN',
		username,
		password,
	};
}

export const loginRestore = loginAction => ({
	type: AUTH_LOGIN_RESTORE_START,
	loginAction,
});

export const loginError = error => ({
	type: AUTH_LOGIN_FAIL,
	error,
});

export function directLogout() {
	return { type: 'AUTH_START_LOGOUT' };
}

export function logout() {
	return areYouSureAction(directLogout(), "Are you sure you want to log out?", "Logout succesful!", "");
}

export function logoutSuccess() {
	return {
		type: 'AUTH_LOGOUT_SUCCESS',
	};
}

export const logoutError = error => ({
	type: AUTH_LOGOUT_FAIL,
	error,
});

export const setAuthToken = token => ({
	type: AUTH_SET_TOKEN,
	token,
});

export const setRouteAfterAuthentication = route => ({
	type: AUTH_SET_ROUTE_AFTER_AUTH,
	route,
});

