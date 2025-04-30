import React, { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

import useModalStore from '@/stores/useModalStore';

const Modal = () => {
  const { isOpen, isClosing, modalContent, closeModal } = useModalStore();
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
          className={`w-[50%] min-w-[200px] max-w-[600px] fixed top-0 z-50 mx-auto rounded-lg`}
        >
          {modalContent}
        </motion.dialog>
      )}
    </AnimatePresence>
  );
};

export default Modal;
