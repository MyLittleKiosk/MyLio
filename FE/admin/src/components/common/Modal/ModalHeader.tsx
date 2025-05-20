interface ModalHeaderProps {
  title: string;
  description: string;
}

const ModalHeader = ({ title, description }: ModalHeaderProps) => {
  return (
    <header className='flex flex-col items-start justify-between'>
      <h2 className='font-preBold text-xl'>{title}</h2>
      <p className='font-preRegular text-md text-content whitespace-pre-line leading-tight'>
        {description}
      </p>
    </header>
  );
};

export default ModalHeader;
