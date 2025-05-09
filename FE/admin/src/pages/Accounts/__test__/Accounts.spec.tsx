import DUMMY_ACCOUNT_LIST from '../../../service/mock/dummies/accounts';

describe('계정 관리 페이지', () => {
  it('매장 관리자 계정들을 조회할 수 있다.', () => {
    // given -  페이지에 접근한다.
    cy.intercept('GET', '/api/account?pageable=1').as('getAccounts');
    cy.visit('/accounts');

    // when -  어카운트 탭을 클릭 했을 때, 계정 목록을 조회한다.
    cy.wait('@getAccounts');

    cy.get('table').should('exist');

    // then -  테이블 제목 확인
    cy.get('h2').should('have.text', '계정 목록');
    cy.contains('계정 목록').should('exist');

    // then -  계정 목록 확인
    cy.get('table tbody tr').should(
      'have.length',
      DUMMY_ACCOUNT_LIST.accounts.length
    );

    cy.get('table tbody tr')
      .first()
      .within(() => {
        cy.contains(DUMMY_ACCOUNT_LIST.accounts[0].userName).should('exist');
      });
  });

  it('매장 관리자 계정을 추가할 수 있다.', () => {
    // given -  페이지에 접근한다.
    // HTTP 응답 설정
    cy.intercept('GET', '/api/account?pageable=1').as('getAccounts');
    cy.intercept('POST', '/api/account', {
      statusCode: 200,
      body: {
        success: true,
        data: {},
        timestamp: '2021-01-01T00:00:00.000Z',
      },
    }).as('createAccount');
    cy.visit('/accounts');

    // when -  계정 추가 버튼을 클릭 했을 때, 계정 추가 모달이 나타난다.
    cy.wait('@getAccounts');

    cy.contains('button', '계정 추가').click();

    // then -  계정 추가 모달이 나타난다.
    cy.get('#add-account-modal').should('exist');

    // then -  계정 추가 모달의 입력 필드에 값을 입력한다.
    cy.get('#account-name-input').type('홍길동');
    cy.get('#email-local-part-input').type('hong');
    cy.get('#email-domain-select').select('naver.com');
    cy.get('#store-name-input').type('카페 이름');
    cy.get('#address-input').type('서울특별시 강남구 강남대로 123');

    // then -  계정 추가 버튼을 클릭 했을 때, 계정 추가 요청이 성공한다.
    cy.get('button[type="submit"]').click();

    cy.contains('button', '확인').click();

    cy.wait('@createAccount');

    // then -  계정 추가 모달이 사라진다.
    cy.contains('h2', '계정 추가').should('not.exist');
  });

  it('매장 관리자 계정을 삭제할 수 있다.', () => {
    // given -  페이지에 접근한다.
    cy.intercept('GET', '/api/account?pageable=1').as('getAccounts');
    cy.intercept('DELETE', '/api/account/1', {
      statusCode: 200,
      body: {
        success: true,
        data: {},
        timestamp: '2021-01-01T00:00:00.000Z',
      },
    }).as('deleteAccount');
    cy.visit('/accounts');

    // when -  삭제 아이콘 버튼을 클릭 했을 때, 계정 삭제 모달이 나타난다.
    cy.wait('@getAccounts');

    // then -  계정 삭제 버튼을 클릭 했을 때, 계정 삭제 요청이 성공한다.
    cy.get('table tbody tr')
      .first()
      .within(() => {
        cy.get('td')
          .eq(4) // 4번째 td (삭제 아이콘)
          .within(() => {
            cy.get('button').click();
          });
      });

    // then -  계정 삭제 모달이 나타난다.
    cy.contains('button', '확인').click();

    cy.wait('@deleteAccount');

    // then -  계정 삭제 모달이 사라진다.
    cy.contains('button', '확인').should('not.exist');
  });
});
