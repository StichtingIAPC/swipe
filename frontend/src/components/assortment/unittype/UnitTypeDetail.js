import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router";
import FontAwesome from "../../tools/icons/FontAwesome";
import { valueTypes, incrementalTypes } from "../../../constants/assortment";

class UnitTypeDetail extends React.Component {
	render() {
		const unitType = this.props.unitType;
		return (
			<div className="box">
				<div className="box-header with-border">
					<h3 className="box-title">Supplier: {unitType.name}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to="/assortment/" className="btn btn-default btn-sm" title="Close"><FontAwesome icon="close" /></Link>
								<Link to={`/assortment/unittype/${unitType.id}/edit/`} className="btn btn-default btn-sm" title="Edit"><FontAwesome icon="edit" /></Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<dl className="dl-horizontal">
						{['type_long', 'type_short'].map(
							(key) => (
								<div key={key}>
									<dt>{key}</dt>
									<dd>{String(unitType[key])}</dd>
								</div>
							)
						)}
						<div>
							<dt>Value type</dt>
							<dd>{(valueTypes.find(el => el.id === this.props.unitType.value_type) || {}).name}</dd>
						</div>
						<div>
							<dt>Counting type</dt>
							<dd>{(incrementalTypes.find(el => el.id === this.props.unitType.incremental_type) || {}).name}</dd>
						</div>
					</dl>
				</div>
			</div>
		);
	}
}

export default connect(
	(state, props) => ({
		unitType: (state.unitTypes.unitTypes || []).find(el => el.id === Number(props.params.unitTypeID)),
	}),
)(UnitTypeDetail);
