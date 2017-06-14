const defaultState = {
	query: '',
	results: [],
};

export default function(state = defaultState, action) {
	if (action.type === 'REGISTER_CLIENT_SEARCH') return { ...state, query: action.query };
	if (action.type === 'REGISTER_CLIENT_SEARCH_RESULTS') return { ...state, results: action.results };
	return state;
}
