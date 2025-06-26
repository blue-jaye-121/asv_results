pipeline {
	agent  { label 'main' }
	stages {
		stage('Run ASV') {
			steps {
				sh 'bash ./benchmarks/asv_run_script.sh'
			}
		}
	}
}
