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
    error: { control: 'boolean' },
    disabled: { control: 'boolean' },
  },
} satisfies Meta<typeof Input>;

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
    ...WithLabel.args,
    type: 'number',
  },
};

export const Error: Story = {
  args: {
    ...WithLabel.args,
    error: true,
  },
};

export const Disabled: Story = {
  args: {
    ...WithLabel.args,
    disabled: true,
  },
};
