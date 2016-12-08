import * as actions from "../../actions/money/currencies";

/**
 * Created by Matthias on 26/11/2016.
 */

export function currencies(state = {
	objects: {},
	fetching: false,
	invalid: true,
	loaded: false,
}, action) {
	const {objects, ...rest} = state;
	let objs;
	switch (action.type) {
	case actions.ADD_CURRENCY:
		return {
			...rest,
			objects: {
				...objects,
				[action.currency.iso]: {...action.currency},
			},
		};
	case actions.CHANGE_CURRENCY:
		return {
			...rest,
			objects: {
				...objects,
				[action.currency.iso]: {...action.currency},
			},
		};
	case actions.INVALIDATE_CURRENCIES:
		return {
			...state,
			invalid: true,
		};
	case actions.MARK_CURRENCY_AS_UPDATING:
		return {
			...rest,
			objects: {
				...objects,
				[action.iso]: {...objects[action.iso], updating: true},
			},
		};
	case actions.RECEIVE_CURRENCIES:
		objs = {};
		for (const currency of action.currencies) {
			objs[currency.iso] = {...currency};
		}
		return {
			objects: objs,
			fetching: false,
			invalid: false,
			loaded: true,
		};
	case actions.REMOVE_CURRENCY:
		objs = {...objects};
		delete objs[action.iso];
		return {
			...rest,
			objects: objs,
		};
	case actions.START_FETCH_CURRENCIES:
		return {
			...state,
			fetching: true,
		};
	default:
		return state;
	}
}

export default currencies;
