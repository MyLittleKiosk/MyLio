//절대 경로 사용이 불가합니다 !
import MENU_LIST from '../../../service/mock/dummies/menu';
import { CATEGORY_LIST } from '../../../service/mock/dummies/category';
import { OPTION_LIST } from '../../../service/mock/dummies/option';

describe('메뉴관리 페이지', () => {
  it('전체 메뉴 목록을 조회할 수 있다.', () => {
    //given - 메뉴 관리 페이지에 접근한다.
    cy.visit('/menus');

    //when - 메뉴 탭을 클릭 했을 때, 메뉴 목록을 조회한다.
    cy.get('#메뉴').click();

    cy.intercept('GET', '/api/menus', MENU_LIST);

    //then - 전체 메뉴 목록 조회에 성공한다.

    // 테이블이 존재하는지 확인
    cy.get('table').should('exist');

    // 테이블 제목 확인
    cy.contains('메뉴 목록').should('exist');

    // 메뉴 데이터가 테이블에 제대로 렌더링되었는지 확인
    cy.get('table tbody tr').should(
      'have.length',
      MENU_LIST.data.content.length
    );

    // 첫 번째 메뉴 데이터의 내용 확인
    cy.get('table tbody tr')
      .first()
      .within(() => {
        cy.contains(MENU_LIST.data.content[0].nameKr).should('exist');
      });

    // 메뉴 추가 버튼이 존재하는지 확인
    cy.contains('button', '메뉴 추가').should('exist');
  });
});

describe('카테고리 관리 페이지', () => {
  it('카테고리 목록을 조회할 수 있다.', () => {
    //given - 카테고리 관리 페이지에 접근한다.
    cy.visit('/menus');

    //when - 카테고리 탭을 클릭 했을 때, 카테고리 목록을 조회한다.
    cy.get('#카테고리').click();

    cy.intercept('GET', '/api/category?pageable=1', CATEGORY_LIST);

    //then - 카테고리 목록 조회에 성공한다.

    // 테이블이 존재하는지 확인
    cy.get('table').should('exist');

    // 테이블 제목 확인
    cy.contains('카테고리 목록').should('exist');

    // 카테고리 데이터가 테이블에 제대로 렌더링되었는지 확인
    cy.get('table tbody tr').should(
      'have.length',
      CATEGORY_LIST.data.content.length
    );

    // 첫 번째 카테고리 데이터의 내용 확인
    cy.get('table tbody tr')
      .first()
      .within(() => {
        cy.contains(CATEGORY_LIST.data.content[0].nameKr).should('exist');
      });
  });
});

describe('옵션관리 페이지', () => {
  it('옵션 목록을 조회할 수 있다.', () => {
    //given - 옵션 관리 페이지에 접근한다.
    cy.visit('/menus');

    //when - 옵션 탭을 클릭 했을 때, 옵션 목록을 조회한다.
    cy.get('#옵션').click();

    cy.intercept('GET', '/api/option', OPTION_LIST).as('getOptions');

    //then - 옵션 목록 조회에 성공한다.
    // 테이블이 존재하는지 확인
    cy.get('table').should('exist');

    // 옵션 관리 제목 확인
    cy.contains('옵션 관리').should('exist');

    // 테이블 제목 확인
    cy.contains('옵션 목록').should('exist');

    // 옵션 데이터가 테이블에 제대로 렌더링되었는지 확인
    cy.get('table tbody tr').should(
      'have.length',
      OPTION_LIST.data.options.length
    );

    // 첫 번째 옵션 데이터의 내용 확인
    cy.get('table tbody tr')
      .first()
      .within(() => {
        cy.contains(OPTION_LIST.data.options[0].optionNameKr).should('exist');
      });
  });
});
