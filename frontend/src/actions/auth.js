export function startLogin(username, password) {
	return {
		type: 'AUTH_START_LOGIN',
		username,
		password,
	};
}

export function loginSuccess(token, user) {
	return {
		type: 'AUTH_LOGIN_SUCCESS',
		token,
		user,
	};
}

export function loginError(error) {
	return {
		type: 'AUTH_LOGIN_ERROR',
		error,
	};
}

export function logout() {
	return { type: 'AUTH_START_LOGOUT' };
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

export function setRouteAfterAuthentication(route) {
	return {
		type: 'AUTH_SET_ROUTE_AFTER_AUTH',
		route,
	};
}
