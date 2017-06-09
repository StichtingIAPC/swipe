export function startFetchingLabelTypes({ redirectTo } = {}) {
	return {
		type: 'LABEL_TYPE_FETCH_START',
		redirectTo,
	};
}

export function doneFetchingLabelTypes(labelTypes) {
	return {
		type: 'LABEL_TYPE_FETCH_DONE',
		labelTypes,
	};
}

export function createLabelType(labelType) {
	return {
		type: 'LABEL_TYPE_CREATE',
		labelType,
	};
}

export function updateLabelType(labelType) {
	return {
		type: 'LABEL_TYPE_UPDATE',
		labelType,
	};
}

export function deleteLabelType(labelType) {
	return {
		type: 'LABEL_TYPE_DELETE',
		labelType,
	};
}

export function labelTypeFetchError(error) {
	return {
		type: 'LABEL_TYPE_FETCH_ERROR',
		error,
	};
}

export function labelTypeInputError(error) {
	return {
		type: 'LABEL_TYPE_INPUT_ERROR',
		error,
	};
}

export {
	startFetchingLabelTypes as labelTypes
};
