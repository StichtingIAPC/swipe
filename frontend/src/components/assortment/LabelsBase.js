import React from 'react';
import { connect } from 'react-redux';
import { Switch, Route } from 'react-router-dom';
import LabelTypeList from './labeltype/LabelTypeList';
import UnitTypeList from './unittype/UnitTypeList';
import { connectMixin, fetchStateRequirementsFor } from '../../core/stateRequirements';
import { labelTypes } from '../../state/assortment/label-types/actions.js';
import { unitTypes } from '../../state/assortment/unit-types/actions.js';
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
					<LabelTypeList activeID={this.props.labelTypeID} />
					<UnitTypeList activeID={this.props.unitTypeID} />
				</div>
				<div className="col-sm-8">
					{
						this.props.requirementsLoaded ? (
							<Switch>
								<Route path={`${match.path}labeltype/create`} component={LabelTypeEdit} />
								<Route path={`${match.path}labeltype/:labelTypeID/edit`} component={LabelTypeEdit} />
								<Route path={`${match.path}labeltype/:labelTypeID`} component={LabelTypeDetail} />
								<Route path={`${match.path}unittype/create`} component={UnitTypeEdit} />
								<Route path={`${match.path}unittype/:unitTypeID/edit`} component={UnitTypeEdit} />
								<Route path={`${match.path}unittype/:unitTypeID`} component={UnitTypeDetail} />
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
