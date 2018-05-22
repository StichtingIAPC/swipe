/* eslint-disable no-undef,no-undefined */
import paymentReducer from './reducer.js';
import {
	SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT,
	TOGGLE_SPLIT_PAYMENT,
	RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT
} from './actions';

describe('Tests reducer for sales.payments', () => {
	const defaultState = {
		paymentIsSplit: false,
		paymentTypes: {},
		validations: {},
	};
	test('No Action', () => {
		expect(paymentReducer(undefined, {})).toEqual(defaultState);
	});
	test('Set new payment type', () => {
		expect(paymentReducer(undefined, {
			type: SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT,
			field: '7',
			value: {
				amount: '5',
			},
		})).toEqual({
			...defaultState,
			paymentTypes: {
				7: {
					amount: '5',
				},
			},
		});
	});

	test('Reset payment types', () => {
		expect(paymentReducer({
			...defaultState,
			paymentTypes: {
				7: {
					amount: '5',
				},
			},
		}, {
			type: RESET_AMOUNTS_OF_PAYMENT_TYPES_ON_RECEIPT,
		})).toEqual({
			...defaultState,
		});
	});

	test('Set existing payment type', () => {
		expect(paymentReducer({
			...defaultState,
			paymentTypes: {
				7: {
					amount: '5',
				},
			},
		}, {
			type: SET_AMOUNT_OF_PAYMENT_TYPE_ON_RECEIPT,
			field: '7',
			value: { amount: '4' },
		})).toEqual({
			...defaultState,
			paymentTypes: {
				7: {
					amount: '4',
				},
			},
		});
	});

	test('Toggle split payment empty state', () => {
		expect(paymentReducer(undefined, {
			type: TOGGLE_SPLIT_PAYMENT,
		})).toEqual({
			...defaultState,
			paymentIsSplit: true,
		});
	});

	test('Toggle split payment set state', () => {
		expect(paymentReducer({
			paymentIsSplit: true,
			paymentTypes: {},
		}, {
			type: TOGGLE_SPLIT_PAYMENT,
		})).toEqual({
			...defaultState,
			paymentIsSplit: false,
		});
	});
});
