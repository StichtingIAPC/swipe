export function getArticleById(state, id) {
	return state.assortment.articles.articles.find(art => art.id === id);
}
