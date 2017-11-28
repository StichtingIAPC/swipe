let LOG = true;


const isAvailableRecursively = ([ name, functor ], state = {}) => {
	const stateComponent = state[name];

	if (typeof functor === 'function') {
		const loaded = !!stateComponent && !!stateComponent.populated;

		if (LOG) {
			console.log(`name: "${name}" loaded: ${loaded}`);
		}
		return loaded;
	}

	return Object.entries(functor)
		.map(entry => [ entry[0], isAvailableRecursively(entry, stateComponent) ])
		.reduce((sum, [ _name, _value ]) => ({
			...sum,
			[_name]: _value,
		}), {});
};

const fetchMissingRecursively = ([ name, functor ], tree = {}, dispatch) => {
	const treeComponent = tree[name];

	if (typeof functor === 'function') {
		if (!treeComponent) {
			dispatch(functor());
			if (LOG) {
				console.log(`started fetching requirements for "${name}"`);
			}
		}
		return;
	}

	Object.entries(functor)
		.map(entry => fetchMissingRecursively(entry, treeComponent, dispatch));
};

const hasMissingDependencies = obj => Object.entries(obj)
	.some(([ , value ]) => {
		if (typeof value === 'boolean') { return value; }
		return hasMissingDependencies(value);
	});

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
 * @param _state: {Object?}
 * @returns {Func|{requirementsLoaded: boolean, missingRequirements: Array<[String, Function]>}}
 */
export function connectMixin(requirements, _state = null) {
	/**
	 * @callback Func
	 * @param state: {Object}
	 * @returns {{
	 *   availableRequirements: Object,
	 *   fetchMissingFor: Function,
	 *   fetchAllFor: Function,
	 *   requirementsLoaded: boolean,
	 * }}
	 */
	function func(state) {
		const availableRequirements = isAvailableRecursively([ 'state', requirements ], { state });

		return {
			availableRequirements,
			requirementsLoaded: hasMissingDependencies(availableRequirements),
			fetchMissingFor: obj => fetchMissingRecursively(
				[ 'availableRequirements', requirements ],
				{ availableRequirements },
				obj.props.dispatch
			),
			fetchAllFor: obj => fetchMissingRecursively(
				[ 'all', requirements ],
				{},
				obj.props.dispatch,
			),
		};
	}

	// case connect((state) => ({...connectMixin(requirements, state)}))
	if (_state !== null) {
		return func(_state);
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

	obj.props.fetchMissingFor(obj);
}
