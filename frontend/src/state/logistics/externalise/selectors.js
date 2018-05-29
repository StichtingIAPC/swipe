export const getExternailseRootState = state => state.logistics.externalise;

export const getExternailseCurrentItem = state => getExternailseRootState(state).currentItem;
export const getExternailseItems = state => getExternailseRootState(state).items;

export const getExternalisationLoading = state => getExternailseItems(state).isLoading;
export const getExternalisationPopulated = state => getExternailseItems(state).isPopulated;

export const getExternalisationValidations = state => getExternailseRootState(state).validations;
