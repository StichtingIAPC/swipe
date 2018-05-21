export const getExternailzeRootState = state => state.logisitics.externalize;
export const getExternailzeCurrentItem = state => getExternailzeRootState(state).currentItem;
export const getExternailzeItems = state => getExternailzeRootState(state).items;

export const getExternalisationLoading = state => getExternailzeItems(state).isLoading;
export const getExternalisationPopulated = state => getExternailzeItems(state).isPopulated;

export const getExternalisationValidations = state => getExternailzeRootState(state).validations;
