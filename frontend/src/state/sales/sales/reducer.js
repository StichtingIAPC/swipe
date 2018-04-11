import { SALES_MUTATE_SALES_LINE } from './actions';
const initialState = [];

export default function salesReducer(state = initialState, action) {
	if (action.type === SALES_MUTATE_SALES_LINE) {
		const salesLine = state.find(art => art.id === action.article.id);
		let newAmount;
		const proposedAmount = (salesLine ? salesLine.count : 0) + action.amount;

		if (action.amount >= 0) {
			newAmount = Math.min(proposedAmount, action.article.count);
		} else {
			newAmount = Math.max(proposedAmount, 0);
		}

		if (salesLine) {
			if (newAmount <= 0) {
				return state.filter(art => art.id !== action.article.id);
			}
			return state.map(art => {
				if (art.id === action.article.id) {
					return {
						...art,
						count: newAmount,
					};
				}
				return art;
			});
		}
		return state.concat([{
			...action.article,
			count: newAmount,
		}]);
	}
	return state;
}
