import { combineReducers } from 'redux';
import {
	setFieldReducer,
	resetFieldReducer,
} from '../../../tools/reducerComponents';

import { crudReducers } from '../../../tools/CRUDHelper';
import actions from './actions';

export default crudReducers('logistics/externalize', 'currentItem', 'items');
