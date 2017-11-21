import paymentTypeSaga from './payment-types/saga';
import registerSaga from './registers/saga';

export default function* saga() {
	yield* paymentTypeSaga();
	yield* registerSaga();
}
