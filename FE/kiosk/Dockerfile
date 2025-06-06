######################## 1단계 ─ Build ########################
FROM node:20.10.0-alpine AS build

# Yarn Berry는 Corepack으로 관리
RUN corepack enable && corepack prepare yarn@stable --activate

WORKDIR /app

# Berry 프로젝트는 lockfile + .yarnrc.yml + .yarn/releases 등을 함께 복사
COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn/ .yarn/

# 의존성 설치 (Berry 표준)
RUN yarn install

ARG BASE_PATH=/
ARG VITE_PUBLIC_API_URL
ARG VITE_OPENAI_API_KEY
ARG VITE_PUBLIC_VOICE_API_URL

ENV BASE_PATH ${BASE_PATH}
ENV VITE_PUBLIC_API_URL ${VITE_PUBLIC_API_URL}
ENV VITE_OPENAI_API_KEY ${VITE_OPENAI_API_KEY}
ENV VITE_PUBLIC_VOICE_API_URL ${VITE_PUBLIC_VOICE_API_URL}

# 애플리케이션 소스 복사 → 빌드
COPY . .
RUN yarn build      # scripts.build 정의(CRA면 react-scripts, Vite면 vite build)

######################## 2단계 ─ Runtime ########################
FROM nginx:alpine

# (CRA: /app/build,   Vite: /app/dist) → 실제 폴더명 확인
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
