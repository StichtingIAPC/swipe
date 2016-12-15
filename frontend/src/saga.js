import {takeEvery, takeLatest} from "redux-saga";
import {login} from "./sagas/auth.js";
import {populateCurrencies, createCurrency, updateCurrency} from "./sagas/money/currencies";
import {populateSuppliers, createSupplier, updateSupplier} from "./sagas/suppliers";

export default function* rootSaga() {
	yield takeLatest('MONEY_POPULATE_CURRENCIES', populateCurrencies);
	yield takeEvery('MONEY_CREATE_CURRENCY', createCurrency);
	yield takeEvery('MONEY_UPDATE_CURRENCY', updateCurrency);
	yield takeEvery('AUTH_START_LOGIN', login);
	yield takeEvery('SUPPLIER_POPULATE_SUPPLIERS', populateSuppliers);
	yield takeEvery('SUPPLIER_CREATE_SUPPLIER', createSupplier);
	yield takeEvery('SUPPLIER_UPDATE_SUPPLIER', updateSupplier);
};
