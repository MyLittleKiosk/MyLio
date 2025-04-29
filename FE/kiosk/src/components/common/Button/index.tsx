interface ButtonProps {
  content: string;
  onClick: () => void;
}

const Button = ({ content, onClick }: ButtonProps) => {
  return (
    <button
      className='w-full rounded-md bg-primary text-white font-bold max-w-sm px-3 py-2'
      onClick={onClick}
    >
      {content}
    </button>
  );
};

export default Button;
