import { KIOSK_LIST } from '../../../datas/kioskList';

describe('키오스크 관리 페이지', () => {
  beforeEach(() => {
    // 로그인 페이지 방문
    cy.visit('/login');

    // 로그인 정보 입력
    cy.get('#email').type('test@ssafy.io');
    cy.get('#password').type('qwer1234');

    // // 로그인 API 응답 모킹
    // cy.intercept('POST', '/api/auth/login', {
    //   statusCode: 200,
    //   body: {
    //     success: true,
    //     data: {
    //       email: 'test@ssafy.io',
    //       password: 'qwer1234',
    //     },
    //   },
    // }).as('loginRequest');

    // 로그인 버튼 클릭
    cy.get('button[type="submit"]').click();

    // 로그인 요청 완료 대기
    // cy.wait('@loginRequest');

    // 키오스크 API 요청 인터셉트 설정
    cy.intercept('GET', '/api/kiosk', {
      statusCode: 200,
      body: {
        success: true,
        data: KIOSK_LIST,
        timestamp: new Date().toISOString(),
      },
    }).as('getKioskList');
  });

  it('키오스크 목록을 전체 조회할 수 있다.', () => {
    //given - 키오스크 관리 페이지에 접근한다.

    cy.visit('/kiosks');

    //when - 키오스크 목록을 조회한다
    cy.wait('@getKioskList');

    // 테이블이 존재하는지 확인
    cy.get('table').should('exist');

    //키오스크 관리 제목 확인
    cy.contains('키오스크 목록').should('exist');

    // 첫 번째 옵션 데이터의 내용 확인
    cy.get('table tbody tr')
      .first()
      .within(() => {
        cy.contains(KIOSK_LIST.content[0].name).should('exist');
      });
  });

  it('키오스크를 추가할 수 있다.', () => {
    // API 요청 인터셉트 설정
    cy.intercept('POST', '/api/kiosk', {
      statusCode: 200,
      body: {
        success: true,
        data: {
          kiosk_id: 1,
          start_order: 'A',
          name: '키오스크 01',
          is_activate: false,
        },
        timestamp: new Date().toISOString(),
      },
    }).as('addKiosk');

    //given - 키오스크 관리 페이지에 접근한다.
    cy.visit('/kiosks');
    cy.wait('@getKioskList');

    //when - 키오스크 추가 버튼을 클릭한다.
    cy.contains('button', '키오스크 등록').click();

    // 모달이 나타나는지 확인
    cy.contains('키오스크 등록').should('exist');
    cy.contains('키오스크 정보를 등록합니다.').should('exist');

    // 키오스크명 입력
    cy.get('#kioskName').type('테스트 키오스크');

    // 그룹명 입력
    cy.get('#groupName').type('A');

    // API 요청 완료 대기
    // cy.wait('@addKiosk');

    // 저장 버튼 클릭
    cy.contains('button', '저장').click();
    // cy.get('#saveAddKiosk').click();

    // 성공 모달이 나타나는지 확인
    cy.contains('등록 성공').should('exist');
    cy.contains('키오스크 등록에 성공했습니다.').should('exist');

    // 성공 모달의 닫기 버튼 클릭
    cy.contains('button', '닫기').click();
  });

  it('키오스크를 수정할 수 있다.', () => {
    //given - 키오스크 관리 페이지에 접근한다.
    cy.visit('/kiosks');

    //when - 키오스크 목록의 첫 번째 항목의 수정 버튼을 클릭한다.
    cy.get('table tbody tr')
      .first()
      .find('td')
      .eq(3) // 수정 버튼이 있는 셀
      .find('#edit') // 수정 버튼 또는 아이콘
      .click();

    // 수정 모달이 나타나는지 확인
    cy.contains('키오스크 정보 수정').should('exist');
    cy.contains('키오스크 정보를 수정합니다.').should('exist');

    // 현재 키오스크명이 입력 필드에 있는지 확인
    cy.get('#kioskName').should('have.value', KIOSK_LIST.content[0].name);
    cy.get('#groupName').should('have.value', KIOSK_LIST.content[0].startOrder);

    // 키오스크명 수정
    const updatedName = '수정된 키오스크';
    cy.get('#kioskName').clear().type(updatedName);

    // 그룹명 수정
    const updatedGroup = 'B';
    cy.get('#groupName').clear().type(updatedGroup);

    // API 요청 인터셉트 설정
    cy.intercept('PATCH', `/api/kiosk/${KIOSK_LIST.content[0].kioskId}`, {
      statusCode: 200,
      body: {
        success: true,
        data: {},
        timestamp: new Date().toISOString(),
      },
    }).as('updateKiosk');

    // 저장 버튼 클릭
    cy.contains('button', '저장').click();

    // API 요청 완료 대기
    // cy.wait('@updateKiosk');

    // 성공 모달이 나타나는지 확인
    cy.contains('수정 성공').should('exist');
    cy.contains('키오스크 수정에 성공했습니다.').should('exist');

    // 성공 모달의 닫기 버튼 클릭
    cy.contains('button', '닫기').click();
  });

  it('키오스크를 삭제할 수 있다.', () => {
    //given - 키오스크 관리 페이지에 접근한다.
    cy.visit('/kiosks');

    //when - 키오스크 목록의 첫 번째 항목의 삭제 버튼을 클릭한다.
    cy.get('table tbody tr')
      .first()
      .find('td:last-child button:last-child, td:last-child svg:last-child')
      .last() // 여러 요소 중 마지막 요소만 선택
      .click();

    // 삭제 모달이 나타나는지 확인
    cy.contains('삭제 확인').should('exist');

    // API 요청 인터셉트 설정
    cy.intercept('DELETE', `/api/kiosk/${KIOSK_LIST.content[0].kioskId}`, {
      statusCode: 200,
      body: {
        success: true,
        data: {},
        timestamp: new Date().toISOString(),
      },
    }).as('deleteKiosk');

    // API 요청 완료 대기
    // cy.wait('@deleteKiosk');

    // 삭제 버튼 클릭
    cy.get('#deleteKioskBtn').click();

    // 성공 모달이 나타나는지 확인
    cy.contains('삭제 성공').should('exist');

    // 성공 모달의 확인 버튼 클릭
    cy.contains('button', '확인').click();
  });
});
