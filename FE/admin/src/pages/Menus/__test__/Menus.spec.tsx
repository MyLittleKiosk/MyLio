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

  it('카테고리를 추가할 수 있다.', () => {
    //given - 메뉴 관리 페이지 - 카테고리 탭에 접근한다.
    cy.visit('/menus');
    cy.get('#카테고리').click();

    //when - 카테고리 추가 버튼을 클릭하고, 한글 메뉴명을 입력한다. 입력 후 '번역하기' 버튼을 클릭해 영문명을 생성한다.
    cy.contains('button', '카테고리 추가').click();

    // 모달이 나타나는지 확인
    cy.contains('새 카테고리 추가').should('exist');

    // 카테고리명 입력
    cy.get('#categoryAdd').type('커피');

    // 번역하기 버튼 클릭
    cy.contains('button', '번역하기').click();

    // 번역된 영문명이 나타날 때까지 대기
    cy.get('#engCategory').should('have.value', 'Coffee');

    // API 요청 인터셉트 및 응답 확인 (추가 버튼 클릭 전에 인터셉트 설정)
    cy.intercept('POST', '/api/category', {
      statusCode: 200,
      body: {
        success: true,
        data: {},
        timestamp: new Date().toISOString(),
      },
    }).as('addCategory');

    // alert 메시지를 확인하기 위한 spy 설정
    const alertStub = cy.stub();
    cy.on('window:alert', alertStub);

    // 추가 버튼 클릭 (force: true 옵션 추가)
    cy.get('#addCategory')
      .click({ force: true })
      .then(() => {
        // alert 메시지 확인
        cy.on('window:alert', () => {
          cy.wrap(alertStub).should('be.calledWith', '등록에 성공했습니다.');
        });
      });

    // 모달이 닫혔는지 확인
    cy.contains('새 카테고리 추가').should('not.exist');
    //then - 추가 버튼을 클릭해 카테고리 추가에 성공한다.
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

  it('옵션 그룹을 추가할 수 있다.', () => {
    //given - 메뉴 관리 페이지 - 옵션 탭에 접근한다.
    cy.visit('/menus');
    cy.get('#옵션').click();

    //when - 옵션 그룹 추가 버튼을 클릭하고, 한글 옵션 그룹명을 입력한다.
    cy.contains('button', '옵션 그룹 추가').click();

    // 모달이 나타나는지 확인
    cy.contains('dialog', '옵션 그룹 추가').should('exist');

    // 옵션 그룹명 입력
    cy.get('#optionGroupAdd').type('사이즈');

    // 번역하기 버튼 클릭
    cy.contains('button', '번역하기').click();

    // 번역된 영문명이 나타날 때까지 대기
    cy.get('#engOptionGroup').should('have.value', 'Size');

    // API 요청 인터셉트 설정 (클릭 직전에 설정)
    cy.intercept('POST', '/api/option', {
      statusCode: 200,
      body: {
        success: true,
        data: {},
        timestamp: new Date().toISOString(),
      },
    }).as('addOptionGroup');

    // alert 메시지를 확인하기 위한 spy 설정
    const alertStub = cy.stub();
    cy.on('window:alert', alertStub);

    // 추가 버튼 클릭
    cy.get('#addOptionGroup')
      .click({ force: true })
      .then(() => {
        // alert 메시지 확인
        cy.wrap(alertStub).should('be.calledWith', '등록에 성공했습니다.');
      });

    // 모달이 닫혔는지 확인
    cy.contains('dialog', '옵션 그룹 추가').should('not.exist');
  });

  it('옵션 그룹을 수정할 수 있다.', () => {
    //given - 메뉴 관리 페이지 - 옵션 탭에 접근한다.
    cy.visit('/menus');
    cy.get('#옵션').click();

    //when - 옵션 목록의 첫 번째 항목의 수정 버튼을 클릭한다.
    cy.get('table tbody tr')
      .first()
      .find('td')
      .eq(2) // 수정 버튼이 있는 셀
      .find('#edit')
      .click();

    // 수정 모달이 나타나는지 확인
    cy.contains('옵션 편집').should('exist');

    // 현재 옵션 그룹명이 입력 필드에 있는지 확인
    cy.get('#optionGroupNameEdit').should(
      'have.value',
      OPTION_LIST.data.options[0].optionNameKr
    );
    cy.get('#optionGroupNameEnEdit').should(
      'have.value',
      OPTION_LIST.data.options[0].optionNameEn
    );

    // 옵션 그룹명 수정
    const updatedName = '수정된 옵션명';
    cy.get('#optionGroupNameEdit').clear().type(updatedName);

    // API 요청 인터셉트 설정
    cy.intercept(
      'PATCH',
      `/api/option/${OPTION_LIST.data.options[0].optionId}`,
      {
        statusCode: 200,
        body: {
          success: true,
          data: {},
          timestamp: new Date().toISOString(),
        },
      }
    ).as('editOptionGroup');

    // 수정 버튼 클릭
    cy.get('#optionGroupNameEdit')
      .parents('form')
      .find('button[type="submit"]')
      .click();

    // 성공 모달이 나타나는지 확인
    cy.contains('dialog', '옵션 그룹명 수정').should('exist');
    cy.contains('옵션 그룹명 수정이 완료되었습니다.').should('exist');

    // 성공 모달의 확인 버튼 클릭
    cy.contains('button', '확인').click();
  });

  it('옵션 그룹을 삭제할 수 있다.', () => {
    //given - 메뉴 관리 페이지 - 옵션 탭에 접근한다.
    cy.visit('/menus');
    cy.get('#옵션').click();

    //when - 옵션 목록의 첫 번째 항목의 삭제 아이콘을 클릭한다.
    cy.get('table tbody tr')
      .first()
      .find('td')
      .last()
      .find('svg') // 삭제 아이콘(IconTrashCan)
      .click();

    // 삭제 확인 모달이 나타나는지 확인
    cy.contains('삭제 확인').should('exist');

    // API 요청 인터셉트 설정
    cy.intercept(
      'DELETE',
      `/api/option/${OPTION_LIST.data.options[0].optionId}`,
      {
        statusCode: 200,
        body: {
          success: true,
          data: {},
          timestamp: new Date().toISOString(),
        },
      }
    ).as('deleteOption');

    // 삭제 버튼 클릭
    cy.contains('button', '삭제').click();

    // 성공 모달이 나타나는지 확인
    cy.contains('삭제 성공').should('exist');

    // 성공 모달의 확인 버튼 클릭
    cy.contains('button', '확인').click();

    // 모달이 닫혔는지 확인
    cy.contains('삭제 확인').should('not.exist');
  });

  it('옵션 상세를 추가할 수 있다.', () => {
    //given - 메뉴 관리 페이지 - 옵션 탭에 접근한다.
    cy.visit('/menus');
    cy.get('#옵션').click();

    //when - 옵션 목록의 첫 번째 항목의 수정 버튼을 클릭한다.
    cy.get('table tbody tr')
      .first()
      .find('td')
      .eq(2) // 수정 버튼이 있는 셀
      .find('#edit')
      .click();

    // 모달이 나타나는지 확인
    cy.contains('dialog', '옵션 상세 추가').should('exist');

    // 옵션 상세명 입력
    cy.get('#optionDetailNameAdd').type('사이즈');

    // 가격 입력
    cy.get('#optionDetailPriceAdd').type('1000');

    // API 요청 인터셉트 설정 (클릭 직전에 설정)
    cy.intercept('POST', '/api/option_detail/:optionId', {
      statusCode: 200,
      body: {
        success: true,
        data: {},
        timestamp: new Date().toISOString(),
      },
    }).as('addOptionDetail');

    // 추가 버튼 클릭
    cy.get('#optionDetailAdd')
      .click({ force: true })
      .then(() => {
        // 모달이 나타나는지 확인
        cy.contains('dialog', '추가 성공').should('exist');

        // 확인 버튼 클릭
        cy.contains('button', '확인').click();
      });

    // 모달이 닫혔는지 확인
    cy.contains('dialog', '옵션 상세 추가').should('not.exist');
  });

  it('옵션 상세를 수정할 수 있다.', () => {
    //given - 메뉴 관리 페이지 - 옵션 탭에 접근한다.
    cy.visit('/menus');
    cy.get('#옵션').click();

    //when - 옵션 목록의 첫 번째 항목의 수정 버튼을 클릭한다.
    cy.get('table tbody tr')
      .first()
      .find('td')
      .eq(2) // 수정 버튼이 있는 셀
      .find('#edit')
      .click();

    // 수정 모달이 나타나는지 확인
    cy.contains('옵션 편집').should('exist');

    // 옵션 상세 테이블이 존재하는지 확인
    cy.contains('옵션 상세').should('exist');
    cy.get('table').eq(1).should('exist'); // 두 번째 테이블(옵션 상세 테이블)

    // 첫 번째 옵션 상세의 값을 수정
    const updatedDetailName = '라지 사이즈';
    const updatedPrice = 2000;

    // 첫 번째 옵션 상세의 이름 수정
    cy.get(
      `#optionDetailValueEdit-${OPTION_LIST.data.options[0].optionDetail[0].optionDetailId}`
    )
      .clear()
      .type(updatedDetailName);

    // 첫 번째 옵션 상세의 가격 수정
    cy.get(
      `#optionDetailPriceEdit-${OPTION_LIST.data.options[0].optionDetail[0].optionDetailId}`
    )
      .clear()
      .type(updatedPrice.toString());

    // API 요청 인터셉트 설정
    cy.intercept(
      'PATCH',
      `/api/option_detail/${OPTION_LIST.data.options[0].optionDetail[0].optionDetailId}`,
      {
        statusCode: 200,
        body: {
          success: true,
          data: {},
          timestamp: new Date().toISOString(),
        },
      }
    ).as('editOptionDetail');

    // 수정 버튼 클릭
    cy.get('#optionDetailEdit').first().click();

    // 성공 모달이 나타나는지 확인
    cy.contains('dialog', '옵션 상세 수정').should('exist');
    cy.contains('옵션 상세 수정이 완료되었습니다.').should('exist');

    // 성공 모달의 확인 버튼 클릭
    cy.contains('button', '확인').click();
  });

  it('옵션 상세를 삭제할 수 있다.', () => {
    //given - 메뉴 관리 페이지 - 옵션 탭에 접근한다.
    cy.visit('/menus');
    cy.get('#옵션').click();

    //when - 옵션 목록의 첫 번째 항목의 수정 버튼을 클릭한다.
    cy.get('table tbody tr')
      .first()
      .find('td')
      .eq(2) // 수정 버튼이 있는 셀
      .find('#edit')
      .click();

    // 수정 모달이 나타나는지 확인
    cy.contains('옵션 편집').should('exist');

    // 옵션 상세 테이블이 존재하는지 확인
    cy.contains('옵션 상세').should('exist');
    cy.get('table').eq(1).should('exist'); // 두 번째 테이블(옵션 상세 테이블)

    // API 요청 인터셉트 설정
    cy.intercept(
      'DELETE',
      `/api/option_detail/${OPTION_LIST.data.options[0].optionDetail[0].optionDetailId}`,
      {
        statusCode: 200,
        body: {
          success: true,
          data: {},
          timestamp: new Date().toISOString(),
        },
      }
    ).as('deleteOptionDetail');

    // 삭제 버튼 클릭
    cy.get('#optionDetailDelete').first().click();

    // 성공 모달이 나타나는지 확인
    cy.contains('dialog', '옵션 상세 삭제').should('exist');
    cy.contains('옵션 상세 삭제가 완료되었습니다.').should('exist');

    // 성공 모달의 확인 버튼 클릭
    cy.contains('button', '확인').click();
  });
});
