export const SALES_COMMIT_CREATE = 'sales/commit/create';
export const SALES_COMMIT_CREATE_DONE = 'sales/commit/create/done';
export const SALES_COMMIT_CREATE_FAILED = 'sales/commit/create/failed';
export const SALES_COMMIT_CREATE_FINALLY = 'sales/commit/create/finally';

export const salesCommitCreate = () => ({ type: SALES_COMMIT_CREATE });
export const salesCommitCreateDone = (transaction) => ({ type: SALES_COMMIT_CREATE_DONE, transaction });
export const salesCommitCreateFailed = (error) => ({ type: SALES_COMMIT_CREATE_FAILED, error });
export const salesCommitCreateFinally = () => ({ type: SALES_COMMIT_CREATE_FINALLY});



