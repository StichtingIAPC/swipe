import { combineReducers } from "redux";
import { routerReducer } from "react-router-redux";
import articles from "./articles";
import suppliers from "./suppliers";
import auth from "./auth";
import sidebar from "./sidebar";
import currencies from "./money/currencies";
import VATs from "./money/VATs";
import accountingGroups from "./money/accountingGroups";
import registers from "./registers";
import paymentTypes from "./paymentTypes";

export default combineReducers({
	routing: routerReducer,
	accountingGroups,
	articles,
	auth,
	currencies,
	registers,
	paymentTypes,
	sidebar,
	suppliers,
	VATs,
});
