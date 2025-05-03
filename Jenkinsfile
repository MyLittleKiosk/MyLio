pipeline {
  agent any

  /* ───── 1) 브랜치명을 안전한 태그로 변환 ───── */
  environment {
    // ① '/' → '-'  ② 소문자 변환  ③ a-z0-9_- 이외 문자는 공백으로 제거
    PREVIEW_TAG = "${env.BRANCH_NAME
                      .replaceAll('/', '-')
                      .toLowerCase()
                      .replaceAll('[^a-z0-9_-]', '')}"
    PREVIEW_DOMAIN = "mr-${env.PREVIEW_TAG}.preview.example.com"
  }

  stages {
    stage('Detect FE target') {
      steps {
        script {
          def ref = env.CHANGE_BRANCH ?: env.BRANCH_NAME       // MR이면 CHANGE_BRANCH 사용
          def tokens = ref.tokenize('/')
          if (tokens.size() < 2) {
            error "브랜치명에서 FE 앱을 찾지 못했습니다. (ref=${ref})"
          }
          env.FE_APP = tokens[1]          // admin 또는 service
          echo "▶ FE_APP = ${env.FE_APP}"
          echo "▶ PREVIEW_TAG = ${env.PREVIEW_TAG}"
        }
      }
    }

    stage('Preview up (build+run)') {
      steps {
        sh """
          docker-compose \\
            -f docker-compose.preview.yml \\
            --project-name fe-preview-${PREVIEW_TAG} \\
            up -d --build --remove-orphans
        """
      }
    }
  }

  post {
    cleanup {
      sh """
        docker-compose -f docker-compose.preview.yml \\
          --project-name fe-preview-${PREVIEW_TAG} down -v || true
        docker image rm -f fe-preview:${PREVIEW_TAG} || true
      """
    }
  }
}
