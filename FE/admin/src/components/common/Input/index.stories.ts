import Input from './index';
import type { Meta, StoryObj } from '@storybook/react';

const meta: Meta<typeof Input> = {
  title: 'Components/Common/Input',
  component: Input,
  tags: ['autodocs'],
  argTypes: {
    label: { control: 'text' },
    id: { control: 'text' },
    placeholder: { control: 'text' },
    type: { control: 'text' },
    value: { control: 'text' },
    onChange: { action: 'changed' },
    className: { control: 'text' },
  },
};

export default meta;

type Story = StoryObj<typeof Input>;

export const WithLabel: Story = {
  args: {
    label: 'Label',
    id: 'withlabelinput',
    placeholder: 'placeholder',
    type: 'text',
    value: '',
    onChange: () => {},
  },
};

export const WithoutLabel: Story = {
  args: {
    id: 'withoutlabelinput',
    placeholder: 'placeholder',
    type: 'text',
    value: '',
    onChange: () => {},
  },
};

export const NumberInput: Story = {
  args: {
    label: 'Number',
    id: 'numberinput',
    placeholder: 'placeholder',
    type: 'number',
    value: '',
    onChange: () => {},
  },
};
