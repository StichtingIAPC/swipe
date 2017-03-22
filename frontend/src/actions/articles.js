export function startFetchingArticles({redirectTo} = {}) {
	return { type: 'ARTICLE_FETCH_START', redirectTo };
}

export function doneFetchingArticles(articles) {
	return { type: 'ARTICLE_FETCH_DONE', articles };
}

export function createArticle(article) {
	return { type: 'ARTICLE_CREATE', article };
}

export function updateArticle(article) {
	return { type: 'ARTICLE_UPDATE', article };
}

export function deleteArticle(article) {
	return { type: 'ARTICLE_DELETE', article };
}

export function articleFetchError(error) {
	return { type: 'ARTICLE_FETCH_ERROR', error };
}

export function articleInputError(error) {
	return { type: 'ARTICLE_INPUT_ERROR', error };
}

export {
	startFetchingArticles as articles
}

