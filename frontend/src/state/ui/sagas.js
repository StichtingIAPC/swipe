import {takeEvery} from "redux-saga/es/effects";
import * as actions from "./actions";
import {put} from "redux-saga/effects";
import swal from 'sweetalert';

export function* areYouSureSaga(action) {
	const ok = yield(swal({
		title: "Are you sure?",
		text: action.text,
		icon: "warning",
		buttons: true,
		dangerMode: true,
	}));
	if (ok) {
		yield put(actions.toastAction(action.successText));
		yield put(action.action);
	} else {
		yield put(actions.toastAction(action.failureText));
	}
}

export function* toastSaga(action) {
	if (action.text !== "")
		yield swal(action.text);
}

export default function* saga() {
	yield takeEvery(actions.ARE_YOU_SURE_ACTION, areYouSureSaga);
	yield takeEvery(actions.TOAST_ACTION, toastSaga);
}
