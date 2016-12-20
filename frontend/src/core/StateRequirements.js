/**
 * Created by Matthias on 28/11/2016.
 */

export function connectMixin(requirements, state = null) {
	function func(_state) {
		const missingRequirements = Object.entries(requirements)
			.filter((entry) => _state[entry[0]][entry[0]].length == 0);
		return {
			requirementsLoaded: missingRequirements.length == 0,
			missingRequirements: missingRequirements,
		}
	}

	if (state != null) { // case connect((state) => ({...connectMixin(requirements, state)}))
		return func(state);
	} else { // case connect(connectMixin(requirements))
		return func;
	}
}

export function fetchStateRequirementsFor(obj) {
	if (obj.props.requirementsLoaded) {
		return;
	}
	obj.props.missingRequirements
		.forEach(
			(entry) => obj.props.dispatch(entry[1]())
		);
}
