import { combineReducers } from 'redux'

import { routerReducer } from 'react-router-redux';

import suppliers from './suppliers';
import auth from './auth';

export default combineReducers({
	suppliers,
	auth,
	routing: routerReducer,
});
