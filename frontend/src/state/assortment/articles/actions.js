export const ASSORTMENT_ARTICLES_FETCH_ALL_START =		'assortment/articles/fetch/all/start';
export const ASSORTMENT_ARTICLES_FETCH_ALL_SUCCESS =	'assortment/articles/fetch/all/success';
export const ASSORTMENT_ARTICLES_FETCH_ALL_FAIL =		'assortment/articles/fetch/all/fail';
export const ASSORTMENT_ARTICLES_FETCH_ALL_FINALLY =	'assortment/articles/fetch/all/finally';
export const ASSORTMENT_ARTICLES_FETCH_START =			'assortment/articles/fetch/start';
export const ASSORTMENT_ARTICLES_FETCH_SUCCESS =		'assortment/articles/fetch/success';
export const ASSORTMENT_ARTICLES_FETCH_FAIL =			'assortment/articles/fetch/fail';
export const ASSORTMENT_ARTICLES_FETCH_FINALLY =		'assortment/articles/fetch/finally';
export const ASSORTMENT_ARTICLES_CREATE_START =			'assortment/articles/create/start';
export const ASSORTMENT_ARTICLES_CREATE_SUCCESS =		'assortment/articles/create/success';
export const ASSORTMENT_ARTICLES_CREATE_FAIL =			'assortment/articles/create/fail';
export const ASSORTMENT_ARTICLES_CREATE_FINALLY = 		'assortment/articles/create/finally';
export const ASSORTMENT_ARTICLES_UPDATE_START = 		'assortment/articles/update/start';
export const ASSORTMENT_ARTICLES_UPDATE_SUCCESS = 		'assortment/articles/update/success';
export const ASSORTMENT_ARTICLES_UPDATE_FAIL = 			'assortment/articles/update/fail';
export const ASSORTMENT_ARTICLES_UPDATE_FINALLY = 		'assortment/articles/update/finally';
export const ASSORTMENT_ARTICLES_DELETE_START =			'assortment/articles/delete/start';
export const ASSORTMENT_ARTICLES_DELETE_SUCCESS =		'assortment/articles/delete/success';
export const ASSORTMENT_ARTICLES_DELETE_FAIL =			'assortment/articles/delete/fail';
export const ASSORTMENT_ARTICLES_DELETE_FINALLY =		'assortment/articles/delete/finally';
export const ASSORTMENT_ARTICLES_SET_FIELD =			'assortment/articles/setField';
export const ASSORTMENT_ARTICLES_NEW_ARTICLE =			'assortment/articles/newArticle';

export const fetchAllArticlesStart = redirectTo => ({
	type: ASSORTMENT_ARTICLES_FETCH_ALL_START,
	redirectTo,
});

export const fetchAllArticlesSuccess = articles => ({
	type: ASSORTMENT_ARTICLES_FETCH_ALL_SUCCESS,
	articles,
});

export const fetchAllArticlesFail = reason => ({
	type: ASSORTMENT_ARTICLES_FETCH_ALL_FAIL,
	reason,
});

export const fetchAllArticlesFinally = () => ({
	type: ASSORTMENT_ARTICLES_FETCH_ALL_FINALLY,
});

export const fetchArticleStart = id => ({
	type: ASSORTMENT_ARTICLES_FETCH_START,
	id,
});

export const fetchArticleSuccess = article => ({
	type: ASSORTMENT_ARTICLES_FETCH_SUCCESS,
	article,
});

export const fetchArticleFail = (id, reason) => ({
	type: ASSORTMENT_ARTICLES_FETCH_FAIL,
	id,
	reason,
});

export const fetchArticleFinally = () => ({
	type: ASSORTMENT_ARTICLES_FETCH_FINALLY,
});

export const createArticleStart = article => ({
	type: ASSORTMENT_ARTICLES_CREATE_START,
	article,
});

export const createArticleSuccess = article => ({
	type: ASSORTMENT_ARTICLES_CREATE_SUCCESS,
	article,
});

export const createArticleFail = (article, reason) => ({
	type: ASSORTMENT_ARTICLES_CREATE_FAIL,
	article,
	reason,
});

export const createArticleFinally = () => ({
	type: ASSORTMENT_ARTICLES_CREATE_FINALLY,
});

export const updateArticleStart = article => ({
	type: ASSORTMENT_ARTICLES_UPDATE_START,
	article,
});

export const updateArticleSuccess = article => ({
	type: ASSORTMENT_ARTICLES_UPDATE_SUCCESS,
	article,
});

export const updateArticleFail = (article, reason) => ({
	type: ASSORTMENT_ARTICLES_UPDATE_FAIL,
	article,
	reason,
});

export const updateArticleFinally = () => ({
	type: ASSORTMENT_ARTICLES_UPDATE_FINALLY,
});

export const deleteArticleStart = id => ({
	type: ASSORTMENT_ARTICLES_DELETE_START,
	id,
});

export const deleteArticleSuccess = id => ({
	type: ASSORTMENT_ARTICLES_DELETE_SUCCESS,
	id,
});

export const deleteArticleFail = (id, reason) => ({
	type: ASSORTMENT_ARTICLES_DELETE_FAIL,
	id,
	reason,
});

export const deleteArticleFinally = () => ({
	type: ASSORTMENT_ARTICLES_DELETE_FINALLY,
});

export const setArticleField = (field, value) => ({
	type: ASSORTMENT_ARTICLES_SET_FIELD,
	field,
	value,
});

export const newArticle = () => ({
	type: ASSORTMENT_ARTICLES_NEW_ARTICLE,
});
