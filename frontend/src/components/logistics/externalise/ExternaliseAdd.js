import React, { Component } from 'react';
import FontAwesome from '../../tools/icons/FontAwesome';
import { connect } from 'react-redux';
import { newAction as resetExternalise, setFieldAction as setExternaliseField, createAction as createExternalise, newAction as newExternalise } from '../../../state/logistics/externalise/actions';

import Form from '../../forms/Form';
import ArticleTypeSelector from '../../article/ArticleTypeSelector';
import { CharField, IntegerField, MoneyField, StringField } from '../../forms/fields';

class ExternaliseAdd extends Component {
	setMemo = event => this.props.setExternaliseField('memo', event.target.value);

	addArticle = () => this.props.setExternaliseField(
		'externaliseline_set',
		this.props.externalise.externaliseline_set.concat([{
			// eslint-disable-next-line
			article: undefined,
			amount: {
				currency: 'EUR',
				amount: '',
			},
			count: '',
		}]));
	removeArticle = index => () => this.props.setExternaliseField('externaliseline_set', this.props.externalise.externaliseline_set.filter((_, i) => i !== index));

	updateArticleField = (index, field) =>
		ev => {
			this.props.setExternaliseField(
				'externaliseline_set',
				this.props.externalise.externaliseline_set.map((el, i) => {
					if (i === index) {
						return {
							...el,
							[field]: ev.target ? ev.target.value : ev,
						};
					}
					return el;
				})
			);
		};
	updateArticleFieldArticle = index => ({ target: { value }}) => {
		this.props.setExternaliseField(
			'externaliseline_set',
			this.props.externalise.externaliseline_set.map((el, i) => {
				if (i === index) {
					const e = {
						...el,
					};

					e.amount = e.amount || {};
					e.amount.amount = value;
					return e;
				}
				return el;
			})
		);
	};
	updateArticleFieldCount = index => ({ target: { value }}) => {
		this.props.setExternaliseField(
			'externaliseline_set',
			this.props.externalise.externaliseline_set.map((el, i) => {
				if (i === index) {
					return {
						...el,
						count: Number(value),
					};
				}
				return el;
			})
		);
	};

	create = () => this.props.createExternalise(this.props.externalise);
	reset = () => this.props.newExternalise();

	render() {
		return <Form
			title="Add new externalisation"
			onReset={this.reset}
			onSubmit={this.create}
			error={this.props.error}
			closeLink="/logistics/externalise/">
			<StringField onChange={this.setMemo} name="Memo" value={this.props.externalise.memo} />
			{this.props.externalise.externaliseline_set.map((line, index) => (
				<div key={index}>
					<div className="form-group">
						<label className="col-sm-3 control-label" htmlFor="article">Article</label>
						<div className="col-sm-9">
							<ArticleTypeSelector
								onChange={this.updateArticleField(index, 'article')}
								name="article"
								value={this.props.externalise.externaliseline_set[index].article &&
										this.props.externalise.externaliseline_set[index].article.id} />
						</div>
					</div>
					<div className="form-group">
						<label className="col-sm-3 control-label" htmlFor="cost">Price</label>
						<div className="col-sm-9">
							<MoneyField
								onChange={this.updateArticleFieldArticle(index)}
								name="cost"
								currency={this.props.externalise.externaliseline_set[index].amount &&
											this.props.externalise.externaliseline_set[index].amount.currency}
								value={this.props.externalise.externaliseline_set[index].amount &&
										this.props.externalise.externaliseline_set[index].amount.amount} />
						</div>
					</div>
					<IntegerField
						name="Count"
						value={this.props.externalise.externaliseline_set[index].count}
						onChange={this.updateArticleFieldCount(index)} />
					<span className="input-group-btn">
						<a className="btn btn-danger" onClick={this.removeArticle(index)}>
							<FontAwesome icon="trash" />
						</a>
					</span>
				</div>
			))}
			<a className="btn btn-success" onClick={this.addArticle}>Add article</a>
		</Form>;
	}
}

export default connect(
	state => ({
		externalise: state.logistics.externalise.activeObject,
		error: state.logistics.externalise.error,
	}),
	{
		reset: resetExternalise,
		setExternaliseField,
		createExternalise,
		newExternalise,
	}
)(ExternaliseAdd);
