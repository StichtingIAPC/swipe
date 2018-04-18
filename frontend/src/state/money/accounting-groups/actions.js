export const MONEY_ACCOUNTING_GROUPS_FETCH_ALL_START = 'money/accounting-groups/fetchAll/start';
export const MONEY_ACCOUNTING_GROUPS_FETCH_ALL_SUCCESS = 'money/accounting-groups/fetchAll/success';
export const MONEY_ACCOUNTING_GROUPS_FETCH_ALL_FAIL = 'money/accounting-groups/fetchAll/fail';
export const MONEY_ACCOUNTING_GROUPS_FETCH_ALL_FINALLY = 'money/accounting-groups/fetchAll/finally';

export const MONEY_ACCOUNTING_GROUPS_FETCH_START = 'money/accounting-groups/fetch/start';
export const MONEY_ACCOUNTING_GROUPS_FETCH_SUCCESS = 'money/accounting-groups/fetch/success';
export const MONEY_ACCOUNTING_GROUPS_FETCH_FAIL = 'money/accounting-groups/fetch/fail';
export const MONEY_ACCOUNTING_GROUPS_FETCH_FINALLY = 'money/accounting-groups/fetch/finally';

export const MONEY_ACCOUNTING_GROUPS_CREATE_START = 'money/accounting-groups/create/start';
export const MONEY_ACCOUNTING_GROUPS_CREATE_SUCCESS = 'money/accounting-groups/create/success';
export const MONEY_ACCOUNTING_GROUPS_CREATE_FAIL = 'money/accounting-groups/create/fail';
export const MONEY_ACCOUNTING_GROUPS_CREATE_FINALLY = 'money/accounting-groups/create/finally';

export const MONEY_ACCOUNTING_GROUPS_UPDATE_START = 'money/accounting-groups/update/start';
export const MONEY_ACCOUNTING_GROUPS_UPDATE_SUCCESS = 'money/accounting-groups/update/success';
export const MONEY_ACCOUNTING_GROUPS_UPDATE_FAIL = 'money/accounting-groups/update/fail';
export const MONEY_ACCOUNTING_GROUPS_UPDATE_FINALLY = 'money/accounting-groups/update/finally';

export const MONEY_ACCOUNTING_GROUPS_DELETE_START = 'money/accounting-groups/delete/start';
export const MONEY_ACCOUNTING_GROUPS_DELETE_SUCCESS = 'money/accounting-groups/delete/success';
export const MONEY_ACCOUNTING_GROUPS_DELETE_FAIL = 'money/accounting-groups/delete/fail';
export const MONEY_ACCOUNTING_GROUPS_DELETE_FINALLY = 'money/accounting-groups/delete/finally';

export const MONEY_ACCOUNTING_GROUPS_SET_FIELD = 'money/accounting-groups/setField';
export const MONEY_ACCOUNTING_GROUPS_NEW_ACCOUNTINGGROUP = 'money/accounting-groups/newAccountinggroup';

export const fetchAllAccountingGroupsStart = redirectTo => ({
	type: MONEY_ACCOUNTING_GROUPS_FETCH_ALL_START,
	redirectTo,
});

export const fetchAllAccountingGroupsSuccess = accountingGroups => ({
	type: MONEY_ACCOUNTING_GROUPS_FETCH_ALL_SUCCESS,
	accountingGroups,
});

export const fetchAllAccountingGroupsFail = reason => ({
	type: MONEY_ACCOUNTING_GROUPS_FETCH_ALL_FAIL,
	reason,
});

export const fetchAllAccountingGroupsFinally = () => ({
	type: MONEY_ACCOUNTING_GROUPS_FETCH_ALL_FINALLY,
});

export const fetchAccountingGroupStart = id => ({
	type: MONEY_ACCOUNTING_GROUPS_FETCH_START,
	id,
});

export const fetchAccountingGroupSuccess = accountingGroup => ({
	type: MONEY_ACCOUNTING_GROUPS_FETCH_SUCCESS,
	accountingGroup,
});

export const fetchAccountingGroupFail = (id, reason) => ({
	type: MONEY_ACCOUNTING_GROUPS_FETCH_FAIL,
	id,
	reason,
});

export const fetchAccountingGroupFinally = () => ({
	type: MONEY_ACCOUNTING_GROUPS_FETCH_FINALLY,
});

export const createAccountingGroupStart = accountingGroup => ({
	type: MONEY_ACCOUNTING_GROUPS_CREATE_START,
	accountingGroup,
});

export const createAccountingGroupSuccess = accountingGroup => ({
	type: MONEY_ACCOUNTING_GROUPS_CREATE_SUCCESS,
	accountingGroup,
});

export const createAccountingGroupFail = (accountingGroup, reason) => ({
	type: MONEY_ACCOUNTING_GROUPS_CREATE_FAIL,
	accountingGroup,
	reason,
});

export const createAccountingGroupFinally = () => ({
	type: MONEY_ACCOUNTING_GROUPS_CREATE_FINALLY,
});

export const updateAccountingGroupStart = accountingGroup => ({
	type: MONEY_ACCOUNTING_GROUPS_UPDATE_START,
	accountingGroup,
});

export const updateAccountingGroupSuccess = accountingGroup => ({
	type: MONEY_ACCOUNTING_GROUPS_UPDATE_SUCCESS,
	accountingGroup,
});

export const updateAccountingGroupFail = (accountingGroup, reason) => ({
	type: MONEY_ACCOUNTING_GROUPS_UPDATE_FAIL,
	accountingGroup,
	reason,
});

export const updateAccountingGroupFinally = () => ({
	type: MONEY_ACCOUNTING_GROUPS_UPDATE_FINALLY,
});

export const deleteAccountingGroupStart = id => ({
	type: MONEY_ACCOUNTING_GROUPS_DELETE_START,
	id,
});

export const deleteAccountingGroupSuccess = id => ({
	type: MONEY_ACCOUNTING_GROUPS_DELETE_SUCCESS,
	id,
});

export const deleteAccountingGroupFail = (id, reason) => ({
	type: MONEY_ACCOUNTING_GROUPS_DELETE_FAIL,
	id,
	reason,
});

export const deleteAccountingGroupFinally = () => ({
	type: MONEY_ACCOUNTING_GROUPS_DELETE_FINALLY,
});

export const setAccountingGroupField = (field, value) => ({
	type: MONEY_ACCOUNTING_GROUPS_SET_FIELD,
	field,
	value,
});

export const resetAccountingGroup = () => ({
	type: MONEY_ACCOUNTING_GROUPS_NEW_ACCOUNTINGGROUP,
});

