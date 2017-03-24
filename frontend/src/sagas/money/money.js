import { takeLatest, takeEvery } from "redux-saga";
import { createCurrency, updateCurrency, fetchCurrencies } from "./currencies";
import { fetchVATs, createVAT, updateVAT } from "./VATs";
import { fetchAccountingGroups, createAccountingGroup, updateAccountingGroup } from "./accountingGroups";

export default function* moneySagas() {
	// Currency
	yield takeLatest('CURRENCY_FETCH_START', fetchCurrencies);
	yield takeEvery('CURRENCY_CREATE', createCurrency);
	yield takeEvery('CURRENCY_UPDATE', updateCurrency);
	// VAT
	yield takeLatest('VAT_FETCH_START', fetchVATs);
	yield takeEvery('VAT_CREATE', createVAT);
	yield takeEvery('VAT_UPDATE', updateVAT);
	// Accounting groups
	yield takeLatest('ACCOUNTING_GROUP_FETCH_START', fetchAccountingGroups);
	yield takeEvery('ACCOUNTING_GROUP_CREATE', createAccountingGroup);
	yield takeEvery('ACCOUNTING_GROUP_UPDATE', updateAccountingGroup);
}
