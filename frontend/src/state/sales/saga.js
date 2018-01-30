import commitSaga from './commit/saga.js';


export default function* saga() {
	yield* commitSaga();
}
