import { combineReducers } from 'redux';
import * as actions from './actions';
import {
	booleanControlReducer,
	collectReducers,
	objectControlReducer,
	resetFieldReducer,
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
		actions.ASSORTMENT_ARTICLES_FETCH_ALL_SUCCESS,
	], [], 'articles'),
	activeObject: collectReducers(
		resetFieldReducer([
			actions.ASSORTMENT_ARTICLES_NEW_ARTICLE,
		], defaultArticle),
		objectControlReducer([
			actions.ASSORTMENT_ARTICLES_SET_FIELD,
		], defaultArticle),
		setFieldReducer([
			actions.ASSORTMENT_ARTICLES_FETCH_SUCCESS,
		], defaultArticle, 'article'),
	),
	loading: booleanControlReducer({
		[actions.ASSORTMENT_ARTICLES_FETCH_ALL_START]: true,
		[actions.ASSORTMENT_ARTICLES_FETCH_ALL_FINALLY]: false,
	}, false),
	populated: booleanControlReducer({
		[actions.ASSORTMENT_ARTICLES_FETCH_ALL_SUCCESS]: true,
	}, false),
	error: setFieldReducer([
		actions.ASSORTMENT_ARTICLES_FETCH_ALL_FAIL,
		actions.ASSORTMENT_ARTICLES_FETCH_FAIL,
		actions.ASSORTMENT_ARTICLES_CREATE_FAIL,
		actions.ASSORTMENT_ARTICLES_UPDATE_FAIL,
		actions.ASSORTMENT_ARTICLES_DELETE_FAIL,
	], null, 'reason'),
});
