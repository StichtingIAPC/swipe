export const SALES_ADD_PRODUCT = 'sales/add/product';
export const SALES_RECEIPT_ADD_PRODUCT = 'sales/add/product/dummy';

export function addToSalesList(article, count, currentAmount) {
	return {
		type: SALES_ADD_PRODUCT,
		article,
		count,
		currentAmount,
	};
}

export function receiptAddProduct(articleId, count) {
	return {
		type: SALES_RECEIPT_ADD_PRODUCT,
		article: articleId,
		count,
	};
}

export {
	addToSalesList as addToSalesListAction,
	receiptAddProduct as receiptAddProductAction,
};

