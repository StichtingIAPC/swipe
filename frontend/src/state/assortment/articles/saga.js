import { call, put, takeEvery, takeLatest } from 'redux-saga/effects';
import { push } from 'react-router-redux';

import * as actions from './actions.js';
import * as api from './api';
import { cleanErrorMessage } from '../../../tools/sagaHelpers';

function* fetchAllArticles({ redirectTo }) {
	try {
		const article = yield (yield call(api.getAll)).json();

		yield put(actions.fetchAllArticlesDone(article));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	} catch (e) {
		yield put(actions.fetchAllArticlesFailed(cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchAllArticlesFinally());
	}
}

function* fetchArticle({ id }) {
	try {
		const newArticle = yield (yield call(api.get, id)).json();

		yield put(actions.fetchArticleDone(newArticle));
	} catch (e) {
		yield put(actions.fetchArticleFailed(id, cleanErrorMessage(e)));
	} finally {
		yield put(actions.fetchArticleFinally());
	}
}

function* createArticle({ article }) {
	const document = { ...article };

	try {
		const newArticle = yield (yield call(api.post, document)).json();

		yield put(actions.createArticleDone(newArticle));
		yield put(actions.fetchAllArticles(`/articlemanager/${newArticle.id}/`));
	} catch (e) {
		yield put(actions.createArticleFailed(document, cleanErrorMessage(e)));
	} finally {
		yield put(actions.createArticleFinally());
	}
}

function* updateArticle({ article }) {
	const document = { ...article };

	try {
		const newArticle = yield (yield call(api.put, article.id, document)).json();

		yield put(actions.updateArticleDone(newArticle));
		yield put(actions.fetchAllArticles(`/articlemanager/${newArticle.id}/`));
	} catch (e) {
		yield put(actions.updateArticleFailed(article, cleanErrorMessage(e)));
	} finally {
		yield put(actions.updateArticleFinally());
	}
}

function* deleteArticle({ article }) {
	const document = { ...article };

	try {
		const newArticle = yield (yield call(api.del, article.id, document)).json();

		yield put(actions.deleteArticleDone(newArticle));
		yield put(actions.fetchAllArticles(`/articlemanager/`));
	} catch (e) {
		yield put(actions.deleteArticleFailed(article, cleanErrorMessage(e)));
	} finally {
		yield put(actions.deleteArticleFinally());
	}
}

export default function* saga() {
	yield takeLatest('assortment/articles/FETCH_ALL', fetchAllArticles);
	yield takeLatest('assortment/articles/FETCH', fetchArticle);
	yield takeEvery('assortment/articles/CREATE', createArticle);
	yield takeEvery('assortment/articles/UPDATE', updateArticle);
	yield takeEvery('assortment/articles/DELETE', deleteArticle);
}
