export function fetchOpenRegisterCounts() {
	return { type: 'REGISTERCOUNT_FETCH_OPEN_REGISTERCOUNTS' };
}

export function doneFetchingOpenRegisterCounts(registerCounts) {
	return { type: 'REGISTERCOUNT_FETCH_OPEN_REGISTERCOUNTS_DONE',
		registerCounts };
}

export function createOpenRegisterCounts(registerCount) {
	return { type: 'REGISTERCOUNT_CREATE_OPEN_REGISTERCOUNT',
		registerCount };
}

export function updateOpenRegisterCounts(registerCount) {
	return { type: 'REGISTERCOUNT_UPDATE_OPEN_REGISTERCOUNT',
		registerCount };
}

export function deleteOpenRegisterCount(registerCount) {
	return { type: 'REGISTERCOUNT_DELETE_OPEN_REGISTER',
		registerCount };
}

export function openRegisterCountFetchError(error) {
	return { type: 'REGISTERCOUNT_OPEN_REGISTER_FETCH_ERROR',
		error };
}

export function openRegisterCountInputError(error) {
	return { type: 'REGISTERCOUNT_OPEN_REGISTER_INPUT_ERROR',
		error };
}

export function openUpdateAmount(register, amount) {
	return { type: 'REGISTERCOUNT_OPEN_UPDATE_AMOUNT',
		register,
		amount,
	};
}

export function openUpdateDenomAmount(register, denom, amount) {
	return { type: 'REGISTERCOUNT_OPEN_UPDATE_DENOM_AMOUNT',
		register,
		denom,
		amount,
	};
}


export {
	fetchOpenRegisterCounts as openRegisterCounts,
};
