import { combineReducers } from 'redux';

import accountingGroups from './accounting-groups/reducer.js';
import currencies from './currencies/reducer.js';
import vats from './vats/reducer.js';

export default combineReducers({
	accountingGroups,
	currencies,
	vats,
});
