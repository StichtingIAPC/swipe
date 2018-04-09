/* eslint-disable no-undefined,no-undef */
import {
	booleanControlReducer, collectReducers, objectControlReducer, pathControlReducer, resetFieldReducer,
	setFieldReducer
} from './reducerComponents';

describe('reducerComponent should run correctly with a basic implementation of such a reducer for component: ', () => {
	// Render a checkbox with label in the document
	test('setFieldReducer ', () => {
		const actionOne = 'SETTER1';
		const types = [ actionOne ];

		const setFieldReducerInstance = setFieldReducer(types, 0, 'field1');

		expect(setFieldReducerInstance(undefined, {})).toBe(0);

		let action = { type: actionOne,
			field1: 21 };

		expect(setFieldReducerInstance(undefined, action)).toBe(21);

		action = { type: 'WRONG',
			field1: 21 };
		expect(setFieldReducerInstance(undefined, action)).toBe(0);
	});

	test('objectControlReducer ', () => {
		const actionOne = 'SETTER1';
		const types = [ actionOne ];

		const setFieldReducerInstance = objectControlReducer(types, {}, 'field1');

		expect(setFieldReducerInstance(undefined, {})).toEqual({});

		let action = { type: actionOne,
			field: 'test',
			value: 21 };

		expect(setFieldReducerInstance(undefined, action)).toEqual({ test: 21 });

		action = { type: actionOne,
			field: 'potato',
			value: 'chips' };
		expect(setFieldReducerInstance({ test: 21 }, action)).toEqual({ test: 21,
			potato: 'chips' });

		action = { type: actionOne,
			field: 'test',
			value: 'chips' };
		expect(setFieldReducerInstance({ test: 21 }, action)).toEqual({ test: 'chips' });

		action = { type: 'WRONG' };
		expect(setFieldReducerInstance(undefined, action)).toEqual({});
	});

	test('pathControlReducer ', () => {
		const actionOne = 'SETTER1';
		const types = [ actionOne ];

		const setFieldReducerInstance = pathControlReducer(types, {}, 'field1');

		expect(setFieldReducerInstance(undefined, {})).toEqual({});

		let action = { type: actionOne,
			field: 'test',
			value: 21 };

		expect(setFieldReducerInstance(undefined, action)).toEqual({ test: 21 });

		action = { type: actionOne,
			field: 'potato',
			value: 'chips' };
		expect(setFieldReducerInstance({ test: 21 }, action)).toEqual({ test: 21,
			potato: 'chips' });

		action = { type: actionOne,
			field: 'test',
			value: 'chips' };
		expect(setFieldReducerInstance({ test: 21 }, action)).toEqual({ test: 'chips' });

		action = { type: actionOne,
			field: 'test.a.b',
			value: 'chips',
		};
		expect(setFieldReducerInstance({ test: { otherKey: 'abc' }}, action)).toEqual({ test: {
			otherKey: 'abc',
			a: { b: 'chips' },
		}});

		action = { type: actionOne,
			field: 'test.a.b',
			value: 'chips',
		};
		const obj = { test: {
			otherKey: 'abc',
			a: { b: 'chips' },
		}};

		expect(setFieldReducerInstance(obj, action)).toBe(obj);

		action = { type: 'WRONG' };
		expect(setFieldReducerInstance(undefined, action)).toEqual({});
	});

	test('booleanControlReducer', () => {
		const truthyAction = { type: 'TRUTH_ACTION' };
		const falsyAction = { type: 'UNTRUTH_ACTION' };
		const wrongAction = { type: 'WRONG_ACTION' };


		const types = { [truthyAction.type]: true,
			[falsyAction.type]: false };

		const booleanReducer = booleanControlReducer(types, false);

		expect(booleanReducer(undefined, {})).toBe(false);

		expect(booleanReducer(true, truthyAction)).toBe(true);
		expect(booleanReducer(false, falsyAction)).toBe(false);

		expect(booleanReducer(true, truthyAction)).toBe(true);
		expect(booleanReducer(true, falsyAction)).toBe(false);

		expect(booleanReducer(false, truthyAction)).toBe(true);
		expect(booleanReducer(false, falsyAction)).toBe(false);

		expect(booleanReducer(true, wrongAction)).toBe(true);
		expect(booleanReducer(false, wrongAction)).toBe(false);
	});

	test('collectReducers', () => {
		const actionOne = 'actionOne';
		const actionTwo = 'actionTwo';

		const resetFieldReducerInstance = resetFieldReducer([ actionOne ], false);
		const resetFieldReducerInstance2 = resetFieldReducer([ actionTwo ], 12);
		const a = collectReducers(resetFieldReducerInstance, resetFieldReducerInstance2);

		expect(a(undefined, {})).toBe(false);
		expect(a('data', {})).toBe('data');

		expect(a('data', { type: actionOne })).toBe(false);
		expect(a('data', { type: actionTwo })).toBe(12);
	});

	test('resetFieldReducer', () => {
		const actionOne = 'WRONG_ACTION';
		const types = [ actionOne ];
		const resetFieldReducerInstance = resetFieldReducer(types, false);

		expect(resetFieldReducerInstance(undefined, {})).toBe(false);
		expect(resetFieldReducerInstance(true, { type: actionOne })).toBe(false);
		expect(resetFieldReducerInstance(true, {})).toBe(true);
	});
});
