const formatMoney = (money: number) => {
  return money.toLocaleString('ko-KR', {
    style: 'currency',
    currency: 'KRW',
    minimumFractionDigits: 0,
  });
};

export default formatMoney;
