import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { createArticle, updateArticle } from '../../state/assortment/articles/actions.js';
import { BoolField, IntegerField, SelectField, StringField } from '../forms/fields';
import FontAwesome from '../tools/icons/FontAwesome';
import LabelField from '../forms/LabelField';
import LabelList from '../assortment/LabelList';
import { fetchArticle, newArticle, setArticleField } from '../../state/assortment/articles/actions';
import { connectMixin, fetchStateRequirementsFor } from '../../core/stateRequirements';
import { accountingGroups } from '../../state/money/accounting-groups/actions';
import { labelTypes } from '../../state/assortment/label-types/actions';
import { unitTypes } from '../../state/assortment/unit-types/actions';
import { Box } from 'reactjs-admin-lte';

class ArticleEdit extends React.Component {
	static propTypes = {
		defaultCurrency: PropTypes.object.isRequired,
		article: PropTypes.object.isRequired,
		accountingGroups: PropTypes.arrayOf(PropTypes.object).isRequired,
		addArticle: PropTypes.func.isRequired,
		editArticle: PropTypes.func.isRequired,
		params: PropTypes.shape({ articleID: PropTypes.string.isRequired }).isRequired,
	};

	componentWillMount() {
		this.props.fetchArticle(+this.props.match.params.articleID);
		fetchStateRequirementsFor(this);
	}

	save = () => {
		const { article } = this.props;

		if (article.id === null) {
			this.props.createArticle(article);
		} else {
			this.props.updateArticle(article);
		}
	};

	reset = () => {
		if (typeof this.props.match.params.articleID === 'undefined') {
			this.props.newArticle();
		} else {
			this.props.fetchArticle(+this.props.match.params.articleID);
		}
	};

	componentWillReceiveProps({ match }) {
		if (this.props.match.params.articleID !== match.params.articleID) {
			if (Number.isNaN(+match.params.articleID)) {
				this.props.newArticle();
			} else {
				this.props.fetchArticle(+match.params.articleID);
			}
		}
	}

	setName = ({ target: { value }}) => this.props.setArticleField('name', value);
	setEAN = ({ target: { value }}) => this.props.setArticleField('ean', +value);
	setSerialNumber = () => this.props.setArticleField('serial_number', !this.props.article.serial_number);
	setAccountingGroup = ({ target: { value }}) => this.props.setArticleField('accounting_group', value);

	addLabel = (typeID, value) => this.props.setArticleField(
		'labels',
		{
			...this.props.article.labels,
			[typeID]: (this.props.article.labels[typeID] || [])
				.filter(v => v !== value)
				.concat([ value ]),
		},
	);

	removeLabel = (typeID, value) => this.props.setArticleField(
		'labels',
		{
			...this.props.article.labels,
			[typeID]: (this.props.article.labels[typeID] || [])
				.filter(v => v !== value),
		},
	);

	renderInsert = ({ value, typeID }) => (
		<a
			className="btn btn-danger btn-xs"
			onClick={() => this.removeLabel(typeID, value)}>
			<FontAwesome icon="close" />
		</a>
	);

	render() {
		const { article, requirementsLoaded } = this.props;

		const NEW = article.id === null;

		if (!requirementsLoaded) {
			return null;
		}

		return (
			<Box>
				<Box.Header
					title={`${NEW ? 'New article' : article.name} - Properties`}
					buttons={[
						<Link key="close" to="/articlemanager/" className="btn btn-default btn-sm" title="Close"><FontAwesome icon="close" /></Link>,
						<a key="repeat" onClick={this.reset} className="btn btn-warning btn-sm" title="Reset"><FontAwesome icon="repeat" /></a>,
						<a key="save" onClick={this.save} className="btn btn-success btn-sm" title="Save">Save</a>,
					]} />
				<Box.Body>
					<div className="form-horizontal">
						<StringField
							value={article.name}
							name="Name"
							onChange={this.setName} />
						<IntegerField
							value={article.ean || ''}
							name="EAN"
							onChange={this.setEAN} min={0}
							step={1} />
						<BoolField
							value={article.serial_number} name="Uses serial numbers"
							onChange={this.setSerialNumber} />
					</div>
					<div className="form-horizontal">
						<div className="form-group">
							<label className="col-sm-3 control-label" htmlFor="labels">Labels</label>
							<div className="col-sm-9">
								<LabelField
									name="labels"
									labels={article.labels}
									onAddLabel={this.addLabel} />
							</div>
							<LabelList
								className="col-sm-9 col-sm-offset-3"
								labels={article.labels}
								insert={this.renderInsert} />
						</div>
					</div>
				</Box.Body>
				<Box.Header title="Pricing" />
				<Box.Body>
					<div className="form-horizontal">
						<SelectField
							value={article.accounting_group || ''}
							name="Accounting group"
							onChange={this.setAccountingGroup}
							options={this.props.accountingGroups} />
						{'{ PricingModelSelectorComponent }'}
					</div>
				</Box.Body>
				<Box.Header title="Suppliers" />
				<Box.Body>
					{'{ SupplierInfoComponent }'}
				</Box.Body>
				{
					this.props.errorMsg ? (
						<Box.Footer>
							{this.props.errorMsg}
						</Box.Footer>
					) : null
				}
			</Box>
		);
	}
}

export default connect(
	state => ({
		...connectMixin({
			assortment: {
				labelTypes,
				unitTypes,
			},
			money: {
				accountingGroups,
			},
		}, state),
		defaultCurrency: (state.settings || {}).defaultCurrency || { // get default currency from settings, or otherwise a hardcoded default 'EURO',
			symbol: '€',
			digits: 2,
			iso: 'EUR',
		},
		article: state.assortment.articles.activeObject,
		accountingGroups: state.money.accountingGroups.accountingGroups,
	}),
	{
		fetchArticle,
		setArticleField,
		newArticle,
		createArticle: article => {
			const copy = { ...article };

			if (!copy.useFixedPrice) {
				copy.fixed_price = null;
			}
			delete copy['useFixedPrice'];
			return createArticle(copy);
		},
		updateArticle: article => {
			const copy = { ...article };

			if (!copy.useFixedPrice) {
				copy.fixed_price = null;
			}
			delete copy['useFixedPrice'];
			return updateArticle(copy);
		},
		dispatch: e => e,
	}
)(ArticleEdit);
