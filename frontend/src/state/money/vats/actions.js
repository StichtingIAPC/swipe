export function fetchAllvats(redirectTo) {
	return {
		type: 'money/vats/FETCH_ALL',
		redirectTo,
	};
}

export function fetchAllvatsDone(vats) {
	return {
		type: 'money/vats/FETCH_ALL_DONE',
		vats,
	};
}

export function fetchAllvatsFailed(reason) {
	return {
		type: 'money/vats/FETCH_ALL_FAILED',
		reason,
	};
}

export function fetchAllvatsFinally() {
	return {
		type: 'money/vats/FETCH_ALL_FINALLY',
	};
}

export function fetchvat(id) {
	return {
		type: 'money/vats/FETCH',
		id,
	};
}

export function fetchvatDone(vat) {
	return {
		type: 'money/vats/FETCH_DONE',
		vat,
	};
}

export function fetchvatFailed(id, reason) {
	return {
		type: 'money/vats/FETCH_FAILED',
		id,
		reason,
	};
}

export function fetchvatFinally() {
	return {type: 'money/vats/FETCH_FINALLY'};
}

export function createvat(vat) {
	return {
		type: 'money/vats/CREATE',
		vat,
	};
}

export function createvatDone(vat) {
	return {
		type: 'money/vats/CREATE_DONE',
		vat,
	};
}

export function createvatFailed(vat, reason) {
	return {
		type: 'money/vats/CREATE_FAILED',
		vat,
		reason,
	};
}

export function createvatFinally() {
	return {type: 'money/vats/CREATE_FINALLY'};
}

export function updatevat(vat) {
	return {
		type: 'money/vats/UPDATE',
		vat,
	};
}

export function updatevatDone(vat) {
	return {
		type: 'money/vats/UPDATE_DONE',
		vat,
	};
}

export function updatevatFailed(vat, reason) {
	return {
		type: 'money/vats/UPDATE_FAILED',
		vat,
		reason,
	};
}

export function updatevatFinally() {
	return {
		type: 'money/vats/UPDATE_FINALLY',
	};
}

export function deletevat(id) {
	return {
		type: 'money/vats/DELETE',
		id,
	};
}

export function deletevatDone(id) {
	return {
		type: 'money/vats/DELETE_DONE',
		id,
	};
}

export function deletevatFailed(id, reason) {
	return {
		type: 'money/vats/DELETE_FAILED',
		id,
		reason,
	};
}

export function deletevatFinally() {
	return {type: 'money/vats/DELETE_FINALLY'};
}

export function setvatField(field, value) {
	return {
		type: 'money/vats/SET_FIELD',
		field,
		value,
	};
}

export default fetchAllvats;
export {
	fetchAllvats as vats
};
