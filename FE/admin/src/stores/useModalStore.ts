import { ReactNode } from 'react';
import { create } from 'zustand';

type ModalSize = 'sm' | 'md' | 'lg' | 'xl';

interface ModalState {
  // isOpen: 모달이 열려있는지 여부, isClosing: 모달이 닫히는 중인지 여부, modalContent: 모달에 렌더링할 컴포넌트트, openModal: 모달 열기 함수, closeModal: 모달 닫기 함수
  isOpen: boolean;
  isClosing: boolean;
  modalContent: ReactNode | null;
  modalSize: ModalSize;
  openModal: (content: ReactNode, size?: ModalSize) => void;
  closeModal: () => void;
}

const useModalStore = create<ModalState>((set) => ({
  isOpen: false,
  isClosing: false,
  modalContent: null,
  modalSize: 'md',
  openModal: (content, size = 'md') => {
    set({
      isOpen: true,
      isClosing: false,
      modalContent: content,
      modalSize: size,
    });
  },
  closeModal: () => {
    set({ isClosing: true });
    setTimeout(() => {
      set({ isOpen: false, modalContent: null, isClosing: false });
    }, 200);
  },
}));

export default useModalStore;
