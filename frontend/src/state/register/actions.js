export function startFetchingRegisterOpen() {
	return { type: 'REGISTER_OPEN_FETCH_START' };
}

export function doneFetchingRegisterOpen(isOpen) {
	return {
		type: 'REGISTER_OPEN_FETCH_SUCCESS',
		isOpen,
	};
}

export function errorFetchingRegisterOpen() {
	return { type: 'REGISTER_OPEN_FETCH_FEILED' };
}
