import React from "react";
import { Link } from "react-router";
import { connect } from "react-redux";
import LabelTypeList from "./labeltype/LabelTypeList";
import UnitTypeList from "./unittype/UnitTypeList";
import { connectMixin, fetchStateRequirementsFor } from "../../core/stateRequirements";
import { labelTypes } from "../../actions/assortment/labelTypes";
import { unitTypes } from "../../actions/assortment/unitTypes";

class LabelsModal extends React.Component {
	componentWillMount() {
		fetchStateRequirementsFor(this);
	}

	render() {
		return (
			<div  className="row">
				<div className="col-sm-4">
					<LabelTypeList activeID={this.props.labelTypeID} />
					<UnitTypeList activeID={this.props.unitTypeID} />
				</div>
				<div className="col-sm-8">
					{this.props.requirementsLoaded ? this.props.children : null}
				</div>
			</div>
		)
	}
}

export default connect(
	connectMixin({
		labelTypes,
		unitTypes,
	}),
)(LabelsModal);
