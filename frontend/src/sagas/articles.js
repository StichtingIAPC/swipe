import { call, put } from "redux-saga/effects";
import { push } from "react-router-redux";
import { get, post, put as api_put } from "../api";
import { startFetchingArticles, doneFetchingArticles, articleFetchError, articleInputError } from "../actions/articles";

export function* fetchArticles({redirectTo} = {}) {
	try {
		const data = yield (yield call(
			get,
			'/article/',
		)).json();
		yield put(doneFetchingArticles(data));
		if (redirectTo) {
			yield put(push(redirectTo));
		}
	}	catch (e) {
		yield put(articleFetchError(e.message));
	}
}

export function* createArticle({ article } = {}) {
	const document = { ...article };

	try {
		const data = yield (yield call(
			post,
			'/article/',
			document,
		)).json();

		yield put(startFetchingArticles({
			redirectTo: `/articlemanager/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(articleInputError(msg));
	}
}

export function* updateArticle({ article } = {}) {
	const document = { ...article };

	try {
		const data = yield (yield call(
			api_put,
			`/article/${article.id}/`,
			document,
		)).json();

		yield put(startFetchingArticles({
			redirectTo: `/articlemanager/${data.id}/`,
		}));
	} catch (e) {
		let msg;
		if (e instanceof Error)
			msg = e.message;
		if (e instanceof Response)
			msg = e.json();
		yield put(articleInputError(msg));
	}
}
