export function fetchAllUnitTypes(redirectTo) {
	return { type: 'assortment/unit-types/FETCH_ALL',
		redirectTo };
}

export function fetchAllUnitTypesDone(unitTypes) {
	return { type: 'assortment/unit-types/FETCH_ALL_DONE',
		unitTypes };
}

export function fetchAllUnitTypesFailed(reason) {
	return { type: 'assortment/unit-types/FETCH_ALL_FAILED',
		reason };
}

export function fetchAllUnitTypesFinally() {
	return { type: 'assortment/unit-types/FETCH_ALL_FINALLY' };
}

export function fetchUnitType(id) {
	return { type: 'assortment/unit-types/FETCH',
		id };
}

export function fetchUnitTypeDone(unitType) {
	return { type: 'assortment/unit-types/FETCH_DONE',
		unitType };
}

export function fetchUnitTypeFailed(id, reason) {
	return { type: 'assortment/unit-types/FETCH_FAILED',
		id,
		reason };
}

export function fetchUnitTypeFinally() {
	return { type: 'assortment/unit-types/FETCH_FINALLY' };
}

export function createUnitType(unitType) {
	return { type: 'assortment/unit-types/CREATE',
		unitType };
}

export function createUnitTypeDone(unitType) {
	return { type: 'assortment/unit-types/CREATE_DONE',
		unitType };
}

export function createUnitTypeFailed(unitType, reason) {
	return { type: 'assortment/unit-types/CREATE_FAILED',
		unitType,
		reason };
}

export function createUnitTypeFinally() {
	return { type: 'assortment/unit-types/CREATE_FINALLY' };
}

export function updateUnitType(unitType) {
	return { type: 'assortment/unit-types/UPDATE',
		unitType };
}

export function updateUnitTypeDone(unitType) {
	return { type: 'assortment/unit-types/UPDATE_DONE',
		unitType };
}

export function updateUnitTypeFailed(unitType, reason) {
	return { type: 'assortment/unit-types/UPDATE_FAILED',
		unitType,
		reason };
}

export function updateUnitTypeFinally() {
	return { type: 'assortment/unit-types/UPDATE_FINALLY' };
}

export function deleteUnitType(id) {
	return { type: 'assortment/unit-types/DELETE',
		id };
}

export function deleteUnitTypeDone(id) {
	return { type: 'assortment/unit-types/DELETE_DONE',
		id };
}

export function deleteUnitTypeFailed(id, reason) {
	return { type: 'assortment/unit-types/DELETE_FAILED',
		id,
		reason };
}

export function deleteUnitTypeFinally() {
	return { type: 'assortment/unit-types/DELETE_FINALLY' };
}

export function setUnitTypeField(field, value) {
	return { type: 'assortment/unit-types/SET_FIELD',
		field,
		value };
}

export default fetchAllUnitTypes;

export {
	fetchAllUnitTypes as unitTypes
};
