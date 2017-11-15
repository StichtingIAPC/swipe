import stockSaga from './stock/saga.js';


export default function* salesSaga() {
	yield* stockSaga();
}
