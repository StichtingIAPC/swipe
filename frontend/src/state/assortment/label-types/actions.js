export function fetchAllLabelTypes(redirectTo) {
	return { type: 'assortment/label-types/FETCH_ALL',
		redirectTo };
}

export function fetchAllLabelTypesDone(redirectTo) {
	return { type: 'assortment/label-types/FETCH_ALL',
		redirectTo };
}

export function fetchAllLabelTypesFailed(reason) {
	return { type: 'assortment/label-types/FETCH_ALL',
		reason };
}

export function fetchAllLabelTypesFinally() {
	return { type: 'assortment/label-types/FETCH_ALL' };
}

export function fetchLabelType(id) {
	return { type: 'assortment/label-types/FETCH',
		id };
}

export function fetchLabelTypeDone(labelType) {
	return { type: 'assortment/label-types/FETCH_DONE',
		labelType };
}

export function fetchLabelTypeFailed(id, reason) {
	return { type: 'assortment/label-types/FETCH_FAILED',
		id,
		reason };
}

export function fetchLabelTypeFinally() {
	return { type: 'assortment/label-types/FETCH_FINALLY' };
}

export function createLabelType(labelType) {
	return { type: 'assortment/label-types/CREATE',
		labelType };
}

export function createLabelTypeDone(labelType) {
	return { type: 'assortment/label-types/CREATE_DONE',
		labelType };
}

export function createLabelTypeFailed(labelType, reason) {
	return { type: 'assortment/label-types/CREATE_FAILED',
		labelType,
		reason };
}

export function createLabelTypeFinally() {
	return { type: 'assortment/label-types/CREATE_FINALLY' };
}

export function updateLabelType(labelType) {
	return { type: 'assortment/label-types/UPDATE',
		labelType };
}

export function updateLabelTypeDone(labelType) {
	return { type: 'assortment/label-types/UPDATE_DONE',
		labelType };
}

export function updateLabelTypeFailed(labelType, reason) {
	return { type: 'assortment/label-types/UPDATE_FAILED',
		labelType,
		reason };
}

export function updateLabelTypeFinally() {
	return { type: 'assortment/label-types/UPDATE_FINALLY' };
}

export function deleteLabelType(id) {
	return { type: 'assortment/label-types/DELETE',
		id };
}

export function deleteLabelTypeDone(id) {
	return { type: 'assortment/label-types/DELETE_DONE',
		id };
}

export function deleteLabelTypeFailed(id, reason) {
	return { type: 'assortment/label-types/DELETE_FAILED',
		id,
		reason };
}

export function deleteLabelTypeFinally() {
	return { type: 'assortment/label-types/DELETE_FINALLY' };
}

export function setLabelTypeField(field, value) {
	return { type: 'assortment/label-types/SET_FIELD',
		field,
		value };
}

export default fetchAllLabelTypes;
export {
	fetchAllLabelTypes as labelTypes
};
