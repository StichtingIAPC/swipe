import { combineReducers } from 'redux';
import { booleanField, reSetField } from '../tools/subReducers';

export default combineReducers({
	VATs: (state = [], action) => {
		if (action.type === 'VAT_FETCH_DONE')			{
			return action.VATs.map(
				VAT => ({
					...VAT,
					vatperiod_set: VAT.vatperiod_set.sort((a, b) => new Date(a.begin_date).getTime() - new Date(b.begin_date).getTime()),
				})
			);
		}
		return state;
	},
	fetching: booleanField({
		VAT_FETCH_START: true,
		VAT_FETCH_DONE: false,
		VAT_FETCH_ERROR: false,
	}, false),
	fetchError: reSetField('VAT_FETCH_ERROR', 'VAT_FETCH_DONE', null, 'error'),
	inputError: reSetField('VAT_INPUT_ERROR', 'VAT_FETCH_START', null, 'error'),
	populated: booleanField({ VAT_FETCH_DONE: true }, false),
});
