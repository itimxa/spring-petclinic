pipeline{
	agent {label 'wrkr'}
	tools {
		maven 'mvn 3.5'
	}
	stages{
		stage('git clone'){
			steps{
			 checkout scm
			}
			}
		stage('build'){
			steps{
			sh 'mvn package'
			}
			}
		stage('up instances') {
    		steps {
        		withCredentials([[
            	$class: 'AmazonWebServicesCredentialsBinding',
            	credentialsId: 'aws_credent',
            	accessKeyVariable: 'AWS_ACCESS_KEY_ID',
            	secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        		]]) {
            	sh 'AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=eu-central-1 python3 ./scripts/app_instances.py'
        		}
    		}
    	}
		stage('provision'){
       		steps{
            	withCredentials([sshUserPrivateKey(credentialsId: "ssh_key", keyFileVariable: 'keyfile')], [file(credentialsId: 'vars', variable: 'vars.yml'){
				parallel(
				a : {		 
				sh 'ansible-playbook ./scripts/playbookDB.yml -e "@${vars.yml}" -i ./scripts/hosts --private-key=${keyfile}'
				},
				b : {
				sh 'ansible-playbook ./scripts/playbookAPP.yml -e "@${vars.yml}" -i ./scripts/hosts --private-key=${keyfile}'	
				}
				)
				}
        	}
		}
}
}