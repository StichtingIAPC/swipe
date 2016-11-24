/**
 * Created by Matthias on 18/11/2016.
 */
export const LOGIN = 'LOGIN';
export function login(user) {
	return {
		type: LOGIN,
		user: {
			username: user.username,
			gravatarUrl: user.gravatarUrl,
			permissions: user.permissions,
		},
	};
}

export const LOGOUT = 'LOGOUT';
export function logout() {
	return {
		type: LOGOUT,
	};
}

export const START_AUTHENTICATION = 'START_AUTHENTICATION';
export function startAuthentication() {
	return {
		type: START_AUTHENTICATION,
	}
}

export const STOP_AUTHENTICATION = 'STOP_AUTHENTICATION';
export function stopAuthentication() {
	return {
		type: STOP_AUTHENTICATION,
	}
}

export const FAIL_AUTHENTICATION = 'FAILED_AUTHENTICATION';
export function failAuthentication() {
	return {
		type: FAIL_AUTHENTICATION,
	}
}
