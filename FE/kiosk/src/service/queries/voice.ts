import { gcpTts } from '@/service/apis/voice';
import { useMutation } from '@tanstack/react-query';

export function useTTS() {
  return useMutation({
    mutationFn: (text: string) => gcpTts(text),
    onSuccess: (data) => {
      const audio = new Audio(URL.createObjectURL(data));
      audio.play();
    },
  });
}
