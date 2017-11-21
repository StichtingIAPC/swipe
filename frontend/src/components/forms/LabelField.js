import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { connectMixin } from '../../core/stateRequirements';
import { labelTypes } from '../../state/assortment/label-types/actions.js';
import { unitTypes } from '../../state/assortment/unit-types/actions.js';
import AsyncSelectBox from '../base/AsyncSelectBox';

class LabelField extends React.Component {
	static propTypes = { onAddLabel: PropTypes.func.isRequired };

	static defaultProps = { className: 'input-group' };

	constructor(props) {
		super(props);
		this.state = LabelField.getResetState();
		this.cache = {};
	}

	resetState() {
		this.setState(LabelField.getResetState());
	}

	static getResetState() {
		return {
			activeList: [],
			lType: null,
			lValue: null,
			query: '',
		};
	}

	getUnitTypeCached(id) {
		if (!this.cache[id]) {
			this.cache[id] = this.props.unitTypes.find(el => el.id === id);
		}
		return this.cache[id];
	}

	componentWillReceiveProps(props) {
		if (this.props.unitTypes !== props.unitTypes) {
			this.cache = {};
		}
	}

	findLabelTypes(desc) {
		return this.props.labelTypes.filter(
			el => el.name.startsWith(desc) || el.description.indexOf(desc) !== -1
		);
	}

	returnToLabelTypeSelection() {
		this.setState(state => ({
			activeList: [],
			lType: null,
			lValue: null,
			query: state.lType.name,
		}));
	}

	render() {
		const { name, className } = this.props;

		const addLabel = (ltID, lValue) => {
			this.props.onAddLabel(ltID, lValue);
			this.resetState();
		};

		let selectionElement = null;

		if (this.state.lType === null) {
			selectionElement = (
				<div className={className}>
					<AsyncSelectBox
						id={name}
						placeholder="Label type"
						onSearch={
							query => this.setState({
								query,
								activeList: this.findLabelTypes(query)
									.map(el => ({
										key: el.id,
										label: el.name,
									})),
							})
						}
						results={this.state.activeList}
						onSelect={
							key => this.setState({
								query: '',
								lType: this.props.labelTypes
									.find(el => el.id === key),
								activeList: [],
							})
						} />
					{null}
					<div className="input-group-addon">
						rest
					</div>
				</div>
			);
		} else {
			const unitType = this.getUnitTypeCached(this.state.lType.unit_type);

			selectionElement = (
				<div className={className}>
					<span className="input-group-btn">
						<button className="btn btn-default btn-flat" onClick={evt => { evt.preventDefault(); this.returnToLabelTypeSelection(); }}>{this.state.lType.name}</button>
					</span>
					<AsyncSelectBox
						id={name}
						onSearch={query => this.setState(
							state => ({
								query,
								lValue: query,
								activeList: state.lType.labels
									.filter(el => el.value.startsWith(query))
									.map(el => ({
										key: el.id,
										label: el.value,
									}))
									.concat([{
										key: query,
										label: query,
									}]),
							})
						)}
						placeholder="Label value"
						results={this.state.activeList}
						query={this.state.query}
						onSelect={key => addLabel(this.state.lType.id, key === +key ? this.state.lType.labels.find(el => el.id === key).value : key)} />
					{
						unitType.type_short ? <div className="input-group-addon">
							{unitType.type_short}
						</div> : null
					}
				</div>
			);
		}

		return this.props.requirementsLoaded ? selectionElement : 'Loading';
	}
}

export default connect(
	state => ({
		...connectMixin({
			assortment: {
				labelTypes,
				unitTypes,
			},
		}, state),
		labelTypes: state.assortment.labelTypes.labelTypes,
		unitTypes: state.assortment.unitTypes.unitTypes,
	})
)(LabelField);
