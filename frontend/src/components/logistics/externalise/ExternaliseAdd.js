import React, { Component } from 'react';
import FontAwesome from '../../tools/icons/FontAwesome';
import { connect } from 'react-redux';

import actions from '../../../state/logistics/externalise/actions';
import Card from '../../base/Card';
import ArticleTypeSelector from '../../article/ArticleTypeSelector';
import { MoneyField } from '../../forms/fields';
import { Button, ButtonToolbar, ControlLabel, FormControl, FormGroup, HelpBlock, Table } from 'react-bootstrap';
import { getExternalisationValidations } from '../../../state/logistics/externalise/selectors';
import { hasError } from '../../../tools/validations/validators';

class ExternaliseAdd extends Component {
	setMemo = event => this.props.setField('memo', event.target.value);

	addArticle = () => this.props.setField(
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
	removeArticle = index => () => this.props.setField('externaliseline_set', this.props.externalise.externaliseline_set.filter((_, i) => i !== index));

	updateArticleField = (index, field) =>
		ev => {
			this.props.setField(
				'externaliseline_set',
				this.props.externalise.externaliseline_set.map((el, i) => {
					if (i === index) {
						return {
							...el,
							[field]: ev.target ? ev.target.value : ev,
						};
					}
					return el;
				}),
			);
		};
	updateArticleFieldArticle = index => value => {
		this.props.setField(
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
			}),
		);
	};
	updateArticleFieldCount = index => ({ target: { value }}) => {
		this.props.setField(
			'externaliseline_set',
			this.props.externalise.externaliseline_set.map((el, i) => {
				if (i === index) {
					return {
						...el,
						count: Number(value),
					};
				}
				return el;
			}),
		);
	};

	create = () => this.props.createStart();
	reset = () => this.props.startNew();

	render() {
		const validation_memo = this.props.validations ? this.props.validations['memo'] : {};
		const memoValidation = validation_memo ? validation_memo.text : '';
		const memoErrorType = validation_memo ? validation_memo.type : 'success';

		const externalizeSetValidation = this.props.validations ? this.props.validations['externaliseline_set'] : {};
		const externalizeSetValidationText = externalizeSetValidation ? externalizeSetValidation.text : '';
		const externalizeSetErrorType = externalizeSetValidation ? externalizeSetValidation.type : 'success';

		return <Card
			title="Add new externalisation"
			onReset={this.reset}
			error={this.props.error}
			closeLink="/logistics/externalise/">
			<form>
				<FormGroup
					controlId="formBasicText"
					validationState={memoErrorType}>
					<ControlLabel>Memo</ControlLabel>
					<FormControl
						type="text"
						value={this.props.externalise.memo}
						placeholder="Enter text"
						onChange={this.setMemo} />
					<FormControl.Feedback />
					<HelpBlock>{memoValidation}</HelpBlock>
				</FormGroup>
				<FormGroup
					controlId="externalizeSets"
					validationState={externalizeSetErrorType}>
					<Table>
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
										<FormControl
											type="number"
											value={this.props.externalise.externaliseline_set[index].count}
											onChange={this.updateArticleFieldCount(index)}
											bsClass="form-control no-validation-padding" />
									</td>
									<td>
										<Button bsStyle="danger" onClick={this.removeArticle(index)}>
											<FontAwesome icon="trash" />
										</Button>
									</td>
								</tr>
							))}
						</tbody>
					</Table>
					<FormControl.Feedback />
					<HelpBlock>{externalizeSetValidationText}</HelpBlock>
				</FormGroup>

				<ButtonToolbar>
					<Button bsStyle="default" onClick={this.addArticle}><FontAwesome icon="plus" /></Button>
					<Button
						bsStyle="success"
						onClick={this.create}
						disabled={hasError(this.props.validations)}>Save</Button>
				</ButtonToolbar>
			</form>
		</Card>;
	}
}

export default connect(
	state => ({
		externalise: state.logistics.externalise.activeObject,
		error: state.logistics.externalise.error,
		validations: getExternalisationValidations(state),
	}),
	{
		setField: actions.setField,
		createStart: actions.createStart,
		startNew: actions.startNew,
	},
)(ExternaliseAdd);
