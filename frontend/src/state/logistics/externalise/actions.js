import { crudFunctions, crudActions } from '../../../tools/CRUDHelper';

const path = 'logistics/externalise';

const actions = {
	...crudActions(path),
	...crudFunctions(path),
	LOGISTICS_EXTRNALIZE_SET_VALIDATIONS: 'logistics/externalise/validations',
	LOGISTICS_EXTRNALIZE_NEW: 'logistics/externalise/new',
	LOGISTICS_EXTRNALIZE_SET_FIELD: 'logistics/externalise/setField',
};


actions.setValidations = validations => ({
	type: actions.LOGISTICS_EXTRNALIZE_SET_VALIDATIONS,
	validations,
});

actions.newExternalize = () => ({
	type: actions.LOGISTICS_EXTRNALIZE_NEW,
});

export default actions;
