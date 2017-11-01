export function fetchAllArticles(redirectTo) {
	return { type: 'assortment/articles/FETCH_ALL',
		redirectTo };
}

export function fetchAllArticlesDone(articles) {
	return { type: 'assortment/articles/FETCH_ALL_DONE',
		articles };
}

export function fetchAllArticlesFailed(reason) {
	return { type: 'assortment/articles/FETCH_ALL_FAILED',
		reason };
}

export function fetchAllArticlesFinally() {
	return { type: 'assortment/articles/FETCH_ALL_FINALLY' };
}

export function fetchArticle(id) {
	return { type: 'assortment/articles/FETCH',
		id };
}

export function fetchArticleDone(article) {
	return { type: 'assortment/articles/FETCH_DONE',
		article };
}

export function fetchArticleFailed(id, reason) {
	return { type: 'assortment/articles/FETCH_FAILED',
		id,
		reason };
}

export function fetchArticleFinally() {
	return { type: 'assortment/articles/FETCH_FINALLY' };
}

export function createArticle(article) {
	return { type: 'assortment/articles/CREATE',
		article };
}

export function createArticleDone(article) {
	return { type: 'assortment/articles/CREATE_DONE',
		article };
}

export function createArticleFailed(article, reason) {
	return { type: 'assortment/articles/CREATE_FAILED',
		article,
		reason };
}

export function createArticleFinally() {
	return { type: 'assortment/articles/CREATE_FINALLY' };
}

export function updateArticle(article) {
	return { type: 'assortment/articles/UPDATE',
		article };
}

export function updateArticleDone(article) {
	return { type: 'assortment/articles/UPDATE_DONE',
		article };
}

export function updateArticleFailed(article, reason) {
	return { type: 'assortment/articles/UPDATE_FAILED',
		article,
		reason };
}

export function updateArticleFinally() {
	return { type: 'assortment/articles/UPDATE_FINALLY' };
}

export function deleteArticle(id) {
	return { type: 'assortment/articles/DELETE',
		id };
}

export function deleteArticleDone(id) {
	return { type: 'assortment/articles/DELETE_DONE',
		id };
}

export function deleteArticleFailed(id, reason) {
	return { type: 'assortment/articles/DELETE_FAILED',
		id,
		reason };
}

export function deleteArticleFinally() {
	return { type: 'assortment/articles/DELETE_FINALLY' };
}

export function setArticleField(field, value) {
	return { type: 'assortment/articles/SET_FIELD',
		field,
		value };
}

export default fetchAllArticles;
export {
	fetchAllArticles as articles
};
