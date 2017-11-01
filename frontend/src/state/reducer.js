import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';

import assortment from './assortment/reducer.js';
import auth from './auth/reducer.js';
import money from './money/reducer.js';
import register from './register/reducer.js';
import sidebar from './sidebar/reducer.js';
import suppliers from './suppliers/reducer.js';

export default combineReducers({
	routing: routerReducer,
	assortment,
	auth,
	money,
	register,
	sidebar,
	suppliers,
});
