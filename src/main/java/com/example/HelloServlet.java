package com.example;

import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

public class HelloServlet extends HttpServlet {

    @Override
    protected void doGet(
            HttpServletRequest request,
            HttpServletResponse response) throws IOException {

        response.setContentType("text/html");

        String operation = request.getParameter("operation");
        String aParam = request.getParameter("a");
        String bParam = request.getParameter("b");

        String result = "Enter operation, a and b";

        if (operation != null && aParam != null && bParam != null) {
            try {
                double a = Double.parseDouble(aParam);
                double b = Double.parseDouble(bParam);

                result = switch (operation) {
                    case "add" -> String.valueOf(a + b);
                    case "subtract" -> String.valueOf(a - b);
                    case "multiply" -> String.valueOf(a * b);
                    case "divide" -> b != 0
                            ? String.valueOf(a / b)
                            : "Cannot divide by zero";
                    case "modulus" -> b != 0
                            ? String.valueOf(a % b)
                            : "Cannot calculate modulus by zero";
                    default -> "Unknown operation";
                };

            } catch (NumberFormatException e) {
                result = "Invalid numbers";
            }
        }

        response.getWriter().println("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>DevOps Calculator</title>
                </head>
                <body>
                    <h1>Hello from Gradle + Tomcat!</h1>
                    <h2>Calculator</h2>

                    <p>Supported operations:</p>
                    <ul>
                        <li>Addition</li>
                        <li>Subtraction</li>
                        <li>Multiplication</li>
                        <li>Division</li>
                        <li>Modulus</li>
                    </ul>

                    <p>Result: %s</p>

                    <p>Example:</p>
                    <p>?operation=add&amp;a=10&amp;b=5</p>

                    <p>CI/CD Practical Exercise 1</p>
                </body>
                </html>
                """.formatted(result));
    }
}
