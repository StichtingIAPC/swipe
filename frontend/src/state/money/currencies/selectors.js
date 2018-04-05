export const getCurrencyByIso = (state, iso) => {
	const currencies = state.money.currencies.currencies;
	for (const i in currencies) {
		if (currencies[i].iso === iso)
			return currencies[i];
	}

	return {iso: "ERR", symbol: "«"};
};
