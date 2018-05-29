export const REGISTER_FETCH_START = 'register/register/fetchAll/start';
export const REGISTER_FETCH_DONE = 'register/register/fetchAll/done';
export const REGISTER_CREATE = 'register/register/create';
export const REGISTER_UPDATE = 'register/register/update';
export const REGISTER_FETCH_ERROR = 'register/register/fetchAll/error';
export const REGISTER_FETCH_INPUT_ERROR = 'register/register/fetchAll/inputError';



export function startFetchingRegisters({ redirectTo } = {}) {
	return {
		type: REGISTER_FETCH_START,
		redirectTo,
	};
}

export function doneFetchingRegisters(registers) {
	return {
		type: REGISTER_FETCH_DONE,
		registers,
	};
}

export function createRegister(register) {
	return {
		type: REGISTER_CREATE,
		register,
	};
}

export function updateRegister(register) {
	return {
		type: REGISTER_UPDATE,
		register,
	};
}

export function registerFetchError(error) {
	return {
		type: REGISTER_FETCH_ERROR,
		error,
	};
}

export function registerInputError(error) {
	return {
		type: REGISTER_FETCH_INPUT_ERROR,
		error,
	};
}
