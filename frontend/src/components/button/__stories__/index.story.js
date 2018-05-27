import React from 'react';
import { storiesOf } from '@storybook/react';

import Button from '../index';

storiesOf('Button', module)
	.add('default', () => <Button>Button</Button>)
	.add('large', () => <Button large>Button</Button>)
	.add('positive', () => <Button positive>Button</Button>)
	.add('negative', () => <Button negative>Button</Button>);
