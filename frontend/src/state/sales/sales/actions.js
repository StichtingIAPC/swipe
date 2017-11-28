export function addToSalesList(art, count) {
	return {
		type: 'SALES_ADD_PRODUCT',
		article: {...art, count: count},
	};
}


export {
	addToSalesList as addToSalesListAction
};

