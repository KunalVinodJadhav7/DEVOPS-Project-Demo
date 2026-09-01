# Experiment 6 – Java Gradle Build, Testing & Git

## 🎯 Aim

To configure the Java development environment, verify Gradle installation, execute a Java Gradle project, resolve JUnit test dependencies, generate test reports, and push the complete project to a GitHub branch.

---

# 1. 💻 Environment

| Component | Details |
|---|---|
| Operating System | Windows 11 |
| Java | Eclipse Adoptium JDK 21.0.9 LTS |
| Gradle | 9.7.0 |
| Kotlin | 2.4.0 |
| Groovy | 4.0.32 |
| JVM | Java 21.0.9 |
| Architecture | AMD64 |
| Project | Experiment 6 |
| Repository | DEVOPS-Project-Demo |
| Branch | EXPERIMENT-7 |

---

# 2. ☕ Java Configuration

The `JAVA_HOME` environment variable was configured to use Eclipse Adoptium JDK 21.

```cmd
set "JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.9.10-hotspot"

The configured Java home was verified using:

echo %JAVA_HOME%

Output
C:\Program Files\Eclipse Adoptium\jdk-21.0.9.10-hotspot

The Java bin directory was added to the PATH:

set "PATH=%JAVA_HOME%\bin;%PATH%"

Java installation was verified using:

where java

Output
C:\Program Files\Eclipse Adoptium\jdk-21.0.9.10-hotspot\bin\java.exe
C:\Program Files\Common Files\Oracle\Java\javapath\java.exe
C:\Program Files (x86)\Common Files\Oracle\Java\java8path\java.exe

The Eclipse Adoptium JDK 21 installation was successfully detected.

3. 🔨 Gradle Verification
Gradle was verified using:

gradle -version

Output
------------------------------------------------------------
Gradle 9.7.0
------------------------------------------------------------

Build time:    2026-08-06 14:07:35 UTC
Revision:      3defbfc59d757b873d787b2261de5c7f8a00970a

Kotlin:        2.4.0
Groovy:        4.0.32
Ant:            Apache Ant(TM) version 1.10.17 compiled on April 6 2026
Launcher JVM:  21.0.9 (Eclipse Adoptium 21.0.9+10-LTS)
Daemon JVM:    C:\Program Files\Eclipse Adoptium\jdk-21.0.9.10-hotspot
OS:            Windows 11 10.0 amd64

Gradle Environment Summary
Gradle: 9.7.0
Java: 21.0.9
JVM: Eclipse Adoptium
Operating System: Windows 11
Architecture: AMD64
4. 📁 Project Directory
The project is located at:

C:\Users\VIT.VIT-SYS-332\DevOps_Kunal\Experiment 6

The correct project directory was accessed using:

cd "C:\Users\VIT.VIT-SYS-332\DevOps_Kunal\Experiment 6"

5. ⚠️ Initial Gradle Error
The first attempt to execute Gradle was made from the user home directory:

C:\Users\VIT.VIT-SYS-332

The following command was executed:

gradle clean test

This resulted in an error because the home directory did not contain a Gradle project.

Error
Directory 'C:\Users\VIT.VIT-SYS-332' does not contain a Gradle build.

A Gradle build's root directory should contain one of the possible
settings files: settings.gradle, settings.gradle.kts, settings.gradle.dcl.

It may also contain one of the possible build files:
build.gradle, build.gradle.kts, build.gradle.dcl.

Solution
The terminal was moved to the correct Gradle project directory:

cd "C:\Users\VIT.VIT-SYS-332\DevOps_Kunal\Experiment 6"

6. 🧪 Running Gradle Tests
The project was then tested using:

gradle clean test

The initial test execution failed because the JUnit Platform launcher/dependencies were not available on the test runtime classpath.

Error
Execution failed for task ':test'.

Could not start Gradle Test Executor 1.

Failed to load JUnit Platform.

Please ensure that all JUnit Platform dependencies are available
on the test's runtime classpath, including the JUnit Platform launcher.

7. 🔄 Resolving JUnit Dependencies
The Gradle dependencies were refreshed using:

gradle clean test --refresh-dependencies

This forced Gradle to download and refresh the required dependencies.

Result
BUILD SUCCESSFUL in 9s
3 actionable tasks: 3 executed

The project tests were successfully executed after refreshing the dependencies.

8. 📊 Test Results
Gradle generated the test results in:

build\test-results\test

The generated JUnit XML report was:

build\test-results\test\TEST-tests.ExampleTest.xml

The test result directory was verified using:

dir build\test-results\test

Output
Directory of C:\Users\VIT.VIT-SYS-332\DevOps_Kunal\Experiment 6\build\test-results\test

01-09-2026  12:04    <DIR>          .
01-09-2026  12:04    <DIR>          ..
01-09-2026  12:04    <DIR>          binary
01-09-2026  12:04             1,037 TEST-tests.ExampleTest.xml

9. 🧾 Test Class
The executed test class was:

tests.ExampleTest

The generated JUnit XML report was:

TEST-tests.ExampleTest.xml

The XML report was located using:

dir /s /b build\test-results\test\*.xml

Output
C:\Users\VIT.VIT-SYS-332\DevOps_Kunal\Experiment 6\build\test-results\test\TEST-tests.ExampleTest.xml

10. 📄 HTML Test Report
Gradle also generated an HTML test report.

The report was opened using:

start build\reports\tests\test\index.html

Report Location
build\reports\tests\test\index.html

The HTML report provides a visual representation of the executed test cases and their results.

11. 📦 Generated Build Structure
After successful execution, Gradle generated the following test-report structure:

Experiment 6
│
├── build
│   ├── reports
│   │   └── tests
│   │       └── test
│   │           └── index.html
│   │
│   └── test-results
│       └── test
│           ├── binary
│           └── TEST-tests.ExampleTest.xml
│
├── build.gradle
├── settings.gradle
└── ...
