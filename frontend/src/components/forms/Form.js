import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import FontAwesome from '../tools/icons/FontAwesome';
import { Box } from 'reactjs-admin-lte';
import { Button, ButtonGroup } from 'react-bootstrap';

/**
 * Provides a simple box which accepts a form. Also supports displaying an error and can change box type depending on
 * the presence of warnings or errors.
 *
 * @prop children: PropTypes.node.isRequired
 *      All content to be displayed in the from. This should contain at least the form.
 * @prop returnLink: PropTypes.string
 *      An optional return button will use this as a 'to' prop in 'Link' component.
 * @prop closeLink: PropTypes.string
 *      An optional close button will use this as a 'to' prop in 'Link' component.
 * @prop title: PropTypes.string.isRequired
 *      The title of the form.
 * @prop onReset: PropTypes.func.isRequired
 *      This should clear the content of the form and is called when the reset button is pressed.
 * @prop error: PropTypes.string
 *      This will be displayed as an error below the form and change the box style to 'danger'.
 * @prop hasErrors: PropTypes.bool
 *      This will change the box style to 'danger'. Use this make the box change with form validations.
 * @prop hasWarnings: PropTypes.bool
 *      This will change the box style to 'warning'. Use this make the box change with form validations.
 */
export default class Form extends React.Component {
	onSubmit = event => {
		event.preventDefault();
		return this.props.onSubmit(event);
	};

	render() {
		return <Box
			style={this.props.error || this.props.hasErrors ? 'danger' : this.props.hasWarnings ? 'warning' : 'primary'}>
			<Box.Header>
				<Box.Title>{this.props.title}</Box.Title>
				<Box.Tools>
					<ButtonGroup>
						{
							this.props.returnLink ? (
								<Link
									className="btn btn-default btn-sm"
									to={this.props.returnLink}
									title="Return">
									<FontAwesome icon="arrow-left" />
								</Link>
							) : null
						}
						<Button
							bsSize="small"
							bsStyle="warning"
							title="Reset"
							onClick={this.props.onReset}>
							<FontAwesome icon="repeat" />
						</Button>
						{
							this.props.closeLink ? (
								<Link
									className="btn btn-default btn-sm"
									to={this.props.closeLink}
									title="Close">
									<FontAwesome icon="close" />
								</Link>
							) : null
						}
					</ButtonGroup>
				</Box.Tools>
			</Box.Header>
			<Box.Body children={this.props.children} />
			{
				this.props.error ? (
					<Box.Footer className="text-danger">
						<FontAwesome icon="warning" />
						<span> {this.props.error}</span>
					</Box.Footer>
				) : null
			}
		</Box>;
	}
}

Form.propTypes = {
	children: PropTypes.node.isRequired,
	returnLink: PropTypes.string,
	closeLink: PropTypes.string,
	title: PropTypes.string.isRequired,
	onReset: PropTypes.func.isRequired,
	error: PropTypes.string,
	hasErrors: PropTypes.bool,
	hasWarnings: PropTypes.bool,
};
