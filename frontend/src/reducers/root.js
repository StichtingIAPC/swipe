import { combineReducers } from 'redux'

import { routerReducer } from 'react-router-redux';
import suppliers from './suppliers.js';
import auth from './auth.js';
import sidebar from './sidebar.js';

export default combineReducers({
	suppliers,
	auth,
	routing: routerReducer,
	sidebar,
});
