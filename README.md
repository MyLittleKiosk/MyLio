# MyLio
<div align="center">
<img src="https://github.com/user-attachments/assets/70f18ea9-21ad-4d27-bfc6-aa573236e90e" alt="마이리오 로고"/>
</div>

## 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [서비스 화면](#서비스-화면)
3. [기술 스택](#기술-스택)
4. [서비스 아키텍처](#서비스-아키텍처)
5. [ERD](#erd)
6. [팀 소개](#팀-소개)

## 프로젝트 개요

### 📋 **서비스 개요**
생성형 AI 기반 음성인식 키오스크

기존 키오스크의 불편한 사용자 경험을 개선하기 위한 프로젝트입니다.
- **기간:** 2025/4/14 ~ 2025/5/22

### 💰 **서비스 기능**

1. **음성인식 키오스크**
   - 사용자는 음성을 기반으로 키오스크를 활용할 수 있습니다.

2. **절차 생략 주문**
   - "아이스 아메리카노 작은거 하나 카드 결제"와 같이 메뉴, 옵션, 결제 수단을 한 번에 말해 기존의 여러번의 터치가 필요했던 키오스크의 주문방식을 개선했습니다.

3. **메뉴 필터링**
   - "우유 없는 메뉴" 등과 같이 특정 조건을 가진 메뉴들을 검색할 수 있습니다.

4. **다중 주문**
   - 여러개의 메뉴를 한번에 주문할 수 있습니다.

5. **서비스 백오피스**
    - 서비스 관리자 및 서비스 사용자를 위한 백오피스 기능을 제공합니다.
    - 서비스 관리자와 서비스 사용자는 메뉴, 키오스크, 주문, 원재료, 영양성분, 계정정보를 관리할 수 있습니다.
    - 서비스 사용자를 위한 주문 통계를 제공합니다.

## 서비스 화면

### 키오스크

<div align="center">
    <img src="https://github.com/user-attachments/assets/1d217148-0bdf-4bba-8169-a1f63ad275e1" width="30%" alt="옵션 선택"/>
    <img src="https://github.com/user-attachments/assets/64a1087c-313b-4027-8316-4c2a99ed3638" width="30%" alt="메뉴 상세"/>
    <img src="https://github.com/user-attachments/assets/42f06a6c-28e7-48cd-b94e-46e25920aa81" width="30%" alt="메뉴 상세"/>
</div>

### 백오피스

<div align="center">
    <img src="https://github.com/user-attachments/assets/df20a022-34bc-43f5-981d-b4d6937d57b2" width="30%" alt="주문 통계계"/>
    <img src="https://github.com/user-attachments/assets/ecfef17a-983a-4486-b748-a6ddbe3ea483" width="30%" alt="메뉴 추가가"/>
    <img src="https://github.com/user-attachments/assets/8a106403-21f4-4869-aeab-9db971a2c488" width="30%" alt="메뉴 목록록"/>
</div>


## 기술 스택

**Frontend** <br> ![React](https://img.shields.io/badge/react-61DAFB.svg?style=for-the-badge&logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-3178C6.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Yarn Berry](https://img.shields.io/badge/yarn_berry-2C8EBB.svg?style=for-the-badge&logo=yarn&logoColor=white)
![tailwind](https://img.shields.io/badge/tailwind-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Zustand](https://img.shields.io/badge/zustand-E26529.svg?style=for-the-badge&logo=zustand&logoColor=white)
![React Query](https://img.shields.io/badge/react_query-FF4154.svg?style=for-the-badge&logo=reactquery&logoColor=white)
![Axios](https://img.shields.io/badge/axios-000000.svg?style=for-the-badge&logo=axios&logoColor=white)

**Backend** <br> ![Java](https://img.shields.io/badge/java-3670A0?style=for-the-badge&logo=java&logoColor=ffdd54)
![Spring](https://img.shields.io/badge/spring_boot-6DB33F.svg?style=for-the-badge&logo=springboot&logoColor=white)
![Spring Data JPA](https://img.shields.io/badge/spring_data_jpa-6DB33F.svg?style=for-the-badge&logo=springdatajpa&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

**AI** <br> ![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=FFFFFF)
![Fast API](https://img.shields.io/badge/Fast_API-009688.svg?style=for-the-badge&logo=FastAPI&logoColor=white)
![OpenAI](https://img.shields.io/badge/openAI-412991.svg?style=for-the-badge&logo=openai&logoColor=white)

**DevOps** <br> ![NginX](https://img.shields.io/badge/NginX-009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/jenkins-D24939.svg?style=for-the-badge&logo=jenkins&logoColor=white)
![Amazon EC2](https://img.shields.io/badge/amazon_ec2-FF9900.svg?style=for-the-badge&logo=amazonec2&logoColor=white)

**Tools** <br> ![GitLab](https://img.shields.io/badge/gitlab-FC6D26.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Intellij IDEA](https://img.shields.io/badge/Intelij_IDEA-000000?style=for-the-badge&logo=intellijidea&logoColor=white)
![Swagger](https://img.shields.io/badge/swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Figma](https://img.shields.io/badge/figma-F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)
![Jira](https://img.shields.io/badge/Jira-%23FFFFFF.svg?style=for-the-badge&logo=jira&logoColor=blue)

<br>

## 서비스 아키텍처
![Image](https://github.com/user-attachments/assets/cb23b17f-07ba-4cc4-852c-d834978b4afb)

<br>

## ERD

![Image](https://github.com/user-attachments/assets/d61f2e6c-b5ff-4cf8-86b8-3838eadcfa93)

<br>

## 팀 소개

| 이름           | 역할 및 구현 기능                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------------------- |
| 🟧이하영(팀장) | **Frontend**<br>- 관리자 페이지 퍼블리싱 및 API 연결<br>  - 키오스크 반응형 화면 UI/UX<br>                             |
| 🟩강성엽       | **Frontend**<br>- 매출별 통계 차트 구현<br>- 음성 인식 구현 (Clova, GCP TTS)<br>                               |
| 🟦이해루       | **Frontend**<br>- 키오스크 라우팅 구조 설계 및 키오스크 구현<br>- Threshold 기반 음성 인식 구현<br>                                    |
| 🟥신지혜       | **Backend**<br>- 매장 관리자 기능 구현<br>- 서비스 관리자 기능 구현<br>- FastAPI 통신 및 키오스크 주문 검증 로직 구현<br>
| 🟨이병조       | **Infra/Backend**<br>- Docker, docker-compose 기반 시스템 아키텍쳐 구축 <br>- Jenkins CI/CD <br>- S3 연동 모듈 구현구축<br>                           |
| 🟪전아현       | **Backend/AI**<br>- AI 주문 처리 전체 흐름 구현 <br>- Spring 기반 백엔드 아키텍처 설계 <br>- 주문 처리 LLM 기반 프롬프팅<br>- 로그인 기능 구현 <br>- FastAPI 구현                   |
