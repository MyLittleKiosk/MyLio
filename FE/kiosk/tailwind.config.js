/** @type {import('tailwindcss').Config} */
// import typography from '@tailwindcss/typography';

export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    screens: {
      mobile: '344px', // mobile(344px) 이상
      sm: '375px', // 스마트폰 모바일(세로) ~ 479px
      md: '480px', // 스마트폰 모바일(가로) & 태블릿 세로
      lg: '768px', // 태블릿 가로
      xl: '1024px', // 노트북 & 이외 사이즈
    },
    fontFamily: {
      preExtraLight: [
        'Pretendard-ExtraLight',
        'NotoSans-ExtraLight, sans-serif',
      ],
      preLight: ['Pretendard-Light', 'NotoSans-Light', 'sans-serif'],
      preRegular: ['Pretendard-Regular', 'NotoSans-Regular', 'sans-serif'],
      preMedium: ['Pretendard-Medium', 'NotoSans-Medium', 'sans-serif'],
      preSemiBold: ['Pretendard-SemiBold', 'NotoSans-SemiBold', 'sans-serif'],
      preBold: ['Pretendard-Bold', 'NotoSans-Bold', 'sans-serif'],
      preExtraBold: [
        'Pretendard-ExtraBold',
        'NotoSans-ExtraBold',
        'sans-serif',
      ],
    },
    extend: {
      colors: {
        white: '#FFFFFF',
        offWhite: '#FAF9F6',
        title: '#202020',
        longContent: '#3C3C3C',
        content: '#828282',
        content2: '#9D9D9D',
        subContent: '#DDDDDD',
        primary: '#5D85FE',
        secondary: '#BECEFF',
        error: '#D44848',
      },
      backgroundImage: {
        jihyegra: 'linear-gradient(to top, #b73abb, #d0579a, #e46e80)',
      },
      keyframes: {
        ripple: {
          '0%': { width: '0', height: '0', opacity: '0.5' },
          '100%': { width: '500px', height: '500px', opacity: '0' },
        },
      },
      animation: {
        ripple: 'ripple 1s cubic-bezier(0, 0, 0.2, 1)',
      },
      typography: (theme) => ({
        large: {
          css: {
            fontSize: theme('fontSize.xl'), // 기본 폰트 크기
            h1: { fontSize: theme('fontSize.4xl') },
            h2: { fontSize: theme('fontSize.3xl') },
            p: { fontSize: theme('fontSize.lg') },
          },
        },
      }),
    },
  },
  plugins: [],
};
