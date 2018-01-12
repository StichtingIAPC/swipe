/* eslint-disable no-undef */
export const notDone = result => expect(result.done).toBe(false);
export const done = result => expect(result.done).toBe(true);

export const isValue = expectation => result => expect(result.value).toBe(expectation);
export const isObject = expectation => result => expect(result.value).toMatchObject(expectation);

export const nextStep = (generator, tests, ...args) => {
	const result = generator.next(...args);

	for (const t of tests) {
		t(result);
	}

	return result;
};

export const formOf = fields => {
	const form = new FormData();

	for (const field in fields) {
		if (fields.hasOwnProperty(field)) {
			form.append(field, fields[field]);
		}
	}

	return form;
};
