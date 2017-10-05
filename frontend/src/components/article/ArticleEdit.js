import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router';
import { createArticle, updateArticle } from '../../actions/articles';
import { BoolField, IntegerField, SelectField, StringField } from '../forms/fields';
import FontAwesome from '../tools/icons/FontAwesome';
import LabelField from '../forms/LabelField';
import LabelList from '../assortment/LabelList';

class ArticleEdit extends React.Component {
	static propTypes = {
		defaultCurrency: PropTypes.object.isRequired,
		article: PropTypes.object.isRequired,
		accountingGroups: PropTypes.arrayOf(PropTypes.object).isRequired,
		addArticle: PropTypes.func.isRequired,
		editArticle: PropTypes.func.isRequired,
		params: PropTypes.shape({ articleID: PropTypes.string.isRequired }).isRequired,
	};

	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	componentWillMount() {
		this.reset(null);
	}

	getResetState(props = this.props) {
		if (props.article !== null) {
			return {
				...props.article,
				useFixedPrice: false,
			};
		}
		return {
			id: null,
			fixed_price: null,
			accounting_group: null,
			name: '',
			labels: [],
			ean: null,
			serial_number: false,
		};
	}

	save(evt) {
		if (evt) {
			evt.preventDefault();
		}
		if (this.state.id) {
			this.props.editArticle(this.state);
		} else {
			this.props.addArticle(this.state);
		}
	}

	reset(evt, props) {
		if (evt) {
			evt.preventDefault();
		}
		this.setState(this.getResetState(props));
	}

	componentWillReceiveProps(props) {
		if (this.props.article !== props.article) {
			this.reset(null, props);
		}
	}

	removeLabel(ltID, lValue) {
		this.setState(state => ({
			labels: {
				...state.labels,
				[ltID]: (state.labels[ltID] || []).filter(v => v !== lValue),
			},
		}));
	}

	render() {
		return (
			<form className="box">
				<div className="box-header with-border">
					<h3 className="box-title">{`${this.state.id ? this.state.name : 'New article'} - Properties`}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link
									to="/articlemanager/" className="btn btn-default btn-sm"
									  title="Close"><FontAwesome icon="close" /></Link>
								<Link onClick={evt => this.reset(evt)} className="btn btn-warning btn-sm" title="Reset"><FontAwesome
									icon="repeat" /></Link>
								<Link
									onClick={() => this.save()} className="btn btn-success btn-sm"
									  title="Save">Save</Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<div className="form-horizontal">
						<StringField
							value={this.state.name} name="Name"
							onChange={evt => this.setState({ name: evt.target.value })} />
						<IntegerField
							value={this.state.ean || ''} name="EAN"
							onChange={evt => this.setState({ ean: Number(evt.target.value) })} min={0}
							step={1} />
						<BoolField
							value={this.state.serial_number} name="Uses serial numbers"
							onChange={() => this.setState(({ serial_number }) => ({ serial_number: !serial_number }))} />
					</div>
					<div className="form-horizontal">
						<div className="form-group">
							<label className="col-sm-3 control-label" htmlFor="labels">Labels</label>
							<div className="col-sm-9">
								<LabelField
									name="labels"
									labels={this.state.labels}
									onAddLabel={
										(typeID, value) => this.setState(
											state => ({
												...state,
												labels: {
													...state.labels,
													[typeID]: (state.labels[typeID].filter(v => v !== value) || [])
														.concat([ value ]),
												},
											})
										)
									} />
							</div>
							<LabelList
								className="col-sm-9 col-sm-offset-3"
								labels={this.state.labels}
								insert={({ value, typeID }) => (
									<a
										className="btn btn-danger btn-xs"
										onClick={() => this.removeLabel(typeID, value)}>
										<FontAwesome icon="close" />
									</a>
								)} />
						</div>
					</div>
				</div>
				<div className="box-header with-border">
					<h3 className="box-title">Pricing</h3>
				</div>
				<div className="box-body">
					<div className="form-horizontal">
						<SelectField
							value={this.state.accounting_group || ''}
							name="Accounting group"
							onChange={evt => this.setState({ accounting_group: evt.target.value })}
							options={this.props.accountingGroups} />
						{'{ PricingModelSelectorComponent }'}
					</div>
				</div>
				<div className="box-header with-border">
					<h3 className="box-title">Suppliers</h3>
				</div>
				<div className="box-body">
					{'{ SupplierInfoComponent }'}
				</div>
				{
					this.props.errorMsg ? (
						<div className="box-footer">
							{this.props.errorMsg}
						</div>
					) : null
				}
			</form>
		);
	}
}

export default connect(
	(state, ownProps) => ({
		...ownProps,
		defaultCurrency: state.defaultCurrency || {
			symbol: '€',
			digits: 2,
			iso: 'EUR',
		},
		article: (state.articles.articles || []).find(article => article.id === +ownProps.params.articleID),
		accountingGroups: state.accountingGroups.accountingGroups,
	}),
	dispatch => ({
		addArticle: article => {
			const copy = { ...article };

			if (!copy.useFixedPrice) {
				copy.fixed_price = null;
			}
			delete copy['useFixedPrice'];
			return dispatch(createArticle(copy));
		},
		editArticle: article => {
			const copy = { ...article };

			if (!copy.useFixedPrice) {
				copy.fixed_price = null;
			}
			delete copy['useFixedPrice'];
			return dispatch(updateArticle(copy));
		},
	})
)(ArticleEdit);
