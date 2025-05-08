const translator = async (input: string) => {
  if (!input.trim()) return;

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'user',
            content: `You are translating terms for a cafe kiosk management system. 
            Translate the following Korean word to English, considering it might be a menu item, category (like coffee, tea, etc.), or option (like temperature, size, etc.). 
            Respond with just a single English word commonly used in cafe menus, without any explanation or punctuation: "${input}"`,
          },
        ],
        temperature: 0.3,
      }),
    });

    const data = await response.json();
    const result = data.choices?.[0]?.message?.content?.trim();
    return result || '번역 실패';
  } catch (error) {
    console.error(error);
    return '오류 발생';
  }
};

export default translator;
