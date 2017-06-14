import { combineReducers } from "redux";
import { routerReducer } from "react-router-redux";
import articles from "./articles";
import suppliers from "./suppliers";
import auth from "./auth";
import sidebar from "./sidebar";
import currencies from "./money/currencies";
import VATs from "./money/VATs";
import accountingGroups from "./money/accountingGroups";
import labelTypes from "./assortment/labelTypes";
import unitTypes from "./assortment/unitTypes";
import registers from "./register/registers";
import paymentTypes from "./register/paymentTypes";
import closedRegisterCounts from "./register/closedRegisterCounts";
import openRegisterCounts from "./register/openRegisterCounts";

export default combineReducers({
	accountingGroups,
	articles,
	auth,
	currencies,
	labelTypes,
	paymentTypes,
	registers,
	routing: routerReducer,
	sidebar,
	suppliers,
	unitTypes,
	VATs,
	closedRegisterCounts,
	openRegisterCounts,
});
