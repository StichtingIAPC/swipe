import React, { PropTypes } from 'react';
import { Link } from 'react-router';
import FontAwesome from '../../../../../tools/static/tools/components/FontAwesome.js';

export class SBLink extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			open: null,
		};
	}

	toggle(evt) {
		this.setState({
			open: this.state.open ? null : 'active',
		});
		evt.preventDefault();
	}

	render() {
		const children = this.props.children ? (
			<ul className={'treeview-menu' + (this.state.open ? ' menu-open' : '')}>
				{this.props.children}
			</ul>
    ) : null;

		const openswitch = this.props.children ? (
			<span className="pull-right-container" onClick={this.toggle.bind(this)}>
				<FontAwesome icon={(this.state.open ? 'angle-down' : 'angle-left') + ' pull-right'} />
			</span>
    ) : null;

		return (
			<li className={this.state.open ? 'treeview active' : 'treeview'}>
				<Link to={this.props.to} activeClassName={this.props.activeClassName}>
					<FontAwesome icon={this.props.icon} />
					<span>{this.props.text}</span>
					{openswitch}
				</Link>
				{children}
			</li>
		);
	}
}

SBLink.propTypes = {
	to: PropTypes.string.isRequired,
	icon: PropTypes.string,
	children: PropTypes.node,
	activeClassName: PropTypes.string,
};

SBLink.defaultProps = {
	icon: 'circle-o',
	activeClassName: 'active',
};

export default SBLink;
