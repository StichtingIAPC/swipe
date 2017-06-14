import { combineReducers } from 'redux';
import step from './register/step.js';
import client from './register/client.js';
import clientSearch from './register/clientSearch.js';

export default combineReducers({
	step,
	client,
	clientSearch,
});
