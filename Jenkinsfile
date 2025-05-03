pipeline {
  agent any

  /* ---------- 1) 환경변수 정의 ---------- */
  environment {
    // BRANCH_NAME 은 이미 Jenkins 가 넣어 주는 env 변수이므로
    PREVIEW_TAG    = "${env.BRANCH_NAME.replaceAll('/', '-')}"
    PREVIEW_DOMAIN = "mr-${env.PREVIEW_TAG}.preview.example.com"
    // FE_APP 은 뒤 stage 에서 동적으로 set
  }

  stages {
    stage('Detect FE target') {
      steps {
        script {
          def app = env.BRANCH_NAME.tokenize('/')[1]
          if (!app)  error "브랜치명에서 FE 앱을 찾지 못했습니다."
          env.FE_APP = app                 // ★ 여기서 FE_APP 확정
          echo "▶ FE_APP = ${env.FE_APP}"
        }
      }
    }

    stage('Preview up (build+run)') {
      steps {
        /* ---------- 2) 셸 안에서는 $FE_APP 로 그대로 쓰면 OK ---------- */
        sh """
          docker compose \
            -f docker-compose.preview.yml \
            --project-name fe-preview-${PREVIEW_TAG} \
            up -d --build --remove-orphans
        """
      }
    }
  }

  post {
    cleanup {
      /* ---------- 3) Groovy interpolation 을 쓸 땐 env.FE_APP ↓ ---------- */
      sh """
        docker compose -f docker-compose.preview.yml \
          --project-name fe-preview-${PREVIEW_TAG} down -v
        docker image rm -f fe-preview:${PREVIEW_TAG} || true
      """
    }
  }
}
