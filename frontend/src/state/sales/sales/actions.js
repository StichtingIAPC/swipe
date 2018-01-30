export const SALES_ADD_PRODUCT = 'sales/add/product';

export function addToSalesList(article, count, currentAmount) {
	return {
		type: SALES_ADD_PRODUCT,
		article,
		count,
		currentAmount,
	};
}

export {
	addToSalesList as addToSalesListAction
};

