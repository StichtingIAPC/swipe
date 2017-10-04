import assortmentSaga from './assortment/saga.js';
import authSaga from './auth/saga.js';
import moneySaga from './money/saga.js';
import registerSaga from './register/saga.js';
import suppliersSaga from './suppliers/saga.js';

export default function* saga() {
	yield* assortmentSaga();
	yield* authSaga();
	yield* moneySaga();
	yield* registerSaga();
	yield* suppliersSaga();
}
