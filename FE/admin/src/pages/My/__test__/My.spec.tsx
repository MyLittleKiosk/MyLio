import DUMMY_MY_INFO from '../../../service/mock/dummies/my';

describe('마이페이지', () => {
  it('내 정보 조회', () => {
    // given -  인터셉터 설정
    cy.intercept('GET', '/api/account/detail', {
      success: true,
      data: DUMMY_MY_INFO,
      timestamp: new Date().toISOString(),
    }).as('getAccount');

    // given -  페이지에 접근한다.
    cy.visit('/my');

    // when -  내 정보 조회 페이지에 접근한다.
    cy.wait('@getAccount');

    // then - 정보가 정확히 조회됐는지 확인한다.
    cy.get('input[id="username"]').should('have.value', DUMMY_MY_INFO.userName);
    cy.get('input[id="email"]').should('have.value', DUMMY_MY_INFO.email);
    cy.get('input[id="storeName"]').should(
      'have.value',
      DUMMY_MY_INFO.storeName
    );
    cy.get('input[id="storeAddress"]').should(
      'have.value',
      DUMMY_MY_INFO.address
    );
  });
});
