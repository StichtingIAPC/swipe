export function startFetchingUnitTypes({redirectTo} = {}) {
	return { type: 'UNIT_TYPE_FETCH_START', redirectTo };
}

export function doneFetchingUnitTypes(unitTypes) {
	return { type: 'UNIT_TYPE_FETCH_DONE', unitTypes };
}

export function createUnitType(unitType) {
	return { type: 'UNIT_TYPE_CREATE', unitType };
}

export function updateUnitType(unitType) {
	return { type: 'UNIT_TYPE_UPDATE', unitType };
}

export function deleteUnitType(unitType) {
	return { type: 'UNIT_TYPE_DELETE', unitType };
}

export function unitTypeFetchError(error) {
	return { type: 'UNIT_TYPE_FETCH_ERROR', error };
}

export function unitTypeInputError(error) {
	return { type: 'UNIT_TYPE_INPUT_ERROR', error };
}

export {
	startFetchingUnitTypes as unitTypes
}
