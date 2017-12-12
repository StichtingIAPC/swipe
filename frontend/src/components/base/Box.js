import React from 'react';
import FontAwesome from '../tools/icons/FontAwesome';

export default class Box extends React.Component {
	static Header = ({ title, buttons, withoutBorder }) => (
		<div className={`box-header${withoutBorder ? '' : ' with-border'}`}>
			<div className="box-title">{title}</div>
			<div className="box-tools">
				<div className="input-group">
					<div className="btn-group">
						{buttons}
					</div>
				</div>
			</div>
		</div>
	);

	static Body = ({ children }) => (
		<div className="box-body">{children}</div>
	);

	static Footer = ({ children }) => (
		<div className="box-footer">{ children }</div>
	);

	constructor(props) {
		super(props);
		this.state = {
			err: false,
			open: true,
		};

		window.setTimeout(() => console.log(this.updater.isMounted()), 1);
	}

	toggleOpen = () => {
		console.log('hi', this.sym, this);
		this.setState(state => ({ open: !state.open }));
	}

	componentWillCatch(err) {
		console.log(err);
		this.setState(() => ({ err: true }));
	}

	componentWillMount() {
		this.sym = Symbol(`${Math.random()}`);
		console.log('mounting box', this.sym);
	}
	componentWillUnmount() {
		console.log('unmounting Box', this.sym);
		this.sym = null;
	}

	render() {
		const { open, err } = this.state;
		const { header, closable, error, children } = this.props;

		if (err) {
			return (
				<div className="box box-warning box-solid">
					<Box.Header title="Error in this component" />
				</div>
			);
		}

		return (
			<div
				className={`box${
					open ? ' open' : ''
				}${
					error ? ' box-warning box-solid' : ''
				}`}>
				{
					typeof header === 'undefined' ? null : (
						<div className={`box-header${header.withoutBorder ? '' : ' with-border'}`}>
							<div className="box-title">{ header.title }</div>
							<div className="box-tools">
								<div className="input-group">
									<div className="btn-group">{ header.buttons }</div>
									{
										closable ? (
											<a
												className="btn btn-box-tool"
												onClick={this.toggleOpen}
												title={open ? 'Close box' : 'Open box'}>
												<FontAwesome icon={open ? 'minus' : 'plus'} />
											</a>
										) : null
									}
								</div>
							</div>
						</div>
					)
				}
				{ children }
			</div>
		);
	}
}
