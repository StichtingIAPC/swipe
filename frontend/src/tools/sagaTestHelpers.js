/* eslint-disable no-undef,no-undefined */
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

	for (const [ key, value ] of Object.entries(fields)) {
		form.append(key, value);
	}

	return form;
};

export const exportsSagas = (generator, sagas) => {
	let next = generator.next();

	while (!next.done) {
		const saga = sagas[next.value.FORK.args[0]];

		expect(saga).not.toBe(null);
		expect(saga).not.toBe(undefined);
		expect(saga.fun).toBe(next.value.FORK.args[1]);
		expect(saga.type.name).toBe(next.value.FORK.fn.name);

		delete sagas[next.value.FORK.args[0]];

		next = generator.next();
	}

	expect(Object.keys(sagas).length).toBe(0);
};
