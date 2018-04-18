export const REGISTER_REGISTERS_FETCH_START = 'register/fetch/start';
export const REGISTER_REGISTERS_FETCH_SUCCESS = 'register/fetch/success';
export const REGISTER_REGISTERS_FETCH_FAIL = 'register/fetch/fail';
export const REGISTER_REGISTERS_FETCH_FINALLY = 'register/fetch/finally';

export const REGISTER_REGISTERS_CREATE_START = 'register/create/start';
export const REGISTER_REGISTERS_CREATE_SUCCESS = 'register/fetch/success';
export const REGISTER_REGISTERS_CREATE_FAIL = 'register/fetch/fail';
export const REGISTER_REGISTERS_CREATE_FINALLY = 'register/fetch/finally';

export const REGISTER_REGISTERS_UPDATE_START = 'register/update/start';
export const REGISTER_REGISTERS_UPDATE_SUCCESS = 'register/fetch/success';
export const REGISTER_REGISTERS_UPDATE_FAIL = 'register/fetch/fail';
export const REGISTER_REGISTERS_UPDATE_FINALLY = 'register/fetch/finally';

export const REGISTER_REGISTERS_DELETE_START = 'register/delete/start';
export const REGISTER_REGISTERS_DELETE_SUCCESS = 'register/fetch/success';
export const REGISTER_REGISTERS_DELETE_FAIL = 'register/fetch/fail';
export const REGISTER_REGISTERS_DELETE_FINALLY = 'register/fetch/finally';

export const REGISTER_REGISTERS_INPUT_SET_ERROR = 'register/input/setError';

export const doneFetchingRegisters = registers => ({
	type: REGISTER_REGISTERS_FETCH_SUCCESS,
	registers,
});

export const createRegister = register => ({
	type: REGISTER_REGISTERS_CREATE_START,
	register,
});

export const updateRegister = register => ({
	type: REGISTER_REGISTERS_UPDATE_START,
	register,
});

export const deleteRegister = register => ({
	type: REGISTER_REGISTERS_DELETE_START,
	register,
});

export const registerFetchError = error => ({
	type: REGISTER_REGISTERS_FETCH_FAIL,
	error,
});

export const registerInputError = error => ({
	type: REGISTER_REGISTERS_INPUT_SET_ERROR,
	error,
});
