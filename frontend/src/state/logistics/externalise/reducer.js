import { combineReducers } from 'redux';
import {
	setFieldReducer,
	resetFieldReducer,
} from '../../../tools/reducerComponents';

import { crudReducers } from '../../../tools/CRUDHelper';
import actions from './actions';

const defaultExternalisation = {
	id: null,
	memo: '',
	externaliseline_set: [],
};

export default combineReducers({
	...crudReducers('logistics/externalize'),
	currentItem: resetFieldReducer([
		actions.START_NEW,
	], defaultExternalisation),
	validations: setFieldReducer([
		actions.SET_VALIDATIONS,
	], {}, 'validations'),
});
