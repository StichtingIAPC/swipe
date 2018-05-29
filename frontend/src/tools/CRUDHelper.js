import { booleanControlReducer, setFieldReducer, collectReducers, mergeObjects } from './reducerComponents';
import { call, put, takeEvery, select } from 'redux-saga/effects';
import { combineReducers } from 'redux';

/**
 * Removes beginning and trailing slashes, so I know what I'm dealing with.
 * @param path The original path, containing possibbly leading and/or trailing slashes
 * @returns {string} A string without leading and/or trailing slashes
 */
function trim(path) {
	return path.replace(/^\//, '')
		.replace(/\/$/, '');
}

/**
 * Generates all the action constants you will likely need for CRUD.
 * @param path The path of the part of state, this reducer is responsible for. Example: '/logistics/externalize/'
 * @returns {{CREATE_FAIL: string, CREATE_FINALLY: string, CREATE_START: string, CREATE_SUCCESS: string, CREATE_SET_LOADING: string, DELETE_FAIL: string, DELETE_FINALLY: string, DELETE_START: string, DELETE_SUCCESS: string, DELETE_SET_LOADING: string, FETCH_ALL_FAIL: string, FETCH_ALL_FINALLY: string, FETCH_ALL_START: string, FETCH_ALL_SUCCESS: string, FETCH_ALL_SET_LOADING: string, FETCH_FAIL: string, FETCH_FINALLY: string, FETCH_START: string, FETCH_SUCCESS: string, FETCH_SET_LOADING: string, UPDATE_FAIL: string, UPDATE_FINALLY: string, UPDATE_START: string, UPDATE_SUCCESS: string, UPDATE_SET_LOADING: string, SET_FIELD: string}}
 */
export function crudActions(path) {
	const trimmedPath = trim(path);

	return {
		CREATE_FAIL: `${trimmedPath}/create/fail`,
		CREATE_FINALLY: `${trimmedPath}/create/finally`,
		CREATE_START: `${trimmedPath}/create/start`,
		CREATE_SUCCESS: `${trimmedPath}/create/success`,
		CREATE_SET_LOADING: `${trimmedPath}/fetchAll/setLoading`,
		DELETE_FAIL: `${trimmedPath}/delete/fail`,
		DELETE_FINALLY: `${trimmedPath}/delete/finally`,
		DELETE_START: `${trimmedPath}/delete/start`,
		DELETE_SUCCESS: `${trimmedPath}/delete/success`,
		DELETE_SET_LOADING: `${trimmedPath}/fetchAll/setLoading`,
		FETCH_ALL_FAIL: `${trimmedPath}/fetchAll/fail`,
		FETCH_ALL_FINALLY: `${trimmedPath}/fetchAll/finally`,
		FETCH_ALL_START: `${trimmedPath}/fetchAll/start`,
		FETCH_ALL_SUCCESS: `${trimmedPath}/fetchAll/success`,
		FETCH_ALL_SET_LOADING: `${trimmedPath}/fetchAll/setLoading`,
		FETCH_FAIL: `${trimmedPath}/fetch/fail`,
		FETCH_FINALLY: `${trimmedPath}/fetch/finally`,
		FETCH_START: `${trimmedPath}/fetch/start`,
		FETCH_SUCCESS: `${trimmedPath}/fetch/success`,
		FETCH_SET_LOADING: `${trimmedPath}/fetchAll/setLoading`,
		UPDATE_FAIL: `${trimmedPath}/update/fail`,
		UPDATE_FINALLY: `${trimmedPath}/update/finally`,
		UPDATE_START: `${trimmedPath}/update/start`,
		UPDATE_SUCCESS: `${trimmedPath}/update/success`,
		UPDATE_SET_LOADING: `${trimmedPath}/fetchAll/setLoading`,
		SET_FIELD: `${trimmedPath}/setField`,
	};
}

/**
 * Generates all the action functions you will likely need for CRUD.
 * @param path  The path of the part of state, this reducer is responsible for. Example: '/logistics/externalize/'
 * @returns {{createStart: (function(): {type: string}), createSuccess: (function(*): {type: string, data: *}), createFail: (function(*): {type: string, reason: *}), createFinally: (function(): {type: string}), deleteStart: (function(): {type: string}), deleteSuccess: (function(*): {type: string, data: *}), deleteFail: (function(*): {type: string, reason: *}), deleteFinally: (function(): {type: string}), updateStart: (function(): {type: string}), updateSuccess: (function(*): {type: string, data: *}), updateFail: (function(*): {type: string, reason: *}), updateFinally: (function(): {type: string}), fetchAllStart: (function(): {type: string}), fetchAllSuccess: (function(*): {type: string, data: *}), fetchAllFail: (function(*): {type: string, reason: *}), fetchAllFinally: (function(): {type: string}), fetchAllSetLoading: (function(*=): {type: string, isLoading: *}), fetchStart: (function(): {type: string}), fetchSuccess: (function(*): {type: string, data: *}), fetchFail: (function(*): {type: string, reason: *}), fetchFinally: (function(): {type: string}), fetchSetLoading: (function(*=): {type: string, isLoading: *})}}
 */
export function crudFunctions(path) {
	const trimmedPath = trim(path);

	return {
		createStart: () => ({
			type: `${trimmedPath}/create/start`,
		}),
		createSuccess: data => ({
			type: `${trimmedPath}/create/success`,
			data,
		}),
		createFail: reason => ({
			type: `${trimmedPath}/create/fail`,
			reason,
		}),
		createFinally: () => ({
			type: `${trimmedPath}/create/finally`,
		}),
		deleteStart: () => ({
			type: `${trimmedPath}/delete/start`,
		}),
		deleteSuccess: data => ({
			type: `${trimmedPath}/delete/success`,
			data,
		}),
		deleteFail: reason => ({
			type: `${trimmedPath}/delete/fail`,
			reason,
		}),
		deleteFinally: () => ({
			type: `${trimmedPath}/delete/finally`,
		}),
		updateStart: () => ({
			type: `${trimmedPath}/update/start`,
		}),
		updateSuccess: data => ({
			type: `${trimmedPath}/update/success`,
			data,
		}),
		updateFail: reason => ({
			type: `${trimmedPath}/update/fail`,
			reason,
		}),
		updateFinally: () => ({
			type: `${trimmedPath}/update/finally`,
		}),
		fetchAllStart: () => ({
			type: `${trimmedPath}/fetchAll/start`,
		}),
		fetchAllSuccess: data => ({
			type: `${trimmedPath}/fetchAll/success`,
			data,
		}),
		fetchAllFail: reason => ({
			type: `${trimmedPath}/fetchAll/fail`,
			reason,
		}),
		fetchAllFinally: () => ({
			type: `${trimmedPath}/fetchAll/finally`,
		}),
		fetchAllSetLoading: (isLoading = true) => ({
			type: `${trimmedPath}/fetchAll/setLoading`,
			isLoading,
		}),
		fetchStart: () => ({
			type: `${trimmedPath}/fetch/start`,
		}),
		fetchSuccess: data => ({
			type: `${trimmedPath}/fetch/success`,
			data,
		}),
		fetchFail: reason => ({
			type: `${trimmedPath}/fetch/fail`,
			reason,
		}),
		fetchFinally: () => ({
			type: `${trimmedPath}/fetch/finally`,
		}),
		fetchSetLoading: (isLoading = true) => ({
			type: `${trimmedPath}/fetch/setLoading`,
			isLoading,
		}),
	};
}

/**
 * @typedef {Object} SingleDataset
 * @property {object} data
 * @property {boolean} isLoading
 * @property {boolean} isPopulated
 * @property {string} error
 */

/**
 * @typedef {Object} MultipleDataset
 * @property {array} data
 * @property {boolean} isLoading
 * @property {boolean} isPopulated
 * @property {string} error
 */

/**
 * @typedef {Object} CRUDReducers
 * @property {MultipleDataset} items (or what you changed it to)
 * @property {SingleDataset} currentItem (or what you changed it to)
 */

/**
 * Generares reducers for performing CRUD operations.
 * @param path The path of the part of state, this reducer is responsible for. Example: '/logistics/externalize/'
 * The reducers generated will catch actions generated by that path
 * @param manyName The field name for storing many items, which will be filled by the fetchAll method
 * @param singleName The field name for storing a single item, which will be used by the fetch-, create-, and updatemethod
 * @param customReducers if you want to have custom reducers for the {@code singleName} or {@code manyName} then put them here. Also any other reducers for this part of thate
 * can be here.
 * @returns CRUDReducers CRUD Reducers
 */
export function crudReducers(path, manyName, singleName, customReducers) {
	if (!path) {
		throw Error('Path required!');
	}
	if (!manyName) {
		throw Error('ManyName required!');
	}
	if (!singleName) {
		throw Error('SingleName required!');
	}

	const actions = crudActions(path);

	let generatedReducers = {
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

	const combinedReducers = {};

	if (customReducers) {
		// noinspection JSValidateTypes
		generatedReducers = mergeObjects(generatedReducers, customReducers, collectReducers);
	}

	for (const key in generatedReducers) {
		if (generatedReducers.hasOwnProperty(key)) {
			combinedReducers[key] = combineReducers(generatedReducers[key]);
		}
	}
	return combineReducers(combinedReducers);
}

/**
 * Generares sagas for performing CRUD operations.
 * @param path The path of the part of state, this reducer is responsible for. Example: '/logistics/externalize/'
 * The sagas generated will catch actions generated by that path
 * @param api The api object required by the sagas to make requests
 * @param baseSelector A selector that returns the part of that that the CRUDHelper will operate on
 * @param manyName Name for many items, has to match the manyName argument of the CRUDReducers to work
 * @param singleName Name for a single item, has to match the singleName argument of the CRUDReducers to work
 * @returns {{all: all, fetchAll: fetchAll, fetch: fetch, create: create, update: update, delete: delete}}
 */
export function curdSagas(path, api, baseSelector, manyName = 'items', singleName = 'currentItem') {
	const actions = crudActions(path);

	const fetchAllSaga = function* () {
		if (yield select(state => baseSelector(state)[manyName].isLoading)) {
			return;
		}
		yield put(actions.fetchAllSetLoading());
		try {
			const data = yield (yield call(api.getAll)).json();

			yield put(actions.fetchAllSuccess(data));
		} catch (e) {
			yield put(actions.fetchAllFail(e));
		} finally {
			yield put(actions.fetchAllFinally());
		}
	};

	const fetchSaga = function* ({ id }) {
		if (yield select(state => baseSelector(state)[singleName].isLoading)) {
			return;
		}
		yield put(actions.fetchSetLoading());
		try {
			const data = yield (yield call(api.get, id)).json();

			yield put(actions.fetchSuccess(data));
		} catch (e) {
			yield put(actions.fetchFail(e));
		} finally {
			yield put(actions.fetchFinally());
		}
	};

	const createSaga = function* ({ data }) {
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
