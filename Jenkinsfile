pipeline{
	agent {label 'wrkr'}
	tools {
		maven 'mvn 3.5'
	}
	parameters {
    	string(name: 'quantity', defaultValue: '1', description: 'Quantity of app instances')
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
            	sh "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=eu-central-1 python3 ./scripts/app_instances.py ${params.quantity}"
        		}
    		}
    	}
		stage('provision'){
       		steps{
				parallel(
				db_provision : {
					withCredentials([sshUserPrivateKey(credentialsId: "ssh_key", keyFileVariable: 'keyfile'), file(credentialsId: 'vars', variable: 'vars')]){		 
					sh 'ansible-playbook ./scripts/playbookDB.yml -e "@${vars}" -i ./hosts --private-key=${keyfile} --ssh-common-args="-o StrictHostKeyChecking=no"'
					}
				},
				app_provision : {
					withCredentials([sshUserPrivateKey(credentialsId: "ssh_key", keyFileVariable: 'keyfile'), file(credentialsId: 'vars', variable: 'vars')]){	
					sh 'ansible-playbook ./scripts/PlaybookTST.yml -e "@${vars}" -i ./hosts --private-key=${keyfile} --ssh-common-args="-o StrictHostKeyChecking=no"'
					}	
				}
				)
        	}
		}
		stage('health check'){
			steps{
				withCredentials([[
            	$class: 'AmazonWebServicesCredentialsBinding',
            	credentialsId: 'aws_credent',
            	accessKeyVariable: 'AWS_ACCESS_KEY_ID',
            	secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        		]]) {
				sh "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=eu-central-1 python3 ./scripts/check.py"
				}
			}
		}
	}
}
