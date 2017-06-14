const STEPS = [ 'client', 'cart', 'coin', 'care' ];

export default function stepReducer(state = STEPS[0], action) {
	if (action.type === 'REGISTER_NEXT_STEP') return {
		...state,
		step: STEPS[STEPS.indexOf(state.step) + 1],
	};
	return state;
};
