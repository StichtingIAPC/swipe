import {
	ADD_SUPPLIER,
	FETCH_SUPPLIER,
	FETCH_SUPPLIERS,
	INVALIDATE_SUPPLIERS,
	PUT_SUPPLIER,
	RECEIVE_SUPPLIERS,
	REMOVE_SUPPLIER,
	UPDATE_SUPPLIER,
} from '../actions/suppliers'

/**
 * Created by Matthias on 18/11/2016.
 */

function handleSupplier({objects, ...rest}, action) {
	let objs;
	switch (action.type) {
	case ADD_SUPPLIER:
		if (!action.supplier.id) {
			action.supplier.id = Math.max(0, ...Object.values(objects).map((supplier) => supplier.id)) + 1;
		}
		return {
			...rest,
			objects: {
				...objects,
				[action.supplier.id]: action.supplier,
			},
		};
	case FETCH_SUPPLIER:
	case PUT_SUPPLIER:
		return {
			...rest,
			objects: {
				...objects,
				[action.id]: {
					...objects[action.id],
					updating: true,
				},
			},
		};
	case REMOVE_SUPPLIER:
		objs = {...objects};
		delete objs[action.id];
		return {
			...rest,
			objects: objs,
		};
	case UPDATE_SUPPLIER:
		objs = {...objects};
		objs[action.supplier.id] = action.supplier;
		return {
			...rest,
			objects: objs,
		};
	default:
		return {...rest, objects};
	}
}

function handleSuppliers(state, action) {
	switch (action.type) {
	case FETCH_SUPPLIERS:
		return {
			...state,
			fetching: true,
		};
	case INVALIDATE_SUPPLIERS:
		return {
			...state,
			invalid: true,
			error: (action.error ? action.error : state.error),
		};
	case RECEIVE_SUPPLIERS:
		return {
			objects: action.suppliers,
			fetching: false,
			invalid: false,
			lastModified: action.date,
			error: null,
		};
	default:
		return state
	}
}

export function suppliers(state = {
	objects: {},
	fetching: false,
	invalid: false,
}, action) {
	let objs;
	switch (action.type) {
	case ADD_SUPPLIER:
	case FETCH_SUPPLIER:
	case PUT_SUPPLIER:
	case REMOVE_SUPPLIER:
	case UPDATE_SUPPLIER:
		return handleSupplier(state, action);
	case FETCH_SUPPLIERS:
	case INVALIDATE_SUPPLIERS:
	case RECEIVE_SUPPLIERS:
		return handleSuppliers(state, action);
	default:
		return state;
	}
}

export default suppliers;
