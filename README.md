Experiment 6 – Java Gradle Build and Testing
Aim

To configure the Java environment, execute a Gradle-based Java project, resolve test dependencies, and verify successful execution of JUnit tests using Gradle.

Environment
Component	Version / Details
Operating System	Windows 11
Java	Eclipse Adoptium JDK 21.0.9 LTS
Gradle	9.7.0
Kotlin	2.4.0
Groovy	4.0.32
JVM	Java 21.0.9
Architecture	AMD64
Java Configuration

The JAVA_HOME environment variable was configured to point to the Eclipse Adoptium JDK 21 installation.

set "JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.9.10-hotspot"


The Java bin directory was then added to the system PATH:

set "PATH=%JAVA_HOME%\bin;%PATH%"


The active Java executable was verified using:

where java


The Eclipse Adoptium Java 21 installation was detected successfully.

Gradle Verification

Gradle was verified using:

gradle -version


The configured environment reported:

Gradle 9.7.0
Launcher JVM: 21.0.9 (Eclipse Adoptium 21.0.9+10-LTS)
Daemon JVM: C:\Program Files\Eclipse Adoptium\jdk-21.0.9.10-hotspot
OS: Windows 11 10.0 amd64

Project Directory

The Gradle project was located at:

C:\Users\VIT.VIT-SYS-332\DevOps_Kunal\Experiment 6


The initial attempt to run Gradle from the user home directory failed because that directory did not contain a Gradle build.

Directory 'C:\Users\VIT.VIT-SYS-332' does not contain a Gradle build.


The correct project directory was then selected:

cd "C:\Users\VIT.VIT-SYS-332\DevOps_Kunal\Experiment 6"

Running Tests

The following command was used to clean the project and execute the tests:

gradle clean test


The first test execution failed because the JUnit Platform launcher/dependencies were not available on the test runtime classpath.

The dependencies were refreshed using:

gradle clean test --refresh-dependencies


The build then completed successfully:

BUILD SUCCESSFUL in 9s
3 actionable tasks: 3 executed

Test Results

Gradle generated the test results in:

build\test-results\test


The generated XML test report was:

build\test-results\test\TEST-tests.ExampleTest.xml


The test report directory was verified using:

dir build\test-results\test


The HTML test report was opened using:

start build\reports\tests\test\index.html

Test Report

The generated test report contains the results for:

tests.ExampleTest


JUnit XML result:

TEST-tests.ExampleTest.xml

Commands Used

The main commands executed during the experiment were:

set "JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.9.10-hotspot"

echo %JAVA_HOME%

set "PATH=%JAVA_HOME%\bin;%PATH%"

where java

gradle -version

cd "C:\Users\VIT.VIT-SYS-332\DevOps_Kunal\Experiment 6"

gradle clean test

gradle clean test --refresh-dependencies

dir build\test-results\test

start build\reports\tests\test\index.html

dir /s /b build\test-results\test\*.xml

Outcome

The Java 21 and Gradle 9.7 environment was successfully configured and verified.

The Gradle project was executed from the correct project directory. The initial JUnit dependency issue was resolved by refreshing Gradle dependencies, after which the project tests completed successfully.

Final Status: BUILD SUCCESSFUL

Conclusion

The experiment demonstrated the setup and verification of a Java Gradle development environment on Windows. Java 21 was configured using JAVA_HOME, Gradle 9.7 was verified, and the project's JUnit tests were successfully executed after refreshing dependencies. Gradle also generated XML and HTML test reports for verification.
