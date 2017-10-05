/**
 * This function checks if the requirements of a component are loaded, and
 * returns the following:
 *
 * If `state` is not set, it will return an Object which has the fields
 *    requirementsLoaded: a boolean that indicates all specified requirements are loaded, and
 *    missingRequirements: an array that contains the names of any missing requirements
 *
 * If `state` is set (the global state), it will directly return an array which contains
 *    (string, callable) pairs.
 *
 * Usage of this method is to insert requirement validation into the component's properties.
 *
 * Example:
 *
 * connect(
 *   connectMixin({
 *     requirementName: fetchRequirementAction,
 *     fetchRequirementActionButAlsoRequirementName,
 *     ..etc
 *   })
 * )
 *
 * connect(
 *   (state) => {
 *     ...connectMixin({
 *       requirement_name: fetchRequirementAction,
 *       fetchRequirementActionButAlsoRequirementName,
 *       ..etc
 *     })
 *   }
 * )
 *
 * @param requirements: {Object<String, Function>}
 * @param state: {Object?}
 * @returns {Func|{requirementsLoaded: boolean, missingRequirements: Array<[String, Function]>}}
 */
export function connectMixin(requirements, state = null) {
	/**
	 * @callback Func
	 * @param _state: {Object}
	 * @returns {{requirementsLoaded: boolean, missingRequirements: Array<[String, Function]>}}
	 */
	function func(_state) {
		const missingRequirements = Object.entries(requirements)
			.filter(entry => !!_state[entry[0]] && !_state[entry[0]][entry[0]]);

		return {
			requirementsLoaded: missingRequirements.length === 0,
			missingRequirements,
			reloadRequirements: obj => Object.values(requirements).map(fun => obj.props.dispatch(fun)),
		};
	}

	// case connect((state) => ({...connectMixin(requirements, state)}))
	if (state !== null) {
		return func(state);
	}

	// case connect(connectMixin(requirements))
	return func;
}

/**
 * This function uses the metadata on the props of `obj` to dispatch the requirement fetchers of
 * said component.
 * @param obj: Component
 */
export function fetchStateRequirementsFor(obj) {
	if (obj.props.requirementsLoaded) {
		return;
	}

	obj.props.missingRequirements
		.forEach(
			entry => obj.props.dispatch(entry[1]())
		);
}
