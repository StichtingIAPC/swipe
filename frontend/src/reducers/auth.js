const initialState = {
	currentUser: null,
	loading: false,
	error: null,
	token: null,
	nextRoute: '/',
};

export default function authenticationReducer(state = initialState, action) {
	if (action.type === 'AUTH_SET_ROUTE_AFTER_AUTH') return { ...state, nextRoute: action.route };
	if (action.type === 'AUTH_START_LOGIN') return { ...state, loading: true };
	if (action.type === 'AUTH_LOGIN_SUCCESS') return { ...state, token: action.token, loading: false, currentUser: action.user };
	if (action.type === 'AUTH_LOGIN_ERROR') return { ...state, token: null, loading: false, error: action.error, currentUser: null };
	if (action.type === 'AUTH_LOGIN_RESET') return { ...state, token: null, error: null, currentUser: null };
	return state;
}
