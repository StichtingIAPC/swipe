import { crudActionFunctions, crudActions } from '../../../tools/CRUDHelper';
const path = 'logistics/externalise';

export default {
	...crudActions(path),
	...crudActionFunctions(path),
};


export const LOGISTICS_EXTRNALIZE_SET_LOADING = 'logistics/externalise/setLoading';
export const LOGISTICS_EXTRNALIZE_SET_VALIDATIONS = 'logistics/externalise/validations';
export const LOGISTICS_EXTRNALIZE_NEW = 'logistics/externalise/new';
export const LOGISTICS_EXTRNALIZE_SET_FIELD = 'logistics/externalise/setField';

export const setValidations = validations => ({
	type: LOGISTICS_EXTRNALIZE_SET_VALIDATIONS,
	validations,
});

export const newExternalize = () => ({
	type: LOGISTICS_EXTRNALIZE_NEW,
});

export const setLoadingAction = () => ({
	type: LOGISTICS_EXTRNALIZE_SET_LOADING,
});

export const setField = (field, value) => ({
	type: LOGISTICS_EXTRNALIZE_SET_FIELD,
	field,
	value,
});
