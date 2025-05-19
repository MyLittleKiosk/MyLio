import DUMMY_ORDER_LIST from '../../../service/mock/dummies/order';
import { formatMoney } from '../../../utils/formatMoney';

describe('주문 관리 페이지', () => {
  // 로그인 정보 입력
  beforeEach(() => {
    cy.visit('/login');

    cy.get('#email').type('test@ssafy.io');
    cy.get('#password').type('qwer1234');

    cy.get('button[type="submit"]').click();
  });

  it('주문 목록을 조회할 수 있다.', () => {
    // given -  페이지에 접근한다.
    cy.intercept('GET', '/api/order_list?page=1', {
      statusCode: 200,
      body: {
        success: true,
        data: DUMMY_ORDER_LIST,
        timestamp: '2021-01-01T00:00:00.000Z',
      },
    }).as('getOrders');

    cy.visit('/orders');

    // when -  페이지에 접근한다.
    cy.wait('@getOrders');

    cy.get('table tbody tr').should('have.length', 3);

    // then -  페이지에 접근한다.
    cy.get('table tbody tr')
      .first()
      .within(() => {
        cy.contains(DUMMY_ORDER_LIST.content[0].orderId).should('exist');
      });
  });

  it('주문 상세 정보를 조회할 수 있다.', () => {
    // given -  페이지에 접근한다.
    cy.intercept('GET', '/api/order_list?page=1', {
      statusCode: 200,
      body: {
        success: true,
        data: DUMMY_ORDER_LIST,
        timestamp: '2021-01-01T00:00:00.000Z',
      },
    }).as('getOrders');

    cy.visit('/orders');

    // when -  페이지에 접근한다.
    cy.wait('@getOrders');

    cy.get('table tbody tr')
      .first()
      .within(() => {
        cy.contains(DUMMY_ORDER_LIST.content[0].orderId).should('exist');
      });

    cy.get('table tbody tr').first().click();

    cy.contains(
      `총 금액 :${formatMoney(DUMMY_ORDER_LIST.content[0].totalPrice)}`
    );
  });

  it('주문 목록의 다음 페이지로 넘어갈 수 있다.', () => {
    cy.intercept('GET', '/api/order_list?page=1', {
      statusCode: 200,
      body: {
        success: true,
        data: DUMMY_ORDER_LIST,
        timestamp: '2021-01-01T00:00:00.000Z',
      },
    }).as('getOrders');

    // given -  페이지에 접근한다.
    cy.visit('/orders');

    // when -  페이지에 접근한다.
    cy.wait('@getOrders');

    // then -  다음 페이지에 접근한다.
    // 이후 데이터는 더미로 처리할 수 없고 이동이 완료되는 걸로 테스트를 마무리한다.
    cy.get('#nextPage').click();
  });
});
