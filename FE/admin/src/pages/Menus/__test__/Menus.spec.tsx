//절대 경로 사용이 불가합니다 !
import MENU_LIST from '../../../service/mock/dummies/menu';

describe('메뉴관리 페이지', () => {
  it('전체 메뉴 목록을 조회할 수 있다.', () => {
    //given - 메뉴 관리 페이지에 접근한다.
    cy.visit('/menus');

    cy.get('#메뉴').click();

    cy.intercept('GET', '/api/menus', MENU_LIST);

    //then - 전체 메뉴 목록 조회에 성공한다.
    cy.get('table').should('exist');
  });
});
