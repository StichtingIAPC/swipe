export function getArticleById(state, id) {
	return state.assortment.articles.articles.find(art => art.id === id);
}

export function getArticleNameById(state, id){
	const art = getArticleById(state, id);
	if (art)
		return art.name;
	return null;
}

export function getCount(state, stock) {
	const count = stock ? stock.count : 0;

	const salesListCount = state.sales.sales.sales.find(art => art.article === stock.article);
	if (salesListCount) {
		return count - salesListCount.count;
	} else {
		return count;
	}

}