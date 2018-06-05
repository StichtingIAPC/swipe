import assortmentSaga from './assortment/saga.js';
import { saga as authSaga } from './auth/saga.js';
import moneySaga from './money/saga.js';
import registerSaga from './register/saga.js';
import suppliersSaga from './suppliers/saga.js';
import stockSaga from './stock/saga.js';
import logisticsSaga from './logistics/saga.js';
import uiSaga from './ui/sagas.js';
import crmSaga from './crm/sagas.js';
import salesSaga from './sales/saga.js';

export default function* saga() {
	yield* assortmentSaga();
	yield* authSaga();
	yield* crmSaga();
	yield* moneySaga();
	yield* registerSaga();
	yield* suppliersSaga();
	yield* salesSaga();
	yield* stockSaga();
	yield* logisticsSaga();
	yield* uiSaga();
}
