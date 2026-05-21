# Order Service Test Proof

- Test date: `2026-05-02 00:05:58 +07:00`
- Workspace: `C:\Users\ADMIN\Desktop\Seminar chuyên đề\Week8 - Vibe Engineering\microservices_api_demo\microservices_api_demo`
- Module: `order-service`
- Java used: `C:\Program Files\Java\jdk-21`

## Command

```powershell
$env:JAVA_HOME='C:\Program Files\Java\jdk-21'
$env:Path='C:\Program Files\Java\jdk-21\bin;' + $env:Path
mvn -pl order-service test
```

## Result

```text
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0 -- in vn.hdbank.intern.orderservice.OrderServiceIntegrationTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0 -- in vn.hdbank.intern.orderservice.service.OrderServiceUnitTest
[INFO] Results:
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
[INFO] Finished at: 2026-05-02T00:05:58+07:00
```

## Notes

- Maven defaulted to Java 8 before override, so the test run was executed with JDK 21 explicitly.
- The run completed successfully after switching `JAVA_HOME` and `PATH` to JDK 21.
