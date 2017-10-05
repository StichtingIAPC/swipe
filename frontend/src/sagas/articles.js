import { call, put } from 'redux-saga/effects';
import { push } from 'react-router-redux';
import { get, post, put as api_put } from '../api';
import { articleFetchError, articleInputError, doneFetchingArticles, startFetchingArticles } from '../actions/articles';

export function* fetchArticles({ redirectTo } = {}) {
	let msg = null;

	try {
		const data = yield (yield call(
			get,
			'/article/',
		)).json();

		yield put(doneFetchingArticles(data));
		if (redirectTo)
			yield put(push(redirectTo));
	}	catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(articleFetchError(msg));
	}
}

export function* createArticle({ article } = {}) {
	const document = { ...article };
	let msg = null;

	try {
		const data = yield (yield call(
			post,
			'/article/',
			document,
		)).json();

		yield put(startFetchingArticles({ redirectTo: `/articlemanager/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(articleInputError(msg));
	}
}

export function* updateArticle({ article } = {}) {
	const document = { ...article };
	let msg = null;

	try {
		const data = yield (yield call(
			api_put,
			`/article/${article.id}/`,
			document,
		)).json();

		yield put(startFetchingArticles({ redirectTo: `/articlemanager/${data.id}/` }));
	} catch (e) {
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();

		yield put(articleInputError(msg));
	}
}
