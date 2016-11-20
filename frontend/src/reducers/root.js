import { combineReducers } from 'redux'

import suppliers from './suppliers';
import auth from './auth';

/**
 * Created by Matthias on 18/11/2016.
 */

export const swipeApp = combineReducers({
	suppliers,
	auth,
});

export default swipeApp;
