export const getCurrencyByIso = (state, iso) => {
	const currencies = state.money.currencies.currencies;
	for (const i in currencies) {
		if (currencies[i].iso === iso)
			return currencies[i];
	}

	return {iso: "ERR", symbol: "«"};
};
export const getCurrencyActiveObject = (state) => state.money.currencies.activeObject;
export const getCurrencyValidations = (state) => state.money.currencies.validations;