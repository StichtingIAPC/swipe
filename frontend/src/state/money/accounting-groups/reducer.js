const initialState = {
	accountingGroups: null,
	fetching: false,
	inputError: null,
	fetchError: null,
};

export default function accountingGroups(state = initialState, action) {
	if (action.type === 'ACCOUNTING_GROUP_FETCH_START') {
		return {
			...state,
			fetching: true,
			inputError: null,
		};
	}
	if (action.type === 'ACCOUNTING_GROUP_FETCH_DONE') {
		return {
			...state,
			fetching: false,
			accountingGroups: action.accountingGroups.map(accountingGroup => ({ ...accountingGroup })),
			fetchError: null,
		};
	}

	if (action.type === 'ACCOUNTING_GROUP_INPUT_ERROR') 		{
		return {
			...state,
			inputError: action.error,
		};
	}
	if (action.type === 'ACCOUNTING_GROUP_FETCH_ERROR') 		{
		return {
			...state,
			fetching: false,
			fetchError: action.error,
		};
	}
	return state;
}
