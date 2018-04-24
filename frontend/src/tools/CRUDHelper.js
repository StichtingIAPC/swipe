function trim(path) {
	return path.replace(/^\//, '')
		.replace(/\/$/, '');
}

function toCamelCase(string, delimiter) {
	const parts = string.split(delimiter);

	return parts[0].toLowerCase() + parts.slice(1)
		.map(part => part.slice(0, 1).toUpperCase() + part.slice(1))
		.join();
}

function getActionName(path, fieldName) {
	return `${trim(path.toUpperCase()).replace(/\//g, '_')}_${fieldName.toUpperCase()}`;
}

function getActionValue(path) {
	return trim(path);
}

const crudSubActions = (basePath, actionName) => ({
	[`${getActionName(basePath, actionName)}_START`]: `${getActionValue(basePath, actionName)}/start`,
	[`${getActionName(basePath, actionName)}_SUCCESS`]: `${getActionValue(basePath, actionName)}/success`,
	[`${getActionName(basePath, actionName)}_FAIL`]: `${getActionValue(basePath, actionName)}/fail`,
	[`${getActionName(basePath, actionName)}_FINALLY`]: `${getActionValue(basePath, actionName)}/finally`,
});

function getActionFunctionName(path, fieldName) {
	return toCamelCase(trim(path), '/') + fieldName;
}

const crudSubActionFunctions = (basePath, actionName) => ({
	[`${getActionFunctionName(basePath, actionName)}Start`]: () => ({
		type: `${getActionValue(basePath, actionName)}/start`,
	}),
	[`${getActionFunctionName(basePath, actionName)}Success`]: data => ({
		type: `${getActionValue(basePath, actionName)}/success`,
		data,
	}),
	[`${getActionFunctionName(basePath, actionName)}Fail`]: reason => ({
		type: `${getActionValue(basePath, actionName)}/fail`,
		reason,
	}),
	[`${getActionFunctionName(basePath, actionName)}Finally`]: () => ({
		type: `${getActionValue(basePath, actionName)}/finally`,
	}),
});

export const crudActions = basePath => ({
	...crudSubActions(basePath, 'fetchAll'),
	...crudSubActions(basePath, 'fetch'),
	...crudSubActions(basePath, 'create'),
	...crudSubActions(basePath, 'update'),
	...crudSubActions(basePath, 'delete'),
});

export const crudActionFunctions = basePath => ({
	...crudSubActionFunctions(basePath, 'FetchAll'),
	...crudSubActionFunctions(basePath, 'Fetch'),
	...crudSubActionFunctions(basePath, 'Create'),
	...crudSubActionFunctions(basePath, 'Update'),
	...crudSubActionFunctions(basePath, 'Delete'),
});

export const curdReducers = path => {

};

export const curdSagas = path => {

};


console.log(crudActions('/logistics/externalize/'));
console.log(crudActionFunctions('/logistics/externalize/'));
console.log(curdReducers('/logistics/externalize/'));
console.log(curdSagas('/logistics/externalize/'));
