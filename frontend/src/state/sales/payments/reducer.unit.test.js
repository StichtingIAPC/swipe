/* eslint-disable no-undefined */
/**
 * Created by nander on 16-1-18.
 */
import paymentReducer from './reducer.js'
import {ADD_PAYMENT_TYPE, REMOVE_PAYMENT_TYPE} from "./actions";
describe('Reducer tests', () => {
	test('successful', () => {
		expect(paymentReducer(undefined, {})).toEqual({});

		expect(paymentReducer(undefined, {type: ADD_PAYMENT_TYPE, paymentType: 'MAESTRO', amount: 4 })).toEqual({"MAESTRO": 4});

		expect(paymentReducer({"MAESTRO": 4}, {type: REMOVE_PAYMENT_TYPE, paymentType: 'MAESTRO'})).toEqual({});
	});
});