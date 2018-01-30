export const getSales = (state) => state.sales.sales.map(it => ({...it, ['class']: 'SalesTransactionLine', cost: (it.book_value)}));
