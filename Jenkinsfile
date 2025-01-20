pipeline {
    agent any
    environment{
        def VERSION=readFile('version.txt').trim()
        ECR_REPO="600627353694.dkr.ecr.ap-south-1.amazonaws.com/idan/notely"
        AWS_REGION="ap-south-1"
        AWS_ACOUNT_ID="600627353694"
        ADMIN_EMAIL="idancohen55@gmail.com"
        PRODUCT="notely"
    }

    stages {

        stage("Get release last tag and branch mane") {
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
                echo "running docker build for ${PRODUCT} Dockerfile version ${env.LATEST_TAG ?: VERSION}"
                docker build -t ${PRODUCT}_image:${env.LATEST_TAG ?: VERSION} .
                echo "build image successful."
                """
            }
        }

        stage("E2E Test") {
            steps {
                withPythonEnv('python3') {
                    sh """
                        echo "validate if docker-compose is installed"
                        if command -v docker-compose &> /dev/null; then
                            echo "docker-compose is installed."
                        else
                            echo "docker-compose is NOT installed."
                            echo "installing docker-compose"
                            apt-get install -y docker-compose
                            echo "docker-compose installed successfully"
                        fi
                        echo "running ${PRODUCT} application on local container"
                        docker-compose up -d
                        echo "creating container finished successfully"

                        echo "running e2e test"
                        python e2e_test.py
                        echo "e2e test finished successfully"
                    """
                }
            }
        }

        stage("Tag Commit") {
            when {
                expression {
                   ['main'].any {branch -> GIT_BRANCH?.contains(branch)}
                }
            }
            steps {
                script {
                    def commit_hash = sh(
                        script: "git rev-parse HEAD",
                        returnStdout: true
                    ).trim()

                   echo "commit hash is: ${commit_hash}"

                   sh """
                   git tag ${env.LATEST_TAG} ${commit_hash}
                   git push origin ${env.LATEST_TAG}
                   """
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
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: '1', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                    echo "Login to aws ecr"
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${AWS_ACOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    """
                }

                sh """
                echo "creating tag for docker ${PRODUCT}_image"
                docker tag ${PRODUCT}_image:${env.LATEST_TAG ?: VERSION} ${ECR_REPO}:${env.LATEST_TAG ?: VERSION}
                echo "pushing image to AES ECR"
                docker push ${ECR_REPO}:${env.LATEST_TAG ?: VERSION}
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
                docker-compose down
                echo "deleting ${PRODUCT} images"
                docker rmi nginx flask mongo
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

