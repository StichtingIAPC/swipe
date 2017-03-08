export function startFetchingLabels({redirectTo} = {}) {
	return { type: 'LABEL_FETCH_START', redirectTo };
}

export function doneFetchingLabels(labels) {
	return { type: 'LABEL_FETCH_DONE', labels };
}

export function createLabel(label) {
	return { type: 'LABEL_CREATE', label };
}

export function updateLabel(label) {
	return { type: 'LABEL_UPDATE', label };
}

export function deleteLabel(label) {
	return { type: 'LABEL_DELETE', label };
}

export function labelFetchError(error) {
	return { type: 'LABEL_FETCH_ERROR', error };
}

export function labelInputError(error) {
	return { type: 'LABEL_INPUT_ERROR', error };
}

export {
	startFetchingLabels as labels
}
