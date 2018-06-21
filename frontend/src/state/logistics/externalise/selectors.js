export const getExternaliseRootState = state => state.logistics.externalise;

const getItemsSubstate = state => getExternaliseRootState(state).items;
const getCurrentItemSubstate = state => getExternaliseRootState(state).currentItem;

export const getExternailseItems = state => getItemsSubstate(state).data;
export const getExternailseItemsLoading = state => getItemsSubstate(state).isLoading;
export const getExternailseItemsPopulated = state => getItemsSubstate(state).isPopulated;

export const getExternailseCurrentItem = state => getCurrentItemSubstate(state).data;
export const getExternailseCurrentItemLoading = state => getCurrentItemSubstate(state).isLoading;
export const getExternailseCurrentItemPopulated = state => getCurrentItemSubstate(state).isPopulated;
export const getExternailseCurrentItemError = state => getCurrentItemSubstate(state).error;

export const getExternalisationValidations = state => getExternaliseRootState(state).validations;
