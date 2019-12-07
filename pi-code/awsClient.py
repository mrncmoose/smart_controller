from time import sleep
from baseAWSclient import baseAWSmqClient

if __name__ == '__main__':
    myClient = baseAWSmqClient()
    myClient.connect()
    myClient.makeRequest('temperature')
    for i in range(1,60):
        sleep(1)
        if myClient.currentTemp is not None:
            print('Current temperature: {0}'.format(myClient.currentTemp))
            myClient.currentTemp = None
            exit(0)
        print('Waiting for message')
    