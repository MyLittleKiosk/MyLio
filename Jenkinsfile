properties([
  pipelineTriggers([
    [$class: 'GenericTrigger',
      genericVariables: [
        [key: 'action', value: '$.object_attributes.action']
      ],
      tokenCredentialId: 'JENKINS-WH',
      causeString: 'GitLab MR action: $action',
      printPostContent: true,
      printContributedVariables: true,
      regexpFilterText: '$action',
      regexpFilterExpression: '^(open|reopen|merge|close)$'
    ]
  ])
])

pipeline {
  agent any
         
  /************* 1. 공통 변수 계산 *************/
  stages {
    stage('Detect FE target & variables') {
      steps {
        script {
          def ref  = env.CHANGE_BRANCH ?: env.BRANCH_NAME
          def mrId = env.CHANGE_ID

          def tokens = ref.tokenize('/')
          if (tokens.size() < 2)
              error "브랜치명에서 FE 앱을 찾지 못했습니다. (ref=${ref})"
          env.FE_APP = tokens[1]

          if (mrId) {
            env.PROJECT_NAME = "fe-preview-${mrId}"
            env.IMAGE_TAG    = "mr-${mrId}"
            env.BASE_PATH = "/test/${mrId}/"
          } else {
            def safe = ref.replaceAll('/', '-')
                          .toLowerCase()
                          .replaceAll('[^a-z0-9_-]', '')
            env.PROJECT_NAME = "fe-preview-${safe}"
            env.IMAGE_TAG    = "${safe}"
            env.BASE_PATH = "/test/${safe}/"
          }

          echo "▶ FE_APP        = ${env.FE_APP}"
          echo "▶ PROJECT_NAME  = ${env.PROJECT_NAME}"
          echo "▶ IMAGE_TAG     = ${env.IMAGE_TAG}"
          echo "▶ BASE_PATH    = ${env.BASE_PATH}"
        }
      }
    }

    /************* 2. Preview 앱 빌드·배포 *************/
    stage('Build Preview') {
      steps {
        sh '''
          BASE_PATH=${BASE_PATH} IMAGE_TAG=${IMAGE_TAG} \
          docker-compose -f docker-compose.preview.yml \
            --project-name ${PROJECT_NAME} \
            build --no-cache fe-preview
          
          # 네트워크 이름 = ${PROJECT_NAME}_default
          docker network connect ${PROJECT_NAME}_default nginx-lb || true
        '''
      }
    }

    stage('Deploy Preview') {
      steps {
        sh '''
         BASE_PATH=${BASE_PATH} IMAGE_TAG=${IMAGE_TAG} \
          docker-compose -f docker-compose.preview.yml \
           --project-name ${PROJECT_NAME} \
            up -d --force-recreate --remove-orphans fe-preview
        '''
      }
    }
  }

  /************ 3. MR 종료 시 리뷰 앱 정리 ************/
post {
  always {
    script {
      def action = env.gitlabActionType

      if (action && action in ['CLOSE', 'MERGE']) {
        echo "🧹 MR ${action} → cleaning review app"
        sh """
          docker network disconnect ${network} nginx-lb || true
          docker-compose -f docker-compose.preview.yml \\
            --project-name ${PROJECT_NAME} down -v || true
          docker image rm -f fe-preview:${IMAGE_TAG} || true
          docker network rm ${network} || true
        """
      } else {
        echo "🔖 Not a MR close/merge (gitlabActionType=${action}) – skipping cleanup"
      }
    }
  }
}

}