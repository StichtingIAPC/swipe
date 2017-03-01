import { takeEvery, takeLatest } from "redux-saga";
import { login, saveLoginDetails } from "./sagas/auth.js";
import { fetchCurrencies, createCurrency, updateCurrency } from "./sagas/money/currencies";
import { fetchSuppliers, createSupplier, updateSupplier } from "./sagas/suppliers";
import { fetchVATs, createVAT, updateVAT } from "./sagas/money/VATs";
import { fetchAccountingGroups, createAccountingGroup, updateAccountingGroup } from "./sagas/money/accountingGroups";
import { fetchArticles, createArticle, updateArticle } from "./sagas/articles";

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
	// Money Sagas - Accounting groups
	yield takeLatest('ACCOUNTING_GROUP_FETCH_START', fetchAccountingGroups);
	yield takeEvery('ACCOUNTING_GROUP_CREATE', createAccountingGroup);
	yield takeEvery('ACCOUNTING_GROUP_UPDATE', updateAccountingGroup);

	// Article sagas
	yield takeLatest('ARTICLE_FETCH_START', fetchArticles);
	yield takeEvery('ARTICLE_CREATE', createArticle);
	yield takeEvery('ARTICLE_UPDATE', updateArticle);
	yield takeEvery('ARTICLE_DELETE', updateArticle);
};
