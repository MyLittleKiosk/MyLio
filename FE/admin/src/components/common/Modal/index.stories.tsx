import Modal from './index';
import type { Meta, StoryObj } from '@storybook/react';
import useModalStore from '@/stores/useModalStore';

const meta: Meta<typeof Modal> = {
  title: 'Components/Common/Modal',
  component: Modal,
  parameters: {
    layout: 'centered',
  },
  decorators: [
    (Story) => {
      // 스토리북에서 모달 상태를 제어하기 위한 래퍼 컴포넌트
      const { openModal } = useModalStore();

      return (
        <div>
          <button
            onClick={() =>
              openModal(
                <div className='w-[500px] h-[150px]'>모달 내용입니다</div>
              )
            }
          >
            모달 열기
          </button>
          <Story />
        </div>
      );
    },
  ],
};

export default meta;
type Story = StoryObj<typeof Modal>;

export const Default: Story = {};
