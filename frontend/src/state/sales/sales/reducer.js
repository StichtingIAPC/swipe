import {SALES_ADD_PRODUCT} from "./actions";
const initialState = {
	sales: [],
};

export default function salesReducer(state = initialState, action) {
	if (action.type === SALES_ADD_PRODUCT) {
		const salesLine = state.sales.find(art => art.id === action.article.id);
		const newCount = Math.min(Math.max(0, (salesLine ? salesLine.count : 0) + action.count), action.currentAmount);

		if (salesLine) {
			return {
				...state, sales: state.sales.map(art => (art.id === action.article.id) ? { ...art, count: newCount } : art),
			};
		}
		return {
			...state, sales: state.sales.concat([{ ...action.article, count: newCount }]),
		};
	}
	return state;
}
