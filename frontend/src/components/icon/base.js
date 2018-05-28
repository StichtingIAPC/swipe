import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
	display: inline-block;
	position: relative;
	width: ${props => (props.width ? `${props.width}px` : 'auto')};
	height: ${props => (props.height ? `${props.height}px` : 'auto')};
	color: currentColor;
`;

const Canvas = styled.canvas`
	display: block;
	height: 100%;
	visibility: hidden;
`;

const Icon = styled.svg`
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	fill: currentColor;
`;

const Base = ({ children, viewBox, width, height, color, ...props }) => {
	const fragments = viewBox.split(' ');

	return (
		<Container color={color} width={width} height={height} {...props}>
			<Canvas width={fragments[2]} height={fragments[3]} />
			<Icon viewBox={viewBox}>{children}</Icon>
		</Container>
	);
};

export default Base;
