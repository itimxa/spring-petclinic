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
                sh "./Vagrant/vagrant_up_and_env.sh"
            }
        }
    }
}
