export const getCustomer = state => state.sales.customer;
// ATTENTION: The function below is (obviously) a dummy function for acquiring the total of a current sale.
// When properly implmeneting this selector please replace all occurences of getDummySalesTotal with said proper selector
export const getDummySalesTotal = state => ({ amount: '6969.420' });
