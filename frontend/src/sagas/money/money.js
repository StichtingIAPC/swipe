import { takeEvery, takeLatest } from 'redux-saga';
import { createCurrency, fetchCurrencies, updateCurrency } from './currencies';
import { createVAT, fetchVATs, updateVAT } from './VATs';
import { createAccountingGroup, fetchAccountingGroups, updateAccountingGroup } from './accountingGroups';

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
