import { takeEvery, takeLatest } from 'redux-saga';
import { createLabelType, fetchLabelTypes, updateLabelType } from './labelTypes';
import { createUnitType, fetchUnitTypes, updateUnitType } from './unitTypes';

export default function* assortmentSagas() {
	yield takeLatest('LABEL_TYPE_FETCH_START', fetchLabelTypes);
	yield takeEvery('LABEL_TYPE_CREATE', createLabelType);
	yield takeEvery('LABEL_TYPE_UPDATE', updateLabelType);

	yield takeLatest('UNIT_TYPE_FETCH_START', fetchUnitTypes);
	yield takeEvery('UNIT_TYPE_CREATE', createUnitType);
	yield takeEvery('UNIT_TYPE_UPDATE', updateUnitType);
}
