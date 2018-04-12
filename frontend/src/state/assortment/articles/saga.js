import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import * as actions from './actions.js';
import * as api from './api';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';

function* fetchAllArticles({ redirectTo }) {
	try {
		const article = yield (yield call(api.getAll)).json();

		yield put(actions.fetchAllArticlesSuccess(article));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		yield put(actions.fetchAllArticlesFail(cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchAllArticlesFinally());
	}
}

function* fetchArticle({ id }) {
	try {
		const newArticle = yield (yield call(api.get, id)).json();

		yield put(actions.fetchArticleSuccess(newArticle));
	} catch (e) {
		yield put(actions.fetchArticleFail(id, cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchArticleFinally());
	}
}

function* createArticle({ article }) {
	const document = { ...article };

	try {
		const newArticle = yield (yield call(api.post, document)).json();

		yield put(actions.createArticleSuccess(newArticle));
		yield put(actions.fetchAllArticlesStart(`/articlemanager/${newArticle.id}/`));
	} catch (e) {
		yield put(actions.createArticleFail(document, cleanErrorMessage(e)));
	} finally {
		yield put(actions.createArticleFinally());
	}
}

function* updateArticle({ article }) {
	const document = { ...article };

	try {
		const newArticle = yield (yield call(api.put, article.id, document)).json();

		yield put(actions.updateArticleSuccess(newArticle));
		yield put(actions.fetchAllArticlesStart(`/articlemanager/${newArticle.id}/`));
	} catch (e) {
		yield put(actions.updateArticleFail(article, cleanErrorMessage(e)));
	} finally {
		yield put(actions.updateArticleFinally());
	}
}

function* deleteArticle({ article }) {
	const document = { ...article };

	try {
		const newArticle = yield (yield call(api.del, article.id, document)).json();

		yield put(actions.deleteArticleSuccess(newArticle));
		yield put(actions.fetchAllArticlesStart(`/articlemanager/`));
	} catch (e) {
		yield put(actions.deleteArticleFail(article, cleanErrorMessage(e)));
	} finally {
		yield put(actions.deleteArticleFinally());
	}
}

export default function* saga() {
	yield takeLatest(actions.ASSORTMENT_ARTICLES_FETCH_ALL_START, fetchAllArticles);
	yield takeLatest(actions.ASSORTMENT_ARTICLES_FETCH_START, fetchArticle);
	yield takeEvery(actions.ASSORTMENT_ARTICLES_CREATE_START, createArticle);
	yield takeEvery(actions.ASSORTMENT_ARTICLES_UPDATE_START, updateArticle);
	yield takeEvery(actions.ASSORTMENT_ARTICLES_DELETE_START, deleteArticle);
}
