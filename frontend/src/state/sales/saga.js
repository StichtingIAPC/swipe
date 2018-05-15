import paymentsSaga from './payments/saga.js';

export default function* saga() {
	yield* paymentsSaga();
}
