import paramiko




def execute_command(command):
	with paramiko.SSHClient() as ssh:
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect('5.189.180.87',username='sshtest', password='test')
		stdin, stdout, stderr = ssh.exec_command(command)
	
	return stdout


def show_output(input_value):
	print(rstring)
	rstring = input_value.read().decode('utf-8')
	rstring = rstring.split('\n')

	for line in rstring:
		print(line)

show_output(execute_command("ps aux"))
