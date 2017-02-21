import { takeEvery, takeLatest } from "redux-saga";
import { login, saveLoginDetails } from "./sagas/auth.js";
import { fetchCurrencies, createCurrency, updateCurrency } from "./sagas/money/currencies";
import { fetchSuppliers, createSupplier, updateSupplier } from "./sagas/suppliers";
import { fetchVATs, createVAT, updateVAT } from "./sagas/money/VATs";
import { fetchVATPeriods, createVATPeriod, updateVATPeriod } from "./sagas/money/VATPeriods";

export default function* rootSaga() {
	// Auth sagas
	yield takeEvery('AUTH_START_LOGIN', login);
	yield takeEvery('AUTH_LOGIN_SUCCESS', saveLoginDetails);

	// Supplier sagas
	yield takeLatest('SUPPLIER_FETCH_START', fetchSuppliers);
	yield takeEvery('SUPPLIER_CREATE', createSupplier);
	yield takeEvery('SUPPLIER_UPDATE', updateSupplier);
	yield takeEvery('SUPPLIER_DELETE', updateSupplier);

	// Money Sagas - Currency
	yield takeLatest('CURRENCY_FETCH_START', fetchCurrencies);
	yield takeEvery('CURRENCY_CREATE', createCurrency);
	yield takeEvery('CURRENCY_UPDATE', updateCurrency);
	// Money Sagas - VAT
	yield takeLatest('VAT_FETCH_START', fetchVATs);
	yield takeEvery('VAT_CREATE', createVAT);
	yield takeEvery('VAT_UPDATE', updateVAT);
	// Money Sagas - VATPeriod
	yield takeLatest('VAT_PERIOD_FETCH_START', fetchVATPeriods);
	yield takeEvery('VAT_PERIOD_CREATE', createVATPeriod);
	yield takeEvery('VAT_PERIOD_UPDATE', updateVATPeriod);
};
