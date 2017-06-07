export function startFetchingAccountingGroups({ redirectTo } = {}) {
	return {
		type: 'ACCOUNTING_GROUP_FETCH_START',
		redirectTo,
	};
}

export function doneFetchingAccountingGroups(accountingGroups) {
	return {
		type: 'ACCOUNTING_GROUP_FETCH_DONE',
		accountingGroups,
	};
}

export function createAccountingGroup(accountingGroup) {
	return {
		type: 'ACCOUNTING_GROUP_CREATE',
		accGrp: accountingGroup,
	};
}

export function updateAccountingGroup(accountingGroup) {
	return {
		type: 'ACCOUNTING_GROUP_UPDATE',
		accGrp: accountingGroup,
	};
}

export function deleteAccountingGroup(accountingGroup) {
	return {
		type: 'ACCOUNTING_GROUP_DELETE',
		accGrp: accountingGroup,
	};
}

export function accountingGroupInputError(error) {
	return {
		type: 'ACCOUNTING_GROUP_INPUT_ERROR',
		error,
	};
}

export function accountingGroupFetchError(error) {
	return {
		type: 'ACCOUNTING_GROUP_FETCH_ERROR',
		error,
	};
}

export {
	startFetchingAccountingGroups as accountingGroups,
};
