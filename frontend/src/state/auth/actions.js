import { ARE_YOU_SURE_ACTION, areYouSureAction } from '../ui/actions';

export function startLogin(username, password) {
	return {
		type: 'AUTH_START_LOGIN',
		username,
		password,
	};
}

export function loginRestore(loginAction) {
	return {
		type: 'AUTH_LOGIN_RESTORE',
		loginAction,
	};
}

export function loginSuccess(token, user) {
	return {
		type: 'AUTH_LOGIN_SUCCESS',
		data: {
			token,
			user,
		},
	};
}

export function loginError(error) {
	return {
		type: 'AUTH_LOGIN_ERROR',
		error,
	};
}

export function directLogout() {
	return { type: 'AUTH_START_LOGOUT' };
}

export function logout() {
	return areYouSureAction(directLogout(), 'Are you sure you want to log out?', 'Logout succesful!', '');
}

export function logoutSuccess() {
	return {
		type: 'AUTH_LOGOUT_SUCCESS',
	};
}

export function logoutError(error) {
	return {
		type: 'AUTH_LOGOUT_ERROR',
		error,
	};
}

export function setAuthToken(token) {
	return {
		type: 'AUTH_SET_TOKEN',
		token,
	};
}

export function setRouteAfterAuthentication(route) {
	return {
		type: 'AUTH_SET_ROUTE_AFTER_AUTH',
		route,
	};
}
