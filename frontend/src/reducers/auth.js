import {
	LOGIN,
	LOGOUT,
	FAIL_AUTHENTICATION,
	START_AUTHENTICATION,
	STOP_AUTHENTICATION,
} from '../actions/auth';

export const AUTHENTICATING = Symbol('AUTHENTICATING');

/**
 * Created by Matthias on 18/11/2016.
 */

export function authReducer(state = {
	user: null,
	status: 'UNAUTHENTICATED',
	fails: 0,
}, action) {
	switch (action.type) {
	case LOGIN:
		return {
			...state,
			user: {
				username: action.user.username,
				gravatarUrl: action.user.gravatarUrl,
			},
			status: 'AUTHENTICATED',
			fails: 0,
		};
	case LOGOUT:
		return {
			...state,
			user: null,
			status: 'UNAUTHENTICATED',
		};
	case START_AUTHENTICATION:
		return {
			...state,
			fails: 0,
			status: AUTHENTICATING,
		};
	case STOP_AUTHENTICATION:
		return {
			...state,
			status: state.user == null ? 'AUTHENTICATED' : 'UNAUTHENTICATED',
		};
	case FAIL_AUTHENTICATION:
		return {
			...state,
			fails: state.fails + 1,
		};
	default:
		return state;
	}
}

export default authReducer;
