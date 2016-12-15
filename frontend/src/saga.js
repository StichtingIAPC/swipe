import {takeEvery, takeLatest} from "redux-saga";
import {login, saveLoginDetails} from "./sagas/auth.js";
import {populateCurrencies, createCurrency, updateCurrency} from "./sagas/money/currencies";
import {fetchSuppliers, createSupplier, updateSupplier} from "./sagas/suppliers";

export default function* rootSaga() {
	yield takeLatest('MONEY_POPULATE_CURRENCIES', populateCurrencies);
	yield takeEvery('MONEY_CREATE_CURRENCY', createCurrency);
	yield takeEvery('MONEY_UPDATE_CURRENCY', updateCurrency);
	yield takeEvery('AUTH_START_LOGIN', login);
	yield takeEvery('AUTH_LOGIN_SUCCESS', saveLoginDetails);

	// Supplier sagas
	yield takeLatest('SUPPLIER_FETCH_START', fetchSuppliers);
	yield takeEvery('SUPPLIER_CREATE', createSupplier);
	yield takeEvery('SUPPLIER_UPDATE', updateSupplier);
	yield takeEvery('SUPPLIER_DELETE', updateSupplier);
};
