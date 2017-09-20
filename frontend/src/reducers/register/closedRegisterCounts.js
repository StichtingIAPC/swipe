import { combineReducers } from 'redux';
import { booleanField, reSetField } from '../tools/subReducers';

function closedRegisterCounts(state = [], action) {
	switch (action.type) {
	case 'REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS_DONE':
		return action.registerCounts;
	case 'REGISTERCOUNT_CLOSED_UPDATE_AMOUNT':
		return state.map(rCount => {
			if (rCount.register === action.register) {
				return {
					...rCount,
					amount: action.amount,
				};
			}
			return rCount;
		});
	case 'REGISTERCOUNT_CLOSED_UPDATE_DENOM_AMOUNT':
		return state.map(rCount => {
			if (rCount.register === action.register) {
				const obj = {
					...rCount,
					denomination_counts: rCount.denomination_counts
						.filter(dCount => dCount.amount !== action.amount)
						.concat([{
							amount: action.amount,
							number: +action.number,
						}])
						.sort((a, b) => +a.amount - +b.amount),
				};

				obj.amount = obj.denomination_counts.reduce((total, dCount) => total + (+dCount.amount * dCount.number), 0);
				return obj;
			}
			return rCount;
		});
	default:
		return state;
	}
}

export default combineReducers({
	closedRegisterCounts,
	fetching: booleanField({
		REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS: true,
		REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS_DONE: false,
		REGISTERCOUNT_CLOSED_REGISTER_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('REGISTERCOUNT_CLOSED_REGISTER_FETCH_ERROR', 'REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS_DONE', null, 'error'),
	inputError: reSetField('REGISTERCOUNT_CLOSED_REGISTER_INPUT_ERROR', 'REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS', null, 'error'),
	populated: booleanField({ REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS_DONE: true }, false),
});
