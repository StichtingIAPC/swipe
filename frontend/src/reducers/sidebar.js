const initialState = false;

export default function(state = initialState, action) {
	if (action.type === 'SIDEBAR_TOGGLE') return !state;
	if (action.type === 'SIDEBAR_CLOSE') return false;
	if (action.type === 'SIDEBAR_OPEN') return true;
	return state;
}
