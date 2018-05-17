import { booleanControlReducer, setFieldReducer } from './reducerComponents';
import { call, put, takeEvery } from 'redux-saga/effects';

function trim(path) {
	return path.replace(/^\//, '')
		.replace(/\/$/, '');
}

export function crudActions(path) {
	return {
		CREATE_FAIL: `${trim(path)}/create/fail`,
		CREATE_FINALLY: `${trim(path)}/create/finally`,
		CREATE_START: `${trim(path)}/create/start`,
		CREATE_SUCCESS: `${trim(path)}/create/success`,
		CREATE_SET_LOADING: `${trim(path)}/fetchAll/setLoading`,
		DELETE_FAIL: `${trim(path)}/delete/fail`,
		DELETE_FINALLY: `${trim(path)}/delete/finally`,
		DELETE_START: `${trim(path)}/delete/start`,
		DELETE_SUCCESS: `${trim(path)}/delete/success`,
		DELETE_SET_LOADING: `${trim(path)}/fetchAll/setLoading`,
		FETCH_ALL_FAIL: `${trim(path)}/fetchAll/fail`,
		FETCH_ALL_FINALLY: `${trim(path)}/fetchAll/finally`,
		FETCH_ALL_START: `${trim(path)}/fetchAll/start`,
		FETCH_ALL_SUCCESS: `${trim(path)}/fetchAll/success`,
		FETCH_ALL_SET_LOADING: `${trim(path)}/fetchAll/setLoading`,
		FETCH_FAIL: `${trim(path)}/fetch/fail`,
		FETCH_FINALLY: `${trim(path)}/fetch/finally`,
		FETCH_START: `${trim(path)}/fetch/start`,
		FETCH_SUCCESS: `${trim(path)}/fetch/success`,
		FETCH_SET_LOADING: `${trim(path)}/fetchAll/setLoading`,
		UPDATE_FAIL: `${trim(path)}/update/fail`,
		UPDATE_FINALLY: `${trim(path)}/update/finally`,
		UPDATE_START: `${trim(path)}/update/start`,
		UPDATE_SUCCESS: `${trim(path)}/update/success`,
		UPDATE_SET_LOADING: `${trim(path)}/fetchAll/setLoading`,
		SET_FIELD: `${trim(path)}/setField`,
	};
}

export function crudFunctions(path) {
	return {
		createStart: () => ({
			type: `${trim(path)}/create/start`,
		}),
		createSuccess: data => ({
			type: `${trim(path)}/create/success`,
			data,
		}),
		createFail: reason => ({
			type: `${trim(path)}/create/fail`,
			reason,
		}),
		createFinally: () => ({
			type: `${trim(path)}/create/finally`,
		}),
		createSetLoading: (isLoading = true) => ({
			type: `${trim(path)}/create/setLoading`,
			isLoading,
		}),
		deleteStart: () => ({
			type: `${trim(path)}/delete/start`,
		}),
		deleteSuccess: data => ({
			type: `${trim(path)}/delete/success`,
			data,
		}),
		deleteFail: reason => ({
			type: `${trim(path)}/delete/fail`,
			reason,
		}),
		deleteFinally: () => ({
			type: `${trim(path)}/delete/finally`,
		}),
		deleteSetLoading: (isLoading = true) => ({
			type: `${trim(path)}/delete/setLoading`,
			isLoading,
		}),
		updateStart: () => ({
			type: `${trim(path)}/update/start`,
		}),
		updateSuccess: data => ({
			type: `${trim(path)}/update/success`,
			data,
		}),
		updateFail: reason => ({
			type: `${trim(path)}/update/fail`,
			reason,
		}),
		updateFinally: () => ({
			type: `${trim(path)}/update/finally`,
		}),
		updateSetLoading: (isLoading = true) => ({
			type: `${trim(path)}/update/setLoading`,
			isLoading,
		}),
		fetchAll: () => ({
			type: `${trim(path)}/fetchAll/start`,
		}),
		fetchAllSuccess: data => ({
			type: `${trim(path)}/fetchAll/success`,
			data,
		}),
		fetchAllFail: reason => ({
			type: `${trim(path)}/fetchAll/fail`,
			reason,
		}),
		fetchAllFinally: () => ({
			type: `${trim(path)}/fetchAll/finally`,
		}),
		fetchAllSetLoading: (isLoading = true) => ({
			type: `${trim(path)}/fetchAll/setLoading`,
			isLoading,
		}),
		fetch: () => ({
			type: `${trim(path)}/fetch/start`,
		}),
		fetchSuccess: data => ({
			type: `${trim(path)}/fetch/success`,
			data,
		}),
		fetchFail: reason => ({
			type: `${trim(path)}/fetch/fail`,
			reason,
		}),
		fetchFinally: () => ({
			type: `${trim(path)}/fetch/finally`,
		}),
		fetchSetLoading: (isLoading = true) => ({
			type: `${trim(path)}/fetch/setLoading`,
			isLoading,
		}),
	};
}

export const curdReducers = (path, manyName = 'items', singleName = 'currentItem') => {
	const actions = crudActions(path);

	return {
		[manyName]: {
			data: setFieldReducer([
				actions.FETCH_ALL_SUCCESS,
			], [], 'data'),
			isLoading: booleanControlReducer({
				[actions.FETCH_ALL_SET_LOADING]: true,
				[actions.FETCH_ALL_FINALLY]: false,
			}, false),
			isPopulated: booleanControlReducer({
				[actions.FETCH_ALL_SUCCESS]: true,
			}, false),
			error: setFieldReducer([
				actions.FETCH_ALL_FAIL,
			], null, 'reason'),
		},
		[singleName]: {
			data: setFieldReducer([
				actions.FETCH_SUCCESS,
			], null, 'data'),
			isLoading: booleanControlReducer({
				[actions.FETCH_SET_LOADING]: true,
				[actions.FETCH_FINALLY]: false,
			}, false),
			isPopulated: booleanControlReducer({
				[actions.FETCH_SUCCESS]: true,
			}, false),
			error: setFieldReducer([
				actions.FETCH_FAIL,
			], null, 'reason'),
		},
	};
};

export const curdSagas = (path, api) => {
	const actions = crudActions(path);

	const fetchSaga = function* ({ id }) {
		yield put(actions.fetchAllSetLoading());
		try {
			const data = yield (yield call(api.get, id)).json();

			yield put(actions.fetchSuccess(data));
		} catch (e) {
			yield put(actions.fetchFail(e));
		} finally {
			yield put(actions.fetchFinally());
		}
	};

	const fetchAllSaga = function* () {
		yield put(actions.fetchSetLoading());
		try {
			const data = yield (yield call(api.getAll)).json();

			yield put(actions.fetchAllSuccess(data));
		} catch (e) {
			yield put(actions.fetchAllFail(e));
		} finally {
			yield put(actions.fetchAllFinally());
		}
	};

	const createSaga = function* ({ data }) {
		yield put(actions.createSetLoading());
		try {
			const backendData = yield (yield call(api.create, data)).json();

			yield put(actions.createSuccess(backendData));
		} catch (e) {
			yield put(actions.createFail(e));
		} finally {
			yield put(actions.createFinally());
		}
	};

	const updateSaga = function* ({ id, data }) {
		yield put(actions.updateSetLoading());
		try {
			const backendData = yield (yield call(api.update, id, data)).json();

			yield put(actions.updateSuccess(backendData));
		} catch (e) {
			yield put(actions.updateFail(e));
		} finally {
			yield put(actions.updateFinally());
		}
	};

	const deleteSaga = function* ({ id, data }) {
		yield put(actions.deleteSetLoading());
		try {
			const backendData = yield (yield call(api.get, id, data)).json();

			yield put(actions.deleteSuccess(backendData));
		} catch (e) {
			yield put(actions.deleteFail(e));
		} finally {
			yield put(actions.deleteFinally());
		}
	};

	return {
		all: function* () {
			yield takeEvery(actions.FETCH_ALL_START, fetchAllSaga);
			yield takeEvery(actions.FETCH_START, fetchSaga);
			yield takeEvery(actions.CREATE_START, createSaga);
			yield takeEvery(actions.UPDATE_START, updateSaga);
			yield takeEvery(actions.DELETE_START, deleteSaga);
		},
		fetchAll: function* () { yield takeEvery(actions.FETCH_ALL_START, fetchAllSaga); },
		fetch: function* () { yield takeEvery(actions.FETCH_START, fetchSaga); },
		create: function* () { yield takeEvery(actions.CREATE_START, createSaga); },
		update: function* () { yield takeEvery(actions.UPDATE_START, updateSaga); },
		delete: function* () { yield takeEvery(actions.DELETE_START, deleteSaga); },
	};
};


console.dir(crudActions('/logistics/externalize/'));
console.dir(crudFunctions('/logistics/externalize/'));
console.dir(curdReducers('/logistics/externalize/'));
console.dir(curdSagas('/logistics/externalize/'));
