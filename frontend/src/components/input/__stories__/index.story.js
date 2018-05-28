import React from 'react';
import { storiesOf } from '@storybook/react';

import Input from '../index';

storiesOf('Input', module)
	.add('default', () => <Input placeholder="Input" />)
	.add('success', () => <Input placeholder="Input" success />)
	.add('error', () => <Input placeholder="Input" error />);
