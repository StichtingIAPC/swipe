import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
import LabelTypeList from './labeltype/LabelTypeList';
import UnitTypeList from './unittype/UnitTypeList';
import { connectMixin, fetchStateRequirementsFor } from '../../../core/stateRequirements';
import { labelTypes } from '../../../state/assortment/label-types/actions.js';
import { unitTypes } from '../../../state/assortment/unit-types/actions.js';
import LabelTypeEdit from './labeltype/LabelTypeEdit';
import LabelTypeDetail from './labeltype/LabelTypeDetail';
import UnitTypeEdit from './unittype/UnitTypeEdit';
import UnitTypeDetail from './unittype/UnitTypeDetail';

class LabelsModal extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		const { match } = this.props;

		return (
			<div className="row">
				<div className="col-sm-4">
					<Route route={`${match.path}/labeltype/:id`} render={({ id }) => <LabelTypeList activeID={id} /> } />
					<Route route={`${match.path}/unittype/:id`} render={({ id }) => <UnitTypeList activeID={id} /> } />
				</div>
				<div className="col-sm-8">
					{
						this.props.requirementsLoaded ? (
							<Switch>
								<Route path={`${match.path}/labeltype/create`} component={LabelTypeEdit} />
								<Route path={`${match.path}/labeltype/:id/edit`} component={LabelTypeEdit} />
								<Route path={`${match.path}/labeltype/:id`} component={LabelTypeDetail} />
								<Route path={`${match.path}/unittype/create`} component={UnitTypeEdit} />
								<Route path={`${match.path}/unittype/:id/edit`} component={UnitTypeEdit} />
								<Route path={`${match.path}/unittype/:id`} component={UnitTypeDetail} />
							</Switch>
						) : null
					}
				</div>
			</div>
		);
	}
}

export default connect(
	connectMixin({
		assortment: {
			labelTypes,
			unitTypes,
		},
	}),
)(LabelsModal);
