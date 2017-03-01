import { combineReducers } from "redux";
import { routerReducer } from "react-router-redux";
import suppliers from "./suppliers";
import auth from "./auth";
import sidebar from "./sidebar";
import currencies from "./money/currencies";
import VATs from "./money/VATs";
import accountingGroups from "./money/accountingGroups";

export default combineReducers({
	suppliers,
	auth,
	routing: routerReducer,
	sidebar,
	currencies,
	accountingGroups,
	VATs,
});
