import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';

import assortment from './assortment/reducer.js';
import auth from './auth/reducer.js';
import money from './money/reducer.js';
import register from './register/reducer.js';
import sidebar from './sidebar/reducer.js';
import suppliers from './suppliers/reducer.js';
import sales from './sales/reducer.js';
import stock from './stock/reducer.js';
import logistics from './logistics/reducer.js';
import crm from './crm/reducer.js';

export default combineReducers({
	routing: routerReducer,
	assortment,
	auth,
	money,
	register,
	sidebar,
	suppliers,
	sales,
	stock,
	logistics,
	crm,
});
