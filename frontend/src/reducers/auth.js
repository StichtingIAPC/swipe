import { setToken } from '../api';
const initialState = {
	currentUser: null,
	loading: false,
	error: null,
	token: null,
	nextRoute: '/',
};

export default function authenticationReducer(state = initialState, action) {
	if (action.type === 'AUTH_SET_ROUTE_AFTER_AUTH') 		{
		return {
			...state,
			nextRoute: action.route,
		};
	}
	if (action.type === 'AUTH_START_LOGIN') 		{
		return {
			...state,
			loading: true,
		};
	}
	if (action.type === 'AUTH_LOGIN_SUCCESS') {
		setToken(action.token);
		return {
			...state,
			token: action.token,
			loading: false,
			currentUser: action.user,
		};
	}
	if (action.type === 'AUTH_LOGIN_ERROR') {
		setToken(null);
		return {
			...state,
			token: null,
			loading: false,
			error: action.error,
			currentUser: null,
		};
	}
	if (action.type === 'AUTH_START_LOGOUT') {
		return {
			...state,
			loading: true,
		};
	}
	if (action.type === 'AUTH_LOGOUT_SUCCESS') {
		setToken(null);
		return {
			...state,
			token: null,
			currentUser: null,
			loading: false,
		};
	}
	if (action.type === 'AUTH_LOGOUT_ERROR') {
		return {
			...state,
			error: action.error,
			loading: false,
		};
	}
	return state;
}
