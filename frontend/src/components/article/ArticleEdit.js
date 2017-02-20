import React, { PropTypes } from "react";
import { connect } from "react-redux";
import { Link } from "react-router";
import { createArticle, updateArticle } from "../../actions/articles";
import { BoolField, IntegerField, StringField, SelectField } from "../forms/fields";
import FontAwesome from "../tools/icons/FontAwesome";

class ArticleEdit extends React.Component {
	constructor(props) {
		super(props);
		this.state = this.getResetState();
	}

	componentWillMount() {
		this.reset(null);
	}

	getResetState(props = this.props) {
		if (props.article != null) return { ...props.article, useFixedPrice: false };
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

	reset(evt, props) {
		if (evt) evt.preventDefault();
		this.setState(this.getResetState(props));
	}

	submit(evt) {
		evt.preventDefault();
		if (this.state.id == null) {
			this.props.addArticle({ ...this.state, lastModified: new Date() });
		} else {
			this.props.editArticle({ ...this.state, lastModified: new Date() });
		}
	}

	componentWillReceiveProps(props) {
		if (this.props.supplier != props.supplier) this.reset(undefined, props);
	}

	render() {
		return (
			<form className="box">
				<div className="box-header with-border">
					<h3 className="box-title">{`${this.props.id instanceof Number ? this.props.name : 'New article'} - Properties`}</h3>
					<div className="box-tools">
						<div className="input-group">
							<div className="btn-group">
								<Link to="/articlemanager/" className="btn btn-default btn-sm" title="Close"><FontAwesome icon="close" /></Link>
								<Link onClick={(evt) => this.reset(evt)} className="btn btn-warning btn-sm" title="Reset"><FontAwesome icon="repeat" /></Link>
								<Link onClick={(evt) => this.save()} className="btn btn-success btn-sm" title="Save">Save</Link>
							</div>
						</div>
					</div>
				</div>
				<div className="box-body">
					<div className="form-horizontal">
						<StringField value={this.state.name} name="Name" onChange={evt => this.setState({name: evt.target.value})} />
						<IntegerField value={this.state.ean || ''} name="EAN" onChange={evt => this.setState({ean: Number(evt.target.value)})} min={0} step={1} />
						<BoolField value={this.state.serial_number} name="Uses serial numbers" onChange={evt => this.setState({serial_number: evt.target.value})} />
					</div>
					<p>Tag/label add/remove here</p>
				</div>
				<div className="box-header with-border">
					<h3 className="box-title">Pricing</h3>
				</div>
				<div className="box-body">
					<div className="form-horizontal">
						<SelectField
							value={this.state.accounting_group || ''}
							name="Accounting group"
							onChange={(evt) => this.setState({accounting_group: evt.target.value})}
							options={[
								{id: 1, name: "boeken"},
								{id: 2, name: "tekenpakketten"},
							]} />
						{"{ PricingModelSelectorComponent }"}
					</div>
				</div>
				<div className="box-header with-border">
					<h3 className="box-title">Suppliers</h3>
				</div>
				<div className="box-body">
					{"{ SupplierInfoComponent }"}
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
		defaultCurrency: (state.defaultCurrency || {symbol: "€", digits: 2, iso: 'EUR'}),
		article: (state.articles.articles || []).find(article => article.id == Number(ownProps.params.articleID)),
		accountingGroups: state.accountingGroups
	}),
	dispatch => ({
		addArticle: (article) => {
			const copy = {...article};
			if (!copy.useFixedPrice) copy.fixed_price = null;
			delete copy['useFixedPrice'];
			return dispatch(createArticle(copy))
		},
		editArticle: (article) => {
			const copy = {...article};
			if (!copy.useFixedPrice) copy.fixed_price = null;
			delete copy['useFixedPrice'];
			return dispatch(updateArticle(copy))
		},
	})
)(ArticleEdit)
