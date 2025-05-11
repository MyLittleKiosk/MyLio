describe('Login', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.intercept('POST', 'https://k12b102.p.ssafy.io/api/auth/login', {
      statusCode: 200,
      body: {
        success: true,
        data: {
          userId: 1,
          userName: 'test',
          role: 'KIOSK',
        },
      },
    }).as('login');
  });

  it('id, 비밀번호, 키오스크 id를 입력하고 로그인 버튼을 누르면 로그인 성공', () => {
    // given - 로그인 페이지 접속 후, id, 비밀번호, kiosk id 폼 입력
    cy.get('input[id="email"]').type('test@test.com');
    cy.get('input[id="password"]').type('test1234');
    cy.get('input[id="kiosk"]').type('1');
    // when - 로그인 버튼 클릭
    cy.get('button[type="submit"]').click();
    cy.wait('@login').its('response.statusCode').should('eq', 200);
    // then - 로그인 성공
    cy.url().should('include', '/kiosk');
  });
});
