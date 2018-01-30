import articleSaga from './articles/saga.js';
import labelTypeSaga from './label-types/saga.js';
import unitTypeSaga from './unit-types/saga.js';

export default function* assortmentSaga() {
	yield* articleSaga();
	yield* labelTypeSaga();
	yield* unitTypeSaga();
}
