import React, { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

import useModalStore from '@/stores/useModalStore';

const Modal = () => {
  const { isOpen, isClosing, modalContent, closeModal, modalSize } =
    useModalStore();
  const dialog = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (isClosing) return;

    if (isOpen && dialog.current) {
      dialog.current.showModal();
    }
  }, [isOpen, isClosing]);

  function handleBackdropClick(
    event: React.MouseEvent<HTMLDialogElement, MouseEvent>
  ) {
    if (dialog.current && event.target === dialog.current) {
      closeModal();
    }
  }

  const modalVariants = {
    start: {
      opacity: 0,
      y: 150,
    },
    end: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.3,
        ease: 'easeInOut',
      },
    },
    exit: {
      opacity: 0,
      y: 150,
      transition: {
        duration: 0.15,
        ease: 'easeInOut',
      },
    },
  };

  // 모달 크기에 따른 width 클래스 반환
  const getModalWidth = () => {
    switch (modalSize) {
      case 'sm':
        return 'w-[25%] min-w-[200px] max-w-[400px]';
      case 'md':
        return 'w-[35%] min-w-[300px] max-w-[600px]';
      case 'lg':
        return 'w-[50%] min-w-[400px] max-w-[800px]';
      case 'xl':
        return 'w-[70%] min-w-[500px] max-w-[1200px]';
      default:
        return 'w-[30%] min-w-[200px] max-w-[600px]'; // 기본값
    }
  };

  return (
    <AnimatePresence
      onExitComplete={() => {
        if (dialog.current) {
          dialog.current.close();
        }
      }}
    >
      {isOpen && (
        <motion.dialog
          initial='start'
          animate='end'
          exit='exit'
          variants={modalVariants}
          ref={dialog}
          onClick={handleBackdropClick}
          className={`${getModalWidth()} fixed top-0 z-50 mx-auto rounded-lg`}
        >
          {modalContent}
        </motion.dialog>
      )}
    </AnimatePresence>
  );
};

export default Modal;
