import { booleanControlReducer, setFieldReducer } from './reducerComponents';
import { call, put, takeEvery } from 'redux-saga/effects';

function trim(path) {
	return path.replace(/^\//, '')
		.replace(/\/$/, '');
}

export function crudActions(rawPath) {
	const path = trim(rawPath);

	return {
		CREATE_FAIL: `${path}/create/fail`,
		CREATE_FINALLY: `${path}/create/finally`,
		CREATE_START: `${path}/create/start`,
		CREATE_SUCCESS: `${path}/create/success`,
		CREATE_SET_LOADING: `${path}/fetchAll/setLoading`,
		DELETE_FAIL: `${path}/delete/fail`,
		DELETE_FINALLY: `${path}/delete/finally`,
		DELETE_START: `${path}/delete/start`,
		DELETE_SUCCESS: `${path}/delete/success`,
		DELETE_SET_LOADING: `${path}/fetchAll/setLoading`,
		FETCH_ALL_FAIL: `${path}/fetchAll/fail`,
		FETCH_ALL_FINALLY: `${path}/fetchAll/finally`,
		FETCH_ALL_START: `${path}/fetchAll/start`,
		FETCH_ALL_SUCCESS: `${path}/fetchAll/success`,
		FETCH_ALL_SET_LOADING: `${path}/fetchAll/setLoading`,
		FETCH_FAIL: `${path}/fetch/fail`,
		FETCH_FINALLY: `${path}/fetch/finally`,
		FETCH_START: `${path}/fetch/start`,
		FETCH_SUCCESS: `${path}/fetch/success`,
		FETCH_SET_LOADING: `${path}/fetchAll/setLoading`,
		UPDATE_FAIL: `${path}/update/fail`,
		UPDATE_FINALLY: `${path}/update/finally`,
		UPDATE_START: `${path}/update/start`,
		UPDATE_SUCCESS: `${path}/update/success`,
		UPDATE_SET_LOADING: `${path}/fetchAll/setLoading`,
		SET_FIELD: `${path}/setField`,
	};
}

export function crudFunctions(rawPath) {
	const path = trim(rawPath);

	return {
		createStart: () => ({
			type: `${path}/create/start`,
		}),
		createSuccess: data => ({
			type: `${path}/create/success`,
			data,
		}),
		createFail: reason => ({
			type: `${path}/create/fail`,
			reason,
		}),
		createFinally: () => ({
			type: `${path}/create/finally`,
		}),
		createSetLoading: (isLoading = true) => ({
			type: `${path}/create/setLoading`,
			isLoading,
		}),
		deleteStart: () => ({
			type: `${path}/delete/start`,
		}),
		deleteSuccess: data => ({
			type: `${path}/delete/success`,
			data,
		}),
		deleteFail: reason => ({
			type: `${path}/delete/fail`,
			reason,
		}),
		deleteFinally: () => ({
			type: `${path}/delete/finally`,
		}),
		deleteSetLoading: (isLoading = true) => ({
			type: `${path}/delete/setLoading`,
			isLoading,
		}),
		updateStart: () => ({
			type: `${path}/update/start`,
		}),
		updateSuccess: data => ({
			type: `${path}/update/success`,
			data,
		}),
		updateFail: reason => ({
			type: `${path}/update/fail`,
			reason,
		}),
		updateFinally: () => ({
			type: `${path}/update/finally`,
		}),
		updateSetLoading: (isLoading = true) => ({
			type: `${path}/update/setLoading`,
			isLoading,
		}),
		fetchAll: () => ({
			type: `${path}/fetchAll/start`,
		}),
		fetchAllSuccess: data => ({
			type: `${path}/fetchAll/success`,
			data,
		}),
		fetchAllFail: reason => ({
			type: `${path}/fetchAll/fail`,
			reason,
		}),
		fetchAllFinally: () => ({
			type: `${path}/fetchAll/finally`,
		}),
		fetchAllSetLoading: (isLoading = true) => ({
			type: `${path}/fetchAll/setLoading`,
			isLoading,
		}),
		fetch: () => ({
			type: `${path}/fetch/start`,
		}),
		fetchSuccess: data => ({
			type: `${path}/fetch/success`,
			data,
		}),
		fetchFail: reason => ({
			type: `${path}/fetch/fail`,
			reason,
		}),
		fetchFinally: () => ({
			type: `${path}/fetch/finally`,
		}),
		fetchSetLoading: (isLoading = true) => ({
			type: `${path}/fetch/setLoading`,
			isLoading,
		}),
	};
}


export function crudReducers(path, manyName = 'items', singleName = 'currentItem') {
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
}

export function curdSagas(path, api) {
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
		fetchAll: function* () {
			yield takeEvery(actions.FETCH_ALL_START, fetchAllSaga);
		},
		fetch: function* () {
			yield takeEvery(actions.FETCH_START, fetchSaga);
		},
		create: function* () {
			yield takeEvery(actions.CREATE_START, createSaga);
		},
		update: function* () {
			yield takeEvery(actions.UPDATE_START, updateSaga);
		},
		delete: function* () {
			yield takeEvery(actions.DELETE_START, deleteSaga);
		},
	};
}
