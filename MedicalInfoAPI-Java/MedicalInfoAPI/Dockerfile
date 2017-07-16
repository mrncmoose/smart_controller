FROM tomcat:8.5.13-jre8

#TODO's
# ref: https://tomcat.apache.org/tomcat-8.5-doc/manager-howto.html#Introduction 
# create and copy a manager.xml to $CATALINA_BASE/conf/[enginename]/[hostname]
# set up users & passwords in $CATALINA_BASE/conf/tomcat-users.xml  (read the comments!)
# add the role of manager-script, manger-gui & manager-status to the manager user

# in the docker tomcat image:
# CATALINA_BASE:   /usr/local/tomcat
# CATALINA_HOME:   /usr/local/tomcat

# configure for SSL
COPY ./server.xml /usr/local/tomcat/conf/server.xml

ENV DB_HOST="127.0.0.1" \
	DB_PASSWORD="mo!800ose" \
	DB_USER="proxyuser"

WORKDIR /usr/local/tomcat/conf

# If the deploy by file copy works on GCP, this will not be needed.
#ADD ./tomcat-users.xml /usr/local/tomcat/conf/
#ADD ./context.xml /usr/local/tomcat/conf/

# deploy our WAR file
# TODO:  make this part of the maven build
# TODO:  rename war file to just 'MedicalInfoAPI'.  The entire WAR file name is part of the URL.
COPY ./target/MedicalInfoAPI-0.0.1-SNAPSHOT.war /usr/local/tomcat/webapps/

# create the SSL certs
RUN $JAVA_HOME/bin/keytool -genkeypair -noprompt -alias tomcat -dname "CN=backtothepatient.com, OU=ID, O=BackToThePatient, L=Moose, S=NY, C=US" -keyalg RSA -keystore $CATALINA_HOME/conf/localhost-rsa.jks -storepass changeit -keypass changeit

EXPOSE 8080 8443

