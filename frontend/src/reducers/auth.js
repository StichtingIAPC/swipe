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
	if (action.type === 'AUTH_LOGIN_RESET') {
		setToken(null);
		return {
			...state,
			token: null,
			error: null,
			currentUser: null,
		};
	}
	return state;
}
