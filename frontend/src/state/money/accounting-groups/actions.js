export function fetchAllAccountingGroups(redirectTo) {
	return {
		type: 'money/accounting-groups/FETCH_ALL',
		redirectTo,
	};
}

export function fetchAllAccountingGroupsDone(accountingGroups) {
	return {
		type: 'money/accounting-groups/FETCH_ALL_DONE',
		accountingGroups,
	};
}

export function fetchAllAccountingGroupsFailed(reason) {
	return {
		type: 'money/accounting-groups/FETCH_ALL_FAILED',
		reason,
	};
}

export function fetchAllAccountingGroupsFinally() {
	return {
		type: 'money/accounting-groups/FETCH_ALL_FINALLY',
	};
}

export function fetchAccountingGroup(id) {
	return {
		type: 'money/accounting-groups/FETCH',
		id,
	};
}

export function fetchAccountingGroupDone(accountingGroup) {
	return {
		type: 'money/accounting-groups/FETCH_DONE',
		accountingGroup,
	};
}

export function fetchAccountingGroupFailed(id, reason) {
	return {
		type: 'money/accounting-groups/FETCH_FAILED',
		id,
		reason,
	};
}

export function fetchAccountingGroupFinally() {
	return {type: 'money/accounting-groups/FETCH_FINALLY'};
}

export function createAccountingGroup(accountingGroup) {
	return {
		type: 'money/accounting-groups/CREATE',
		accountingGroup,
	};
}

export function createAccountingGroupDone(accountingGroup) {
	return {
		type: 'money/accounting-groups/CREATE_DONE',
		accountingGroup,
	};
}

export function createAccountingGroupFailed(accountingGroup, reason) {
	return {
		type: 'money/accounting-groups/CREATE_FAILED',
		accountingGroup,
		reason,
	};
}

export function createAccountingGroupFinally() {
	return {type: 'money/accounting-groups/CREATE_FINALLY'};
}

export function updateAccountingGroup(accountingGroup) {
	return {
		type: 'money/accounting-groups/UPDATE',
		accountingGroup,
	};
}

export function updateAccountingGroupDone(accountingGroup) {
	return {
		type: 'money/accounting-groups/UPDATE_DONE',
		accountingGroup,
	};
}

export function updateAccountingGroupFailed(accountingGroup, reason) {
	return {
		type: 'money/accounting-groups/UPDATE_FAILED',
		accountingGroup,
		reason,
	};
}

export function updateAccountingGroupFinally() {
	return {
		type: 'money/accounting-groups/UPDATE_FINALLY',
	};
}

export function deleteAccountingGroup(id) {
	return {
		type: 'money/accounting-groups/DELETE',
		id,
	};
}

export function deleteAccountingGroupDone(id) {
	return {
		type: 'money/accounting-groups/DELETE_DONE',
		id,
	};
}

export function deleteAccountingGroupFailed(id, reason) {
	return {
		type: 'money/accounting-groups/DELETE_FAILED',
		id,
		reason,
	};
}

export function deleteAccountingGroupFinally() {
	return {type: 'money/accounting-groups/DELETE_FINALLY'};
}

export function setAccountingGroupField(field, value) {
	return {
		type: 'money/accounting-groups/SET_FIELD',
		field,
		value,
	};
}

export default fetchAllAccountingGroups;
export {
	fetchAllAccountingGroups as accountingGroups
};
