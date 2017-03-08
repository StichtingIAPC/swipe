export function startFetchingRegisters({redirectTo} = {}) {
	return { type: 'REGISTER_FETCH_START', redirectTo };
}

export function doneFetchingRegisters(registers) {
	return { type: 'REGISTER_FETCH_DONE', registers };
}

export function createRegister(register) {
	return { type: 'REGISTER_CREATE', register };
}

export function updateRegister(register) {
	return { type: 'REGISTER_UPDATE', register };
}

export function deleteRegister(register) {
	return { type: 'REGISTER_DELETE', register };
}

export function registerFetchError(error) {
	return { type: 'REGISTER_FETCH_ERROR', error };
}

export function registerInputError(error) {
	return { type: 'REGISTER_INPUT_ERROR', error };
}

export {
	startFetchingRegisters as registers,
}
