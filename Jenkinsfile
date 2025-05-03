
pipeline {
  agent any
  environment {
    PREVIEW_TAG = BRANCH_NAME.replaceAll('/', '-')       // ex) feat-admin-login-page
    PREVIEW_DOMAIN = "mr-${PREVIEW_TAG}.preview.example.com"
  }

  stages {
    stage('Detect FE target') {        // ① admin 인지 service 인지 추출
      steps {
        script {
          /*
           * 브랜치 규칙: feat/<app>/<etc>
           * tokens[1] 이 'admin' 또는 'service'
           */
          def app = BRANCH_NAME.tokenize('/')[1]
          if (!app) { error "브랜치명에서 FE 앱을 찾지 못했습니다." }
          env.FE_APP = app          // Compose 에서 사용
          echo "▶ FE_APP = ${env.FE_APP}"
        }
      }
    }

    stage('Preview up (build+run)') {  // ② docker-compose 에 변수 넘김
      steps {
        sh """
          FE_APP=${FE_APP} \
          PREVIEW_TAG=${PREVIEW_TAG} \
          PREVIEW_DOMAIN=${PREVIEW_DOMAIN} \
          docker compose \
            -f docker-compose.preview.yml \
            --project-name fe-preview-${PREVIEW_TAG} \
            up -d --build --remove-orphans
        """
      }
    }
  }

  post {                              // ③ MR 닫힘·머지 시 정리
    cleanup {
      sh """
        FE_APP=${FE_APP} \
        docker compose -f docker-compose.preview.yml \
          --project-name fe-preview-${PREVIEW_TAG} down -v
        docker image rm -f fe-preview:${PREVIEW_TAG} || true
      """
    }
  }
}
