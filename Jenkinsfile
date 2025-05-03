pipeline {
  agent any

  stages {
    /* ─────────── 1) 공통 변수 계산 ─────────── */
    stage('Detect FE target & variables') {
      steps {
        script {
          /* ① MR 빌드면 CHANGE_BRANCH, 아니면 BRANCH_NAME */
          def ref = env.CHANGE_BRANCH ?: env.BRANCH_NAME

          /* ② FE 앱(admin | service) 추출 */
          def tokens = ref.tokenize('/')
          if (tokens.size() < 2)  error "브랜치명에서 FE 앱을 찾지 못했습니다. (ref=${ref})"
          env.FE_APP = tokens[1]

          /* ③ Compose 프로젝트·태그·도메인용 safe-name */
          env.PREVIEW_TAG = ref
                             .replaceAll('/', '-')      // / → -
                             .toLowerCase()             // 소문자
                             .replaceAll('[^a-z0-9_-]', '') // 허용 문자만
          env.PREVIEW_DOMAIN = "mr-${env.PREVIEW_TAG}.preview.example.com"

          echo "▶ FE_APP        = ${env.FE_APP}"
          echo "▶ PREVIEW_TAG   = ${env.PREVIEW_TAG}"
          echo "▶ PREVIEW_DOMAIN= ${env.PREVIEW_DOMAIN}"
        }
      }
    }

    /* ─────────── 2) Preview 앱 빌드·배포 ─────────── */
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

  /* ─────────── 3) MR 종료 시 정리 ─────────── */
  post {
    always {
      script {
        /* gitlabActionType: OPEN | REOPEN | UPDATE | MERGE | CLOSE (GitLab Branch Source) */
        if (env.gitlabActionType in ['CLOSE', 'MERGE']) {
          echo "🧹 MR ${gitlabActionType} → cleaning review app"
          sh """
            docker-compose -f docker-compose.preview.yml \
              --project-name fe-preview-${TAG} down -v || true
            docker image rm -f fe-preview:${TAG} || true
          """
        } else {
          echo "🔖 MR still open (${gitlabActionType}) – keep preview container running"
         }
      }
    }
  }
}
