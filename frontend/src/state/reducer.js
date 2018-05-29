import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';

import assortment from './assortment/reducer';
import auth from './auth/reducer';
import money from './money/reducer';
import register from './register/reducer';
import sidebar from './sidebar/reducer';
import suppliers from './suppliers/reducer';
import sales from './sales/reducer';
import stock from './stock/reducer';
import logistics from './logistics/reducer';
import crm from './crm/reducer';

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
