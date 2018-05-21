import { crudFunctions, crudActions } from '../../../tools/CRUDHelper';

const path = 'logistics/externalise';

export const START_NEW = `${path}/startNew`;
export const SET_FIELD = `${path}/setField`;
export const SET_VALIDATIONS = `${path}/validations`;

export const startNew = () => ({ type: START_NEW });
export const setField = (field, value) => ({ type: SET_FIELD,
	field,
	value });
export const setValidations = () => ({ type: SET_VALIDATIONS });

const actions = {
	...crudActions(path),
	...crudFunctions(path),
	START_NEW,
	SET_FIELD,
	SET_VALIDATIONS,
	startNew,
	setField,
	setValidations,
};

export default actions;
