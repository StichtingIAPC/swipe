import { takeLatest, takeEvery } from "redux-saga";
import { fetchLabelTypes, createLabelType, updateLabelType } from "./labelTypes";
import { fetchUnitTypes, createUnitType, updateUnitType } from "./unitTypes";

export default function* assortmentSagas() {
	yield takeLatest('LABEL_TYPE_FETCH_START', fetchLabelTypes);
	yield takeEvery('LABEL_TYPE_CREATE', createLabelType);
	yield takeEvery('LABEL_TYPE_UPDATE', updateLabelType);

	yield takeLatest('UNIT_TYPE_FETCH_START', fetchUnitTypes);
	yield takeEvery('UNIT_TYPE_CREATE', createUnitType);
	yield takeEvery('UNIT_TYPE_UPDATE', updateUnitType);
}
