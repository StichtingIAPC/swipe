const initialState = {
	articles: null,
	fetching: false,
	fetchError: null,
	inputError: null,
};

export default function articleReducer(state = initialState, action) {
	if (action.type === 'ARTICLE_FETCH_START') {
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === 'ARTICLE_FETCH_DONE') {
		return {
			...state,
			fetching: false,
			articles: action.articles,
			fetchError: null,
			populated: true,
		};
	}
	if (action.type === 'ARTICLE_INPUT_ERROR') {
		return {
			...state,
			inputError: action.error,
		};
	}
	if (action.type === 'ARTICLE_FETCH_ERROR') {
		return {
			...state,
			fetchError: action.error,
			fetching: false,
		};
	}
	return state;
}
