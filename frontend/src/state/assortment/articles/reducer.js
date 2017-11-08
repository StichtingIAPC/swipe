import { combineReducers } from 'redux';
import { booleanControlReducer, objectControlReducer, setFieldReducer } from '../../../tools/reducerComponents';

const defaultArticle = {
	id: null,
	fixed_price: null,
	accounting_group: null,
	name: '',
	labels: [],
	ean: null,
	serial_number: false,
};

export default combineReducers({
	articles: setFieldReducer([
		'assortment/articles/FETCH_ALL_DONE',
	], [], 'articles'),
	activeObject: objectControlReducer([
		'assortment/articles/SET_FIELD',
	], defaultArticle),
	loading: booleanControlReducer({
		'assortment/articles/FETCH_ALL': true,
		'assortment/articles/FETCH_ALL_FINALLY': false,
	}, false),
	populated: booleanControlReducer({
		'assortment/articles/FETCH_ALL_DONE': true,
	}, false),
	error: setFieldReducer([
		'assortment/articles/FETCH_ALL_FAILED',
		'assortment/articles/FETCH_FAILED',
		'assortment/articles/CREATE_FAILED',
		'assortment/articles/UPDATE_FAILED',
		'assortment/articles/DELETE_FAILED',
	], null, 'reason'),
});
