pipeline {
  agent any

  /************* 1. 공통 변수 계산 *************/
  stages {
    stage('Detect FE target & variables') {
      steps {
        script {
          /* ① MR 빌드면 CHANGE_BRANCH / CHANGE_ID, 아니면 BRANCH_NAME */
          def ref  = env.CHANGE_BRANCH ?: env.BRANCH_NAME
          def mrId = env.CHANGE_ID                      // null → 일반 브랜치 빌드

          /* ② FE 앱(admin | service) 추출 */
          def tokens = ref.tokenize('/')
          if (tokens.size() < 2)
              error "브랜치명에서 FE 앱을 찾지 못했습니다. (ref=${ref})"
          env.FE_APP = tokens[1]

          /* ③ 네이밍 규칙 */
          if (mrId) {                      // ── MR 빌드 ─────────────────────
            env.PROJECT_NAME = "fe-preview-${mrId}"    // docker-compose --project-name
            env.IMAGE_TAG    = "mr-${mrId}"            // fe-preview:mr-69
            env.PREVIEW_PATH = "/test/${mrId}/"
          } else {                         // ── 브랜치 빌드(dev, main 등) ──
            def safe = ref.replaceAll('/', '-')
                            .toLowerCase()
                            .replaceAll('[^a-z0-9_-]', '')
            env.PROJECT_NAME = "fe-preview-${safe}"
            env.IMAGE_TAG    = "${safe}"
            env.PREVIEW_PATH = "/test/${safe}/"
          }

          echo "▶ FE_APP        = ${env.FE_APP}"
          echo "▶ PROJECT_NAME  = ${env.PROJECT_NAME}"
          echo "▶ IMAGE_TAG     = ${env.IMAGE_TAG}"
          echo "▶ PREVIEW_PATH  = ${env.PREVIEW_PATH}"
        }
      }
    }

    /************* 2. Preview 앱 빌드·배포 *************/
    stage('Preview up (build+run)') {
      steps {
        sh """
          docker-compose \\
            -f docker-compose.preview.yml \\
            --project-name ${PROJECT_NAME} \\
            up -d --build --remove-orphans
        """
      }
    }
  }

  /************* 3. MR 종료 시 리뷰 앱 정리 *************/
  post {
    always {
      script {
        /* gitlabActionType: OPEN | REOPEN | UPDATE | MERGE | CLOSE */
        if (env.gitlabActionType in ['CLOSE', 'MERGE']) {
          echo "🧹 MR ${gitlabActionType} → cleaning review app"
          sh """
            docker-compose -f docker-compose.preview.yml \\
              --project-name ${PROJECT_NAME} down -v || true
            docker image rm -f fe-preview:${IMAGE_TAG} || true
          """
        } else {
          echo "🔖 MR still open (${gitlabActionType}) – preview container kept alive"
        }
      }
    }
  }
}
