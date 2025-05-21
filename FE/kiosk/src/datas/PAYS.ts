import card from '@/assets/images/card.png';
import gift from '@/assets/images/gift.png';
import kakaoPay from '@/assets/images/kakao_pay.png';
import phone from '@/assets/images/phone.png';

export const PAY_METHODS = [
  {
    id: 'CARD',
    name: '카드',
    image: card,
  },
  {
    id: 'PAY',
    name: '카카오페이',
    image: kakaoPay,
  },
  {
    id: 'GIFT',
    name: '기프티콘',
    image: gift,
  },
  {
    id: 'MOBILE',
    name: '모바일상품권',
    image: phone,
  },
];
