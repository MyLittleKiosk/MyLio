export function parseState(state: string) {
  switch (state) {
    case 'MAIN':
      return '/';
    case 'ORDER':
      return 'ORDER';
    case 'SEARCH':
      return '/search';
    case 'DETAIL':
      return '/detail';
    case 'CONFIRM':
      return '/confirm';
    case 'SELECT_PAY':
      return '/select-pay';
    case 'PAY':
      return '/pay';
    default:
      return '/';
  }
}
