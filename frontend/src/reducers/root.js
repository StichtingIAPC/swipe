import {combineReducers} from "redux";
import {routerReducer} from "react-router-redux";
import suppliers from "./suppliers";
import auth from "./auth";
import sidebar from "./sidebar";
import currencies from "./money/currencies";
import register from "./register";

export default combineReducers({
	suppliers,
	auth,
	routing: routerReducer,
	sidebar,
	currencies,
	register,
});
