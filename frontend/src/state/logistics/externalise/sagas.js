import { put, takeEvery, select } from 'redux-saga/effects';
import * as api from './api';
import actions from './actions';
import { crudSagas } from '../../../tools/CRUDHelper';
import { getExternailseCurrentItem, getExternaliseRootState } from './selectors';
import { isMoney, validate, validator } from '../../../tools/validations/validators';
import { push } from 'react-router-redux';


export function* createSuccess() {
	yield put(actions.fetchAllStart());
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
	validator('externaliseline_set', 'Externalise set', set => set.reduce((accumulator, current) => accumulator && isMoney(current.amount.amount), true) ? null : () => ({
		type: 'error',
		text: 'Some money input is invalid.',
	})),
	validator('externaliseline_set', 'Externalise set', set => set.reduce((accumulator, current) => accumulator && current.count > 0, true) ? null : () => ({
		type: 'error',
		text: 'Some product count is invalid.',
	})),
	validator('externaliseline_set', 'Externalise set', set => set.reduce((accumulator, current) => accumulator && current.article, true) ? null : () => ({
		type: 'error',
		text: 'Some product is not set.',
	})),
];

export function* externaliseValidator() {
	const current = yield select(getExternailseCurrentItem);
	const res = validate(current, validations);

	yield put(actions.setValidations(res));
}

export default function* saga() {
	yield* crudSagas('logistics/externalise', api, getExternaliseRootState)();
	yield takeEvery(actions.SET_FIELD, externaliseValidator);
	yield takeEvery(actions.CREATE_SUCCESS, createSuccess);
}
