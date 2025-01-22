pipeline {
    agent any
    environment{
        def VERSION=readFile('version.txt').trim()
        ECR_REPO_FRONT="600627353694.dkr.ecr.ap-south-1.amazonaws.com/dan/emulator-front"
        ECR_REPO_BACK="600627353694.dkr.ecr.ap-south-1.amazonaws.com/idan/notely-back"
        AWS_REGION="ap-south-1"
        AWS_ACOUNT_ID="600627353694"
        ADMIN_EMAIL="idancohen55@gmail.com"
        PRODUCT="notely"
        GIT_REPO="github.com/iddchn/notely_application.git"
    }

    stages {

        stage("Checkout") {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage("Unit Test") {
            steps {
                withPythonEnv('python3') {
                    sh """
                        echo "validate if python is installed"
                        if command -v python3 &> /dev/null; then
                            echo "Python3 installed."
                        else
                            echo "Python 3 is NOT installed."
                            echo "installing python requests package"
                        fi

                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r flask-notely/requirements.txt
                        echo "running unit test"
                        pytest
                    """
                }
            }
        }

        stage("Build") {
            steps {
                sh """
                cd flask-notely
                echo "running docker build for ${PRODUCT} flask Dockerfile version ${env.LATEST_TAG ?: VERSION}"
                docker build -t ${PRODUCT}_flask_image:${env.LATEST_TAG ?: VERSION} .
                echo "build flask image successful."
                cd ../notely-front
                docker build -t ${PRODUCT}_nginx_image:${env.LATEST_TAG ?: VERSION} .
                echo "build nginx image successful."
                """
            }
        }

        stage("Deploy") {
            steps {
                script {
                    withPythonEnv('python3') {
                        sh """
                            echo "validate if docker-compose is installed"
                            if command -v docker-compose &> /dev/null; then
                                echo "docker-compose is installed."
                            else
                                echo "docker compose is NOT installed."
                                echo "installing docker-compose"
                                apt-get install docker-compose-plugin
                                echo "docker compose installed successfully"
                            fi
                            echo "running ${PRODUCT} application on local container"
                            docker compose up -d
                        """
                    }
                }
            }
        }

        stage("Deploment Health Check") {
            steps {
                script {
                    sleep 10

                    def max_retries = 5
                    def retry_delay = 10
                    def retries = 0
                    def success = false

                    while (retries < max_retries && !success) {
                        try {
                            def status = sh(script: "curl -o /dev/null -s -w '%{http_code}' http://10.0.1.48:5001/health", returnStdout: true).trim()
                            echo "Health check status: ${status} ===================================="
                            if (status == '200'){
                                    success = true
                                echo "Backend health check succeeded!"
                            } else {
                                echo "throwing exception"
                                throw new Exception("Unexpected status code: ${status}")
                            }
                        } catch (Exception e) {
                            echo "retries: ${retries}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                            if (retries < max_retries) {
                                echo "${retries} is smaller then ${max_retries}"
                                retries++
                                echo "retries +1 : ${retries}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                                echo "Attempt ${retries} failed. Retrying in ${retry_delay} seconds..."
                                sleep retry_delay
                            } else {
                                echo "Health check failed ${retries} times. Marking as failed."
                                error "Failed to test backend health after ${max_retries} attempts."
                                exit 1
                            }
                        }
                    }
                }
            }
        }

        stage("E2E Test") {
            steps {
                script {
                    withPythonEnv('python3') {
                        sh """
                            echo "creating container finished successfully"

                            pip install requests
                            echo "running e2e test"
                            python flask-notely/testing_e2e.py
                            echo "e2e test finished successfully"
                        """
                    }
                }
            }
        }

        stage("Get release last tag") {
            when {
                expression {
                    ['main'].any {branch -> GIT_BRANCH?.contains(branch)}
                }
            }
            steps{
                script{
                    env.LATEST_TAG = createNewTagVersion(VERSION)
                    sh "echo 'latest tag: ${env.LATEST_TAG}'"
                }
            }
        }

        stage("Tag Commit Tag") {
            when {
                expression {
                   ['main'].any {branch -> GIT_BRANCH?.contains(branch)}
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'GitHub_user_pass', passwordVariable: 'GITHUB_PASSWORD', usernameVariable: 'GITHUB_USERNAME')]) {
                    script {
                        def commit_hash = sh(
                            script: "git rev-parse HEAD",
                            returnStdout: true
                        ).trim()

                       echo "commit hash is: ${commit_hash}"

                       sh """
                       git config --global user.name ${GITHUB_USERNAME}
                       git tag -a ${env.LATEST_TAG} -m "new tag for version ${env.LATEST_TAG}"
                       git push https://${GITHUB_USERNAME}:${GITHUB_PASSWORD}@${GIT_REPO} ${env.LATEST_TAG}
                       """
                    }
                }
            }
        }

        stage("Publish") {
            when {
                expression {
                    ['main'].any {branch -> GIT_BRANCH?.contains(branch)}
                }
            }
            steps {
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                        echo "Login to aws ecr"
                        aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin ${AWS_ACOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    """
                }

                sh """
                    echo "tagging ${PRODUCT} images"
                    docker tag ${PRODUCT}_flask_image:${env.LATEST_TAG ?: VERSION} ${ECR_REPO}:${env.LATEST_TAG ?: VERSION}
                    docker tag ${PRODUCT}_back_image:${env.LATEST_TAG ?: VERSION} ${ECR_REPO}:${env.LATEST_TAG ?: VERSION}
                    echo "pushing image to AES ECR"
                    docker push ${ECR_REPO_BACK}:${env.LATEST_TAG ?: VERSION}
                    docker push ${ECR_REPO_FRONT}:${env.LATEST_TAG ?: VERSION}
                """
            }
        }

    }

    post {
        always {
            script {
                sh """
                echo "cleanup e2e test container"
                echo "stopping ${PRODUCT} containers"
                docker compose down
                echo "deleting ${PRODUCT} images"
                docker rmi ${PRODUCT}_flask_image ${PRODUCT}_nginx_image mongo -f
                echo "deleting ${PRODUCT} volumes"
                docker volume prune -f
                """
            }
            emailext attachLog: true, body: '', recipientProviders: [developers()], subject: 'Build results', to: '${ADMIN_EMAIL}'
        }
    }

}

def createNewTagVersion(version) {
    try {
        def lastTag = sh(
            script: 'git describe --tags --abbrev=0',
            returnStdout: true
        ).trim()
        echo "lastTag: ${lastTag}"
        if (lastTag) {
            echo "there is a tag: ${lastTag}"
            def versionParts = lastTag.tokenize('.')
            versionParts[2] = (versionParts[2].toInteger() + 1).toString()
            def newTag = versionParts.join('.')
            echo "the new tag is: ${newTag}"
            return newTag
        }
    } catch (Exception e) {
        echo "there is no tag ${e.message}"
        def parts = version.tokenize('.')
        parts << "1"
        def tag = parts.join('.')
        echo "now the tag is: ${tag}"
        return tag
    }
}

