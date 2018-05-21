import { put, takeEvery, select } from 'redux-saga/effects';
import * as api from './api';
import actions from './actions';
import { curdSagas } from '../../../tools/CRUDHelper';
import { getExternailzeCurrentItem, getExternailzeRootState } from './selectors';
import { isMoney, validate, validator } from '../../../tools/validations/validators';


export function* createSuccess() {
	yield put(actions.fetchAllAction());
	yield put(push('/logistics/externalise'));
}

const validations = [
	validator('memo', 'Memo', memo => memo.length > 3 ? null : () => ({
		type: 'error',
		text: 'Memo field not long enough',
	})),
	validator('memo', 'Memo', memo => memo.length < 24 ? null : () => ({
		type: 'warning',
		text: 'Memo field too long',
	})),
	validator('externaliseline_set', 'Externalize set', set => set.reduce((accumulator, current) => accumulator && isMoney(current.amount.amount), true) ? null : () => ({
		type: 'error',
		text: 'Some money input is invalid.',
	})),
	validator('externaliseline_set', 'Externalize set', set => set.reduce((accumulator, current) => accumulator && current.count > 0, true) ? null : () => ({
		type: 'error',
		text: 'Some product count is invalid.',
	})),
	validator('externaliseline_set', 'Externalize set', set => set.reduce((accumulator, current) => accumulator && current.article, true) ? null : () => ({
		type: 'error',
		text: 'Some product is not set.',
	})),
];

export function* externalizeValidator() {
	const current = yield select(getExternailzeCurrentItem);
	const res = validate(current, validations);

	yield put(actions.setValidations(res));
}

export default function* saga() {
	yield curdSagas('logistics/externalise', api, getExternailzeRootState);
	yield takeEvery(actions.SET_FIELD, externalizeValidator);
}
