import React, { PropTypes } from 'react';
import { Link } from 'react-router';
import FA from '../../tools/FontAwesome.js';

export default class SidebarLink extends React.Component {
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
				<FA icon={(this.state.open ? 'angle-down' : 'angle-left') + ' pull-right'} />
			</span>
		) : null;

		return (
			<li className={this.state.open ? 'treeview active' : 'treeview'}>
				<Link to={this.props.to} activeClassName={this.props.activeClassName || 'active'}>
					<FA icon={this.props.icon ? this.props.icon : 'circle-o'} />
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
