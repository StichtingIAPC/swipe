import externaliseSaga from './externalise/sagas.js';

export default function* saga() {
	yield* externaliseSaga();
}