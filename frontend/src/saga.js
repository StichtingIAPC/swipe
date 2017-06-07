import { takeEvery, takeLatest } from "redux-saga";
import { login, saveLoginDetails } from "./sagas/auth.js";
import { createSupplier, fetchSuppliers, updateSupplier } from "./sagas/suppliers";
import { createArticle, fetchArticles, updateArticle } from "./sagas/articles";
import assortment from "./sagas/assortment/assortment";
import money from "./sagas/money/money";
import register from "./sagas/register/register";

export default function* rootSaga() {
	// Auth sagas
	yield takeEvery('AUTH_START_LOGIN', login);
	yield takeEvery('AUTH_LOGIN_SUCCESS', saveLoginDetails);

	// Supplier sagas
	yield takeLatest('SUPPLIER_FETCH_START', fetchSuppliers);
	yield takeEvery('SUPPLIER_CREATE', createSupplier);
	yield takeEvery('SUPPLIER_UPDATE', updateSupplier);
	yield takeEvery('SUPPLIER_DELETE', updateSupplier);

	// Article sagas
	yield takeLatest('ARTICLE_FETCH_START', fetchArticles);
	yield takeEvery('ARTICLE_CREATE', createArticle);
	yield takeEvery('ARTICLE_UPDATE', updateArticle);
	yield takeEvery('ARTICLE_DELETE', updateArticle);


	yield* assortment();
	yield* money();
	yield* register();
}
