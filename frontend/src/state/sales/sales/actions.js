export const SALES_MUTATE_SALES_LINE = 'sales/add/product';

export function mutateSalesLineOfArticle(article, amount) {
	return {
		type: SALES_MUTATE_SALES_LINE,
		article,
		amount,
	};
}

export {
	mutateSalesLineOfArticle as mutateSalesLineOfArticleAction
};

