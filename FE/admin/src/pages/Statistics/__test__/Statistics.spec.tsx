import { DUMMY_DAILY_SALES } from '../../../service/mock/dummies/statistics';
import { formatMoney } from '../../../utils/formatMoney';

describe('통계 대시보드 페이지', () => {
  it('오늘의 매출과 주문 건수를 확인할 수 있다.', () => {
    // given - 통계 대시보드 페이지에 접근한다.
    cy.visit('/');

    // when - 통계 대시보드 페이지에 접근한다.
    // 오늘의 매출&주문건수를 조회한다.
    cy.intercept('GET', '/api/sales/daily', {
      body: {
        success: true,
        data: DUMMY_DAILY_SALES,
        timestamp: '2025-05-08T01:26:53.695Z',
      },
    });

    // then - 오늘의 매출&주문건수가 테이블에 제대로 렌더링되었는지 확인
    // 정확한 제목으로 이뤄진 텍스트가 존재하는지 확인
    cy.get('h1').should('exist');
    cy.contains('오늘의 총 매출').should('exist');
    cy.contains('오늘의 주문 건수').should('exist');

    // 데이터가 정확히 들어왔는지 확인
    cy.get('section article p').should('have.length', 2);
    cy.get('section article p')
      .first()
      .should('have.text', formatMoney(DUMMY_DAILY_SALES.totalSales));
    cy.get('section article p')
      .last()
      .should('have.text', `${DUMMY_DAILY_SALES.totalOrders} 건`);
  });
});
