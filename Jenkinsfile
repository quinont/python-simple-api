pipeline {
    agent {
        label "python3"
    }
    environment {
        VERSION = '${BUILD_TAG}'
        DOCKER_HUB_REPOSITORY = 'quinont'
    }
    stages {
        stage('Revisando contenido') {
            steps {
                script {
                    sh """
                        ls -alF
                    """
                }
            }
        }
        stage('Install') {
            steps {
                script {
                    sh """
                        make install
                    """
                }
            }
        }
        stage('build') {
            steps {
                script {
                    sh """
                        make build
                    """
                }
            }
        }
        stage('test') {
            steps {
                script {
                    sh """
                        make test
                    """
                }
            }
        }
        stage('Build y push de la imagen') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'docker-hub-credentials', variable: 'DOCKER_HUB_CREDENTIALS')]) {
                        writeFile file: '/kaniko/.docker/config.json', text: "${DOCKER_HUB_CREDENTIALS}"
                        sh """
                            /kaniko/executor --log-format=text --cache=false --dockerfile ${WORKSPACE}/Dockerfile --destination=${DOCKER_HUB_REPOSITORY}/python-simple-api:${VERSION} --context=${WORKSPACE}/
                        """
                    }
                }
            }
        }
    }
}
