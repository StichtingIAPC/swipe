import accountingGroupSaga from './accounting-groups/saga.js';
import currencieSaga from './currencies/saga.js';
import vatSaga from './vat/saga.js';

export default function* moneySagas() {
	yield* accountingGroupSaga();
	yield* currencieSaga();
	yield* vatSaga();
}
