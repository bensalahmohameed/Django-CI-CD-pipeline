pipeline{
    agent any
    tools{
        jdk 'jdk17'
    }
    environment {
        SCANNER_HOME=tool 'sonar-scanner'
    }
    stages {
        stage('clean workspace'){
            steps{
                cleanWs()
            }
        }
        stage('Checkout from Git'){
            steps{
               git branch: 'main', url: 'https://github.com/bensalahmohameed/djangoApp'
            }
        }
        stage("Sonarqube Analysis "){
            steps{
                withSonarQubeEnv('sonar-server') {
                    sh ''' $SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=djangoApp \
                    -Dsonar.projectKey=djangoApp '''
                }
            }
        }
        stage('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('TRIVY FS SCAN') {
            steps {
                sh "trivy fs . > trivyfs.txt"
            }
        }
         stage("TRIVY"){
            steps{
                sh "trivy image saliih07/pythoncluster:final > trivy.txt" 
            }
        }
        stage("creating aks"){
            steps{
                sh '''cd terraform
                terraform init
                terraform validate
                terraform apply --auto-approve
            '''
            }
        }
        stage("deploying ingress controller"){
            steps{
                sh '''NAMESPACE=ingress-basic
                helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
                helm repo update
                helm install ingress-nginx ingress-nginx/ingress-nginx --create-namespace --namespace $NAMESPACE --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz'''
            }
        }
        stage("deploying the application"){
            steps{
                sh '''kubectl apply -f statefulsetmongodb.yaml
                kubectl apply -f mongo-express.yaml
                kubectl apply -f py.yaml
                kubectl apply -f aks-helloworld-one.yaml
                kubectl apply -f hello-world-ingress.yaml
            '''
            }
        }
    }
}