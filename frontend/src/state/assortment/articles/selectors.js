export function getArticleById(state, id) {
	let art = state.assortment.articles.articles.find(art => art.id === id);
	if (!art)
		return {name: "HI"};
	return art;
}
export function getCount(state, stock) {
	if (!stock)
		return 0;
	if (!state.sales)
		return stock.count;


	let oth = state.sales.sales.sales.find(art => art.article === stock.article);
	if (oth) {
		return stock.count - oth.count;
	}

	return stock.count;
}