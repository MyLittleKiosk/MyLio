describe('로그인 페이지', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('아이디 및 비밀번호를 입력후, 로그인 버튼 클릭 시 로그인 처리', () => {
    // given - 아이디 및 비밀번호 input 요소가 존재하고, 로그인 버튼이 존재한다.
    cy.get('#email').should('exist');
    cy.get('#password').should('exist');
    cy.get('button[type="submit"]').should('exist');
    // when - 아이디 및 비밀번호를 입력후, 로그인 버튼 클릭
    cy.get('#email').type('test');
    cy.get('#password').type('test');
    cy.get('button[type="submit"]').click();
    cy.intercept('POST', '/api/login', {
      statusCode: 200,
      body: {
        success: true,
        data: {
          user_id: 1,
          user_name: '홍길동',
          role: 'SUPER',
        },
        timestamp: '2025-05-08T01:26:53.695Z',
      },
    });
    // then - 성공 시 로그인 처리 후, 통계 페이지로 이동한다.
    cy.url().should('include', '/');
  });

  it('아이디 및 비밀번호를 입력후, 로그인 버튼 클릭 시 로그인 실패 처리', () => {
    // given - 아이디 및 비밀번호 input 요소가 존재하고, 로그인 버튼이 존재한다.
    cy.get('#email').should('exist');
    cy.get('#password').should('exist');
    cy.get('button[type="submit"]').should('exist');
    // when - 아이디 및 비밀번호를 입력후, 로그인 버튼 클릭
    cy.get('#email').type('test');
    cy.get('#password').type('test');
    cy.get('button[type="submit"]').click();
    cy.intercept('POST', '/api/login', {
      statusCode: 401,
      body: {
        success: false,
        error: {
          code: 'A004',
          message: '아이디 혹은 비밀번호가 일치하지 않습니다.',
        },
        timestamp: '2025-05-08T00:43:04.030570785',
      },
    });
    // then - 실패 시 alert가 표시된다.
    cy.on('window:alert', () => {
      return true;
    });
  });
});
