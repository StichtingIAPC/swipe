import rootSaga from './state/saga.js';

export default function* saga() {
	yield* rootSaga();
}
