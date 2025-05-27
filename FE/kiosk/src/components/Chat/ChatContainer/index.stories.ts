import type { Meta, StoryObj } from '@storybook/react';
import ChatContainer from './index';

const meta = {
  title: 'Components/Chat/ChatContainer',
  component: ChatContainer,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    userChat: {
      control: 'text',
      description: '사용자 음성 입력 메시지',
    },
    gptChat: {
      control: 'text',
      description: 'GPT 응답 메시지',
    },
    isExpand: {
      control: 'boolean',
      description: '확장 상태',
    },
  },
} satisfies Meta<typeof ChatContainer>;
export default meta;
type Story = StoryObj<typeof meta>;

/**
 * 키오스크 상단에 보일 채팅 컨테이너
 */
export const Default: Story = {
  args: {
    userChat:
      '그란데 사이즈 아이스 바닐라 더블 샷에 오트 밀크로 변경하고, 샷은 3개, 바닐라 시럽 2펌프, 헤이즐넛 시럽 1펌프 추가, 얼음 적게, 휘핑크림 빼고, 카라멜 드리즐이랑 초콜릿 드리즐 둘 다 많이 뿌려주세요. 컵은 벤티 컵에 담아주시고, 텀블러에 옮겨 담아갈 거예요.',
    gptChat: `무엇을 도와드릴까요?\n다양한 커피 메뉴를 소개해드릴게요.\n커피 메뉴를 선택해주세요.\n오늘의 메뉴로 청포도 아이스 티를 추천해드려요!`,
    isExpand: false,
  },
};
