#!/bin/bash
echo "Downloading JInsect lib"
curl -L "http://downloads.sourceforge.net/project/jinsect/JInsect%20v1.0/JInsect.jar?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fjinsect%2F&ts=1403946157&use_mirror=heanet" > JInsect.jar
echo "Downloading json library"
curl -L "http://central.maven.org/maven2/org/json/json/20140107/json-20140107.jar" > json.jar
echo "Downloading OpenJGraph library"
curl -L "http://manoet.altervista.org/stuff/OpenJGraph.jar" > OpenJGraph.jar
