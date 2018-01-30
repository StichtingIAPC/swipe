import { combineReducers } from 'redux';
import {
	booleanControlReducer, collectReducers, objectControlReducer, resetFieldReducer,
	setFieldReducer,
} from '../../../tools/reducerComponents';

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
	activeObject: collectReducers(
		resetFieldReducer([
			'assortment/articles/NEW_ARTICLE',
		], defaultArticle),
		objectControlReducer([
			'assortment/articles/SET_FIELD',
		], defaultArticle),
		setFieldReducer([
			'assortment/articles/FETCH_DONE',
		], defaultArticle, 'article'),
	),
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
