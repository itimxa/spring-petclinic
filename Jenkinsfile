pipeline {
    agent any 
    stages {
        stage('git clone'){
          steps{
              checkout scm
          }  
        }
        stage('everything') { 
            steps {
                sh "chmod +x ./Vagrant/vagrant_up_and_env.sh"
                sh "cd ./Vagrant"
                sh "./vagrant_up_and_env.sh"
            }
        }
    }
}
