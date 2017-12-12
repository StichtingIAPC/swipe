export function getArticleById(state, id) {
	return state.assortment.articles.articles.find(art => art.id === id);
}

export function getStockForArticle(state, article) {

	console.log(state.stock.stock.find(art => art.article === article));
	return state.stock.stock.find(art => art.article === article);
}

export function getArticleNameById(state, id) {
	const art = getArticleById(state, id);
	if (art)
		return art.name;
	return null;
}

export function getCount(state, stock) {
	const count = stock ? stock.count : 0;
	if(!state.sales.sales)
		return count;
	const salesListCount = state.sales.sales.sales.find(art => art.article === stock.article);
	if (salesListCount) {
		return count - salesListCount.count;
	} else {
		return count;
	}

}

export function getSalesTotal(state) {
	return state.sales.sales.sales.reduce((a, art) => {
		return { ...art.price, amount: a.amount + art.count * art.price.amount };
	}, {currency: 'EUR', amount: 0});
}
