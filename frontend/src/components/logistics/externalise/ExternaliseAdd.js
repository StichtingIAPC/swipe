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
			<table className="table">
				<thead>
					<tr>
						<th>Article</th>
						<th width="150px">Price</th>
						<th width="80px">Count</th>
						<th width="50px" />
					</tr>
				</thead>
				<tbody>
					{this.props.externalise.externaliseline_set.map((line, index) => (
						<tr key={index}>
							<td className="form-group col">
								<ArticleTypeSelector
									onChange={this.updateArticleField(index, 'article')}
									name="article"
									value={this.props.externalise.externaliseline_set[index].article &&
									this.props.externalise.externaliseline_set[index].article.id} />
							</td>
							<td className="form-group col">
								<MoneyField
									onChange={this.updateArticleFieldArticle(index)}
									name="cost"
									currency={this.props.externalise.externaliseline_set[index].amount &&
										this.props.externalise.externaliseline_set[index].amount.currency}
									value={this.props.externalise.externaliseline_set[index].amount &&
									this.props.externalise.externaliseline_set[index].amount.amount} />
							</td>
							<td>
								<input
									className="form-control"
									type="number"
									min={0}
									step={1}
									value={this.props.externalise.externaliseline_set[index].count}
									onChange={this.updateArticleFieldCount(index)} />
							</td>
							<td>
								<span className="input-group-btn">
									<a className="btn btn-danger" onClick={this.removeArticle(index)}>
										<FontAwesome icon="trash" />
									</a>
								</span>
							</td>
						</tr>
					))}
				</tbody>
			</table>
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
