import commitSaga from './commit/saga.js';
import paymentsSaga from './payments/saga.js';

export default function* saga() {
	yield* commitSaga();
	yield* paymentsSaga();
}
