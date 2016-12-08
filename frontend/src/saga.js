import {takeEvery} from "redux-saga";
import {login} from "./sagas/auth.js";
import {populateSuppliers, createSupplier, updateSupplier} from "./sagas/suppliers";

export default function* rootSaga() {
	yield takeEvery('AUTH_START_LOGIN', login);
	yield takeEvery('SUPPLIER_POPULATE_SUPPLIERS', populateSuppliers);
	yield takeEvery('SUPPLIER_CREATE_SUPPLIER', createSupplier);
	yield takeEvery('SUPPLIER_UPDATE_SUPPLIER', updateSupplier);
};
