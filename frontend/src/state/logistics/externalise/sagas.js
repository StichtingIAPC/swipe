import {call, put, takeEvery, takeLatest, select} from 'redux-saga/effects';
import {push} from 'react-router-redux';
import store from '../../store';

import * as api from '../../../api';
import * as actions from './actions.js';
import {
    FETCH_ALL_ACTION,
    CREATE_ACTION,
    CREATE_SUCCESS,
    fetchAllAction as fetchAllExternalises,
    SET_FIELD_ACTION, setValidations
} from './actions';
import {cleanErrorMessage} from '../../../tools/sagaHelpers';
import {getExternalisationActiveObject} from "./selectors";
import {validate, validator} from "../../../tools/validations/validators";

export function* fetchAll() {
    console.log("Fuck!");
    try {
        const externalizations = yield (yield call(
            api.get,
            '/externalise/',
        )).json();

        const exts = [].concat.apply([], externalizations.map(e => e.externaliseline_set.map(en => ({
            memo: e.memo,
            count: en.count,
            amount: en.cost,
            article: en.article_type,
        }))));

        yield put(actions.fetchAllSuccess(exts));
    } catch (e) {
        console.log(e);
        yield put(actions.fetchAllError(e));
    } finally {
        yield put(actions.fetchAllFinally());
    }
}

export function* create({externalise}) {
    const document = {
        externaliseline_set: externalise.externaliseline_set.map(e => ({
            ...e,
            // eslint-disable-next-line
            amount: undefined,
            cost: e.amount,
            article: e.article.id,
        })),
        memo: externalise.memo,
        user: store.getState().auth.currentUser.id,
    };

    try {
        const newExternalise = yield (yield call(
            api.post,
            '/externalise/',
            document,
        )).json();

        yield put(actions.createSuccess(newExternalise));
    } catch (e) {
        yield put(actions.createError(cleanErrorMessage(e)));
    } finally {
        yield put(actions.createFinally());
    }
}

export function* createSuccess() {
    yield put(fetchAllExternalises());
    yield put(push('/logistics/externalise'));
}

const validations = [
    validator('memo', 'Memo', (memo) => memo.length > 3 ? null : () => 'Memo field not long enough'),
    validator('memo', 'Memo', (memo) => memo.length < 9 ? null : () => 'Memo field too long')
];

export function* externalizeValidator() {
    const current = yield select(getExternalisationActiveObject);
    const res = validate(current, validations);
    console.log(res);
    yield put(actions.setValidations(res));
}

export default function* saga() {
    yield takeEvery(SET_FIELD_ACTION, externalizeValidator);
    yield takeLatest(FETCH_ALL_ACTION, fetchAll);
    yield takeEvery(CREATE_ACTION, create);
    yield takeLatest(CREATE_SUCCESS, createSuccess);
}
