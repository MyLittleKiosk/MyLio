import postTranslator from '@/service/apis/translator';

async function translator(input: string) {
  try {
    const res = await postTranslator(input);
    const data = res.choices?.[0]?.message?.content?.trim();
    return data || '번역 실패';
  } catch {
    alert('번역 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
    return '번역 실패';
  }
}

export default translator;
