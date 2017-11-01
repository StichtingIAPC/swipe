import { combineReducers } from 'redux';

import articles from './articles/reducer.js';
import labelTypes from './label-types/reducer.js';
import unitTypes from './unit-types/reducer.js';

export default combineReducers({
	articles,
	labelTypes,
	unitTypes,
});
