export function fetchClosedRegisterCounts() {
	return { type: 'REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS' };
}

export function doneFetchingClosedRegisterCounts(registerCounts) {
	return { type: 'REGISTERCOUNT_FETCH_CLOSED_REGISTERCOUNTS_DONE',
		registerCounts };
}

export function createClosedRegisterCounts(registerCount) {
	return { type: 'REGISTERCOUNT_CREATE_CLOSED_REGISTERCOUNT',
		registerCount };
}

export function updateClosedRegisterCounts(registerCount) {
	return { type: 'REGISTERCOUNT_UPDATE_CLOSED_REGISTERCOUNT',
		registerCount };
}

export function deleteClosedRegisterCount(registerCount) {
	return { type: 'REGISTERCOUNT_DELETE_CLOSED_REGISTER',
		registerCount };
}

export function closedRegisterCountFetchError(error) {
	return { type: 'REGISTERCOUNT_CLOSED_REGISTER_FETCH_ERROR',
		error };
}

export function closedRegisterCountInputError(error) {
	return { type: 'REGISTERCOUNT_CLOSED_REGISTER_INPUT_ERROR',
		error };
}

export {
	fetchClosedRegisterCounts as closedRegisterCounts,
};
