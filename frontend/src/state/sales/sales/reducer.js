const initialState = {
	sales: [],

};

export default function salesReducer(state = initialState, action) {
	if (action.type === 'SALES_ADD_PRODUCT'){
		let a = state.sales.find(art => art.id === action.article.id);
		if (a) {
			return {
				...state, sales: state.sales.map(art => (art.id === action.article.id) ? {...art, count: art.count + action.article.count} : art),
			};
		}
		return {
			...state, sales: state.sales.concat([action.article]),
		};
	}
	return state;
}
