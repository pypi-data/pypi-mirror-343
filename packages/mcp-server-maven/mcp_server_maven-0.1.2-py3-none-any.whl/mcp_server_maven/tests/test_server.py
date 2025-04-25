from mcp_server_maven.server import extract_important_maven_output


def test_extract_important_maven_output():
    test_content="""

-------------------------------------------------------
 T E S T S
-------------------------------------------------------
Running com.jd.bdp.ide.domain.TryRunSqlInfoTest
Tests run: 28, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.12 sec - in com.jd.bdp.ide.domain.TryRunSqlInfoTest
Running com.jd.bdp.ide.domain.DataIdeShareDataTest
Tests run: 23, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.ide.domain.DataIdeShareDataTest
Running com.jd.bdp.ide.domain.DataIdeClientInfoTest
Tests run: 26, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 sec - in com.jd.bdp.ide.domain.DataIdeClientInfoTest
Running com.jd.bdp.ide.domain.DataIdeSqlOperationLogTest
Tests run: 114, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.022 sec - in com.jd.bdp.ide.domain.DataIdeSqlOperationLogTest
Running com.jd.bdp.ide.domain.enums.DataIdeShareDataStatusEnumTest
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.ide.domain.enums.DataIdeShareDataStatusEnumTest
Running com.jd.bdp.ide.domain.enums.DataIdeEngineTypeEnumTest
Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.055 sec - in com.jd.bdp.ide.domain.enums.DataIdeEngineTypeEnumTest
Running com.jd.bdp.ide.domain.enums.QueueStatusEnumTest
Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 sec - in com.jd.bdp.ide.domain.enums.QueueStatusEnumTest
Running com.jd.bdp.ide.domain.enums.SpaceMarkEnumTest
Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.607 sec - in com.jd.bdp.ide.domain.enums.SpaceMarkEnumTest
Running com.jd.bdp.ide.domain.enums.DataIdeUploadStatusEnumTest
Tests run: 26, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.ide.domain.enums.DataIdeUploadStatusEnumTest
Running com.jd.bdp.ide.domain.enums.DataIdeExecStatusEnumTest
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.ide.domain.enums.DataIdeExecStatusEnumTest
Running com.jd.bdp.ide.domain.DataIdeSqlOperationOnlineLogTest
Tests run: 30, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.ide.domain.DataIdeSqlOperationOnlineLogTest
Running com.jd.bdp.ide.domain.bo.DataIdeUploadFileParamTest
Tests run: 20, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.ide.domain.bo.DataIdeUploadFileParamTest
Running com.jd.bdp.ide.domain.bo.UgdapQueueResultTest
Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.ide.domain.bo.UgdapQueueResultTest
Running com.jd.bdp.ide.domain.bo.MarketResultTest
Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.ide.domain.bo.MarketResultTest
Running com.jd.bdp.ide.domain.bo.UgdapMarketInfoResultTest
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.ide.domain.bo.UgdapMarketInfoResultTest
Running com.jd.bdp.ide.domain.bo.QueueUsedResultV2Test
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.ide.domain.bo.QueueUsedResultV2Test
Running com.jd.bdp.ide.domain.bo.MetadataTableDetailQueryTest
Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.ide.domain.bo.MetadataTableDetailQueryTest
Running com.jd.bdp.ide.domain.bo.UgdapBusinessLineResultTest
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.ide.domain.bo.UgdapBusinessLineResultTest
Running com.jd.bdp.ide.domain.bo.UgdapTableResultTest
Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.ide.domain.bo.UgdapTableResultTest
Running com.jd.bdp.ide.domain.bo.QueryQueueBOTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.ide.domain.bo.QueryQueueBOTest
Running com.jd.bdp.ide.domain.bo.JobInfoResultTest
Tests run: 22, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.ide.domain.bo.JobInfoResultTest
Running com.jd.bdp.ide.domain.bo.MetadataTableDetailResultTest
Tests run: 97, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.01 sec - in com.jd.bdp.ide.domain.bo.MetadataTableDetailResultTest
Running com.jd.bdp.ide.domain.bo.UgdapAuthMarketTest
Tests run: 19, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.ide.domain.bo.UgdapAuthMarketTest
Running com.jd.bdp.ide.domain.TryRunSqlFinishInfoTest
Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.ide.domain.TryRunSqlFinishInfoTest
Running com.jd.bdp.ide.domain.DataIdeSqlOperationLogOnlineExecContentTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.ide.domain.DataIdeSqlOperationLogOnlineExecContentTest
Running com.jd.bdp.ide.domain.DataIdeUploadFileTest
Tests run: 93, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 sec - in com.jd.bdp.ide.domain.DataIdeUploadFileTest
Running com.jd.bdp.datadev.dto.ScriptManagerParamDtoTest
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.dto.ScriptManagerParamDtoTest
Running com.jd.bdp.datadev.dto.SearchFileDtoTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.dto.SearchFileDtoTest
Running com.jd.bdp.datadev.dto.BuffaloScriptSynParamDtoTest
Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.dto.BuffaloScriptSynParamDtoTest
Running com.jd.bdp.datadev.dto.ScriptFileDtoTest
Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.dto.ScriptFileDtoTest
Running com.jd.bdp.datadev.dto.ScriptCheckParamDtoTest
Tests run: 26, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.dto.ScriptCheckParamDtoTest
Running com.jd.bdp.datadev.dto.SqlToolsProblemsDtoTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.dto.SqlToolsProblemsDtoTest
Running com.jd.bdp.datadev.dto.MetadataFieldQueryTest
Tests run: 17, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.dto.MetadataFieldQueryTest
Running com.jd.bdp.datadev.dto.BuffaloScriptSynResultDtoTest
Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.dto.BuffaloScriptSynResultDtoTest
Running com.jd.bdp.datadev.dto.SqlToolsResultDtoTest
Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.dto.SqlToolsResultDtoTest
Running com.jd.bdp.datadev.vo.ScriptManagerVoTest
Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.vo.ScriptManagerVoTest
Running com.jd.bdp.datadev.vo.PageResultVoTest
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.vo.PageResultVoTest
Running com.jd.bdp.datadev.vo.TableInfoVoTest
Tests run: 30, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.vo.TableInfoVoTest
Running com.jd.bdp.datadev.vo.ScriptCheckVoTest
Tests run: 23, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 sec - in com.jd.bdp.datadev.vo.ScriptCheckVoTest
Running com.jd.bdp.datadev.enums.DataDevScriptLockStatusEnumTest
Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.DataDevScriptLockStatusEnumTest
Running com.jd.bdp.datadev.enums.TableCheckTypeEnumTest
Tests run: 41, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 sec - in com.jd.bdp.datadev.enums.TableCheckTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptUploadStatusEnumTest
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.DataDevScriptUploadStatusEnumTest
Running com.jd.bdp.datadev.enums.DataDevFileDetailOperTypeEnumTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.enums.DataDevFileDetailOperTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevGitOrCodingEnumTest
Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 sec - in com.jd.bdp.datadev.enums.DataDevGitOrCodingEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptFunTypeEnumTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.enums.DataDevScriptFunTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptEngineTypeEnumTest
Tests run: 28, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 sec - in com.jd.bdp.datadev.enums.DataDevScriptEngineTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevFunStatusEnumTest
Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.enums.DataDevFunStatusEnumTest
Running com.jd.bdp.datadev.enums.PublishTypeEnumTest
Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.PublishTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevGitInitFlagTest
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.DataDevGitInitFlagTest
Running com.jd.bdp.datadev.enums.ScriptPublishCheckEnumTest
org.junit.ComparisonFailure: expected:<Success> but was:<null>
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at com.jd.bdp.datadev.enums.ScriptPublishCheckEnumTest.testEnumValueOf(ScriptPublishCheckEnumTest.java:45)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:47)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:44)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:271)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:70)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:50)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runners.Suite.runChild(Suite.java:127)
	at org.junit.runners.Suite.runChild(Suite.java:26)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:160)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:138)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.createRequestAndRun(JUnitCoreWrapper.java:141)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.executeEager(JUnitCoreWrapper.java:114)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.execute(JUnitCoreWrapper.java:86)
	at org.apache.maven.surefire.junitcore.JUnitCoreProvider.invoke(JUnitCoreProvider.java:134)
	at org.apache.maven.surefire.booter.ForkedBooter.invokeProviderInSameClassLoader(ForkedBooter.java:200)
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:153)
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:103)
org.junit.ComparisonFailure: expected:<"[result]"> but was:<"[]">
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at com.jd.bdp.datadev.enums.ScriptPublishCheckEnumTest.testToMessage(ScriptPublishCheckEnumTest.java:34)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:47)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:44)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:271)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:70)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:50)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runners.Suite.runChild(Suite.java:127)
	at org.junit.runners.Suite.runChild(Suite.java:26)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:160)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:138)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.createRequestAndRun(JUnitCoreWrapper.java:141)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.executeEager(JUnitCoreWrapper.java:114)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.execute(JUnitCoreWrapper.java:86)
	at org.apache.maven.surefire.junitcore.JUnitCoreProvider.invoke(JUnitCoreProvider.java:134)
	at org.apache.maven.surefire.booter.ForkedBooter.invokeProviderInSameClassLoader(ForkedBooter.java:200)
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:153)
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:103)
org.junit.ComparisonFailure: expected:<"[result]"> but was:<"[通过]">
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at com.jd.bdp.datadev.enums.ScriptPublishCheckEnumTest.testToDesc(ScriptPublishCheckEnumTest.java:23)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:47)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:44)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:271)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:70)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:50)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runners.Suite.runChild(Suite.java:127)
	at org.junit.runners.Suite.runChild(Suite.java:26)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:160)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:138)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.createRequestAndRun(JUnitCoreWrapper.java:141)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.executeEager(JUnitCoreWrapper.java:114)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.execute(JUnitCoreWrapper.java:86)
	at org.apache.maven.surefire.junitcore.JUnitCoreProvider.invoke(JUnitCoreProvider.java:134)
	at org.apache.maven.surefire.booter.ForkedBooter.invokeProviderInSameClassLoader(ForkedBooter.java:200)
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:153)
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:103)
org.junit.ComparisonFailure: expected:<[0]> but was:<[1]>
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at com.jd.bdp.datadev.enums.ScriptPublishCheckEnumTest.testTocode(ScriptPublishCheckEnumTest.java:12)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:47)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:44)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:271)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:70)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:50)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runners.Suite.runChild(Suite.java:127)
	at org.junit.runners.Suite.runChild(Suite.java:26)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:160)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:138)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.createRequestAndRun(JUnitCoreWrapper.java:141)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.executeEager(JUnitCoreWrapper.java:114)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.execute(JUnitCoreWrapper.java:86)
	at org.apache.maven.surefire.junitcore.JUnitCoreProvider.invoke(JUnitCoreProvider.java:134)
	at org.apache.maven.surefire.booter.ForkedBooter.invokeProviderInSameClassLoader(ForkedBooter.java:200)
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:153)
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:103)
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.076 sec - in com.jd.bdp.datadev.enums.ScriptPublishCheckEnumTest
Running com.jd.bdp.datadev.enums.DataDevFileUpTargetTypeEnumTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.DataDevFileUpTargetTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptNewFileTypeEnumTest
Tests run: 19, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.enums.DataDevScriptNewFileTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevGitReviewStatusEnumTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.DataDevGitReviewStatusEnumTest
Running com.jd.bdp.datadev.enums.ScriptCheckTypeEnumTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.ScriptCheckTypeEnumTest
Running com.jd.bdp.datadev.enums.ScriptCheckOpTypeEnumTest
Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.enums.ScriptCheckOpTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptGitStatusEnumTest
java.lang.NullPointerException
	at com.jd.bdp.datadev.enums.DataDevScriptGitStatusEnum.getGitStatus(DataDevScriptGitStatusEnum.java:23)
	at com.jd.bdp.datadev.enums.DataDevScriptGitStatusEnumTest.testGetGitStatusException(DataDevScriptGitStatusEnumTest.java:117)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:47)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:44)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.mockito.internal.runners.DefaultInternalRunner$1$1.evaluate(DefaultInternalRunner.java:44)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:271)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:70)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:50)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.mockito.internal.runners.DefaultInternalRunner$1.run(DefaultInternalRunner.java:74)
	at org.mockito.internal.runners.DefaultInternalRunner.run(DefaultInternalRunner.java:80)
	at org.mockito.internal.runners.StrictRunner.run(StrictRunner.java:39)
	at org.mockito.junit.MockitoJUnitRunner.run(MockitoJUnitRunner.java:163)
	at org.junit.runners.Suite.runChild(Suite.java:127)
	at org.junit.runners.Suite.runChild(Suite.java:26)
	at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
	at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:160)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:138)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.createRequestAndRun(JUnitCoreWrapper.java:141)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.executeEager(JUnitCoreWrapper.java:114)
	at org.apache.maven.surefire.junitcore.JUnitCoreWrapper.execute(JUnitCoreWrapper.java:86)
	at org.apache.maven.surefire.junitcore.JUnitCoreProvider.invoke(JUnitCoreProvider.java:134)
	at org.apache.maven.surefire.booter.ForkedBooter.invokeProviderInSameClassLoader(ForkedBooter.java:200)
	at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:153)
	at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:103)
Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.enums.DataDevScriptGitStatusEnumTest
Running com.jd.bdp.datadev.enums.XingYunStatusEnumTest
Tests run: 30, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.enums.XingYunStatusEnumTest
Running com.jd.bdp.datadev.enums.DataDevProjectTypeEnumTest
Tests run: 21, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.enums.DataDevProjectTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptFileWhereIsNewEnumTest
Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.DataDevScriptFileWhereIsNewEnumTest
Running com.jd.bdp.datadev.enums.DataDevOperateLogEnumTest
Tests run: 36, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.enums.DataDevOperateLogEnumTest
Running com.jd.bdp.datadev.enums.DataDevOpenScriptTypeEnumTest
Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.enums.DataDevOpenScriptTypeEnumTest
Running com.jd.bdp.datadev.enums.BeeSourceEnumTest
Tests run: 29, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.enums.BeeSourceEnumTest
Running com.jd.bdp.datadev.enums.DataDevGitAccessLevelEnumTest
Tests run: 16, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.enums.DataDevGitAccessLevelEnumTest
Running com.jd.bdp.datadev.enums.DataDevHisTypeEnumTest
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.enums.DataDevHisTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptPublishStatusEnumTest
Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.enums.DataDevScriptPublishStatusEnumTest
Running com.jd.bdp.datadev.enums.DataDevFileUpStatusEnumTest
Tests run: 16, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.enums.DataDevFileUpStatusEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptRunDetailTypeEnumTest
Tests run: 19, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.enums.DataDevScriptRunDetailTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptSaveTypeEnumTest
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.DataDevScriptSaveTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptTargetTypeEnumTest
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.enums.DataDevScriptTargetTypeEnumTest
Running com.jd.bdp.datadev.enums.DataDevResponseCodeEnumTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.enums.DataDevResponseCodeEnumTest
Running com.jd.bdp.datadev.enums.RightRoleEnumTest
Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.enums.RightRoleEnumTest
Running com.jd.bdp.datadev.enums.DataDevRunTypeEnumTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.enums.DataDevRunTypeEnumTest
Running com.jd.bdp.datadev.enums.TableRightEnumTest
Tests run: 17, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.enums.TableRightEnumTest
Running com.jd.bdp.datadev.enums.DataDevScriptRunStatusEnumTest
Tests run: 29, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 sec - in com.jd.bdp.datadev.enums.DataDevScriptRunStatusEnumTest
Running com.jd.bdp.datadev.enums.ScriptCheckStatusEnumTest
Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.enums.ScriptCheckStatusEnumTest
Running com.jd.bdp.datadev.bo.UgdapAccountResultTest
Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.UgdapAccountResultTest
Running com.jd.bdp.datadev.bo.ImageInfoBoTest
---{"code":"code","created":1745491661948,"creator":"bjlvyanmeng","description":"desc","id":100,"imageStatus":"0","isDefault":0,"managers":"bjlvyanmeng","modified":1745491661948,"modifier":"bjlvyanmeng"}Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.033 sec - in com.jd.bdp.datadev.bo.ImageInfoBoTest
Running com.jd.bdp.datadev.bo.MetaDataFiledInfoBoTest
Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.MetaDataFiledInfoBoTest
Running com.jd.bdp.datadev.bo.ProjectInfoBoTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.bo.ProjectInfoBoTest
Running com.jd.bdp.datadev.bo.BuffaloScriptInfoBoTest
Tests run: 17, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.BuffaloScriptInfoBoTest
Running com.jd.bdp.datadev.bo.ScriptTaskProjectInfoBoTest
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.ScriptTaskProjectInfoBoTest
Running com.jd.bdp.datadev.bo.AnalysisTableInfoBoTest
Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.AnalysisTableInfoBoTest
Running com.jd.bdp.datadev.bo.MetadataFieldResultTest
Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.MetadataFieldResultTest
Running com.jd.bdp.datadev.bo.UgdapTableInfoTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.bo.UgdapTableInfoTest
Running com.jd.bdp.datadev.bo.TableSelectBoTest
Tests run: 29, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.bo.TableSelectBoTest
Running com.jd.bdp.datadev.bo.UgdapTableRightBoTest
Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.UgdapTableRightBoTest
Running com.jd.bdp.datadev.bo.UgdapErpTableRightQueueBoTest
Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.UgdapErpTableRightQueueBoTest
Running com.jd.bdp.datadev.bo.UgdapTableResultTest
Tests run: 19, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.UgdapTableResultTest
Running com.jd.bdp.datadev.bo.UgdapDatabaseResultTest
Tests run: 16, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.bo.UgdapDatabaseResultTest
Running com.jd.bdp.datadev.bo.UgdapErpTableRightAccountBoTest
Tests run: 20, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.bo.UgdapErpTableRightAccountBoTest
Running com.jd.bdp.datadev.bo.MetaPartitionDataInfoBoTest
Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.bo.MetaPartitionDataInfoBoTest
Running com.jd.bdp.datadev.domain.DataDevDataImportTest
Tests run: 22, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.domain.DataDevDataImportTest
Running com.jd.bdp.datadev.domain.DataDevCodingFileTest
Tests run: 23, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.domain.DataDevCodingFileTest
Running com.jd.bdp.datadev.domain.DataDevGitNameSpaceTest
Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.DataDevGitNameSpaceTest
Running com.jd.bdp.datadev.domain.Buffalo5QueryTest
Tests run: 24, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.Buffalo5QueryTest
Running com.jd.bdp.datadev.domain.DataDevScriptUpLoadTest
Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.DataDevScriptUpLoadTest
Running com.jd.bdp.datadev.domain.DataDevScriptBuffaloJobTest
Tests run: 50, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.01 sec - in com.jd.bdp.datadev.domain.DataDevScriptBuffaloJobTest
Running com.jd.bdp.datadev.domain.DataDevFileUpLoadDetailTest
Tests run: 73, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.017 sec - in com.jd.bdp.datadev.domain.DataDevFileUpLoadDetailTest
Running com.jd.bdp.datadev.domain.DataDevPlumberArgsTest
Tests run: 48, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 sec - in com.jd.bdp.datadev.domain.DataDevPlumberArgsTest
Running com.jd.bdp.datadev.domain.DataDevFunMemberTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.domain.DataDevFunMemberTest
Running com.jd.bdp.datadev.domain.context.SubmitScriptCheckContextTest
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.012 sec - in com.jd.bdp.datadev.domain.context.SubmitScriptCheckContextTest
Running com.jd.bdp.datadev.domain.DataDevFunSharedGroupTest
Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.domain.DataDevFunSharedGroupTest
Running com.jd.bdp.datadev.domain.Buffalo5PublishTaskRecordQueryTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.Buffalo5PublishTaskRecordQueryTest
Running com.jd.bdp.datadev.domain.DataDevFunCompileSetTest
Tests run: 23, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.DataDevFunCompileSetTest
Running com.jd.bdp.datadev.domain.DataDevFunVersionTest
Tests run: 54, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 sec - in com.jd.bdp.datadev.domain.DataDevFunVersionTest
Running com.jd.bdp.datadev.domain.DataDevGitHisDetailTest
Tests run: 38, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 sec - in com.jd.bdp.datadev.domain.DataDevGitHisDetailTest
Running com.jd.bdp.datadev.domain.DataDevScriptFilePublishTest
Tests run: 76, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 sec - in com.jd.bdp.datadev.domain.DataDevScriptFilePublishTest
Running com.jd.bdp.datadev.domain.JDQFlowInfoTest
Tests run: 21, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.JDQFlowInfoTest
Running com.jd.bdp.datadev.domain.Buffalo5PublishRecordQueryTest
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.Buffalo5PublishRecordQueryTest
Running com.jd.bdp.datadev.domain.Buffalo5ScriptCheckQueryTest
Tests run: 9, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.domain.Buffalo5ScriptCheckQueryTest
Running com.jd.bdp.datadev.domain.xingyun.SpaceResponseTest
Tests run: 16, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.domain.xingyun.SpaceResponseTest
Running com.jd.bdp.datadev.domain.xingyun.CardResponseTest
Tests run: 27, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 sec - in com.jd.bdp.datadev.domain.xingyun.CardResponseTest
Running com.jd.bdp.datadev.domain.DataDevDependencyTest
Tests run: 18, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.DataDevDependencyTest
Running com.jd.bdp.datadev.domain.DataDevDependencyDetailTest
Tests run: 30, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 sec - in com.jd.bdp.datadev.domain.DataDevDependencyDetailTest
Running com.jd.bdp.datadev.domain.DataDevApplicationTest
Tests run: 68, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 sec - in com.jd.bdp.datadev.domain.DataDevApplicationTest
Running com.jd.bdp.datadev.domain.DataDevClientBaseTest
Tests run: 35, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 sec - in com.jd.bdp.datadev.domain.DataDevClientBaseTest
Running com.jd.bdp.datadev.domain.DataDevScriptCodeSnippetTest
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.DataDevScriptCodeSnippetTest
Running com.jd.bdp.datadev.domain.diff.DiffPairVoTest
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.domain.diff.DiffPairVoTest
Running com.jd.bdp.datadev.domain.diff.DiffInfoVoTest
Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.diff.DiffInfoVoTest
Running com.jd.bdp.datadev.domain.diff.ReleaseCompareVoTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.diff.ReleaseCompareVoTest
Running com.jd.bdp.datadev.domain.FileInfoTest
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.domain.FileInfoTest
Running com.jd.bdp.datadev.domain.DataDevFunDirTest
Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.domain.DataDevFunDirTest
Running com.jd.bdp.datadev.domain.DataDevFunLocationTest
Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.domain.DataDevFunLocationTest
Running com.jd.bdp.datadev.domain.UgdapTableInfoTest
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.domain.UgdapTableInfoTest
Running com.jd.bdp.datadev.domain.DataDevGitProjectMemberTest
Tests run: 49, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 sec - in com.jd.bdp.datadev.domain.DataDevGitProjectMemberTest
Running com.jd.bdp.datadev.domain.AgentFileTest
Tests run: 24, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 sec - in com.jd.bdp.datadev.domain.AgentFileTest
Running com.jd.bdp.datadev.domain.DataDevScriptFileHisTest
Tests run: 187, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.046 sec - in com.jd.bdp.datadev.domain.DataDevScriptFileHisTest
Running com.jd.bdp.datadev.domain.DataDevGitHisTest
Tests run: 31, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 sec - in com.jd.bdp.datadev.domain.DataDevGitHisTest
Running com.jd.bdp.datadev.domain.DataDevGitProjectTest
Tests run: 99, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.034 sec - in com.jd.bdp.datadev.domain.DataDevGitProjectTest
Running com.jd.bdp.datadev.domain.DataDevFunDetailHisTest
Tests run: 45, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.013 sec - in com.jd.bdp.datadev.domain.DataDevFunDetailHisTest
Running com.jd.bdp.datadev.domain.DataDevScriptTemplateShowTest
Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.DataDevScriptTemplateShowTest
Running com.jd.bdp.datadev.domain.DataDevGitProjectBranchTest
Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.DataDevGitProjectBranchTest
Running com.jd.bdp.datadev.domain.DataDevScriptTemplateTest
Tests run: 62, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.025 sec - in com.jd.bdp.datadev.domain.DataDevScriptTemplateTest
Running com.jd.bdp.datadev.domain.DataDevGitGroupMemberTest
Tests run: 26, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 sec - in com.jd.bdp.datadev.domain.DataDevGitGroupMemberTest
Running com.jd.bdp.datadev.domain.sandbox.ShouldSqlRunInSandboxResponse2Test
Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.sandbox.ShouldSqlRunInSandboxResponse2Test
Running com.jd.bdp.datadev.domain.sandbox.SqlCheckInfoTest
Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.domain.sandbox.SqlCheckInfoTest
Running com.jd.bdp.datadev.domain.sandbox.SandboxSiteInfoRequestTest
Tests run: 16, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 sec - in com.jd.bdp.datadev.domain.sandbox.SandboxSiteInfoRequestTest
Running com.jd.bdp.datadev.domain.sandbox.ShouldSqlRunInSandboxRequestTest
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.sandbox.ShouldSqlRunInSandboxRequestTest
Running com.jd.bdp.datadev.domain.sandbox.SqlCheckResponseTest
Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.sandbox.SqlCheckResponseTest
Running com.jd.bdp.datadev.domain.sandbox.SandboxSiteInfoResponseTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.sandbox.SandboxSiteInfoResponseTest
Running com.jd.bdp.datadev.domain.sandbox.ShouldSqlRunInSandboxResponseTest
Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.sandbox.ShouldSqlRunInSandboxResponseTest
Running com.jd.bdp.datadev.domain.table.TableCheckParamTest
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.table.TableCheckParamTest
Running com.jd.bdp.datadev.domain.table.TableCheckDownInfoTest
Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.domain.table.TableCheckDownInfoTest
Running com.jd.bdp.datadev.domain.UploadFileVoTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.datadev.domain.UploadFileVoTest
Running com.jd.bdp.datadev.domain.DataDevScriptTemplateShareTest
Tests run: 22, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 sec - in com.jd.bdp.datadev.domain.DataDevScriptTemplateShareTest
Running com.jd.bdp.datadev.domain.DataDevScriptFileTest
Tests run: 75, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.024 sec - in com.jd.bdp.datadev.domain.DataDevScriptFileTest
Running com.jd.bdp.datadev.domain.Buffalo5PublishInfoTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.014 sec - in com.jd.bdp.datadev.domain.Buffalo5PublishInfoTest
Running com.jd.bdp.datadev.domain.Buffalo5AnalysisScriptTest
Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 sec - in com.jd.bdp.datadev.domain.Buffalo5AnalysisScriptTest
Running com.jd.bdp.datadev.domain.Buffalo5CheckTablePermQueryTest
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.domain.Buffalo5CheckTablePermQueryTest
Running com.jd.bdp.datadev.domain.DoubleLinkedListTest
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0 sec - in com.jd.bdp.datadev.domain.DoubleLinkedListTest
Running com.jd.bdp.datadev.domain.task.ScriptTaskRelationTest
Tests run: 22, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 sec - in com.jd.bdp.datadev.domain.task.ScriptTaskRelationTest
Running com.jd.bdp.datadev.domain.DataDevOperateLogTest
Tests run: 24, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 sec - in com.jd.bdp.datadev.domain.DataDevOperateLogTest
Running com.jd.bdp.datadev.domain.DataDevGitProjectMergeTest
Tests run: 45, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.01 sec - in com.jd.bdp.datadev.domain.DataDevGitProjectMergeTest
Running com.jd.bdp.datadev.domain.AgentFileRootDirTest
Tests run: 15, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.domain.AgentFileRootDirTest
Running com.jd.bdp.datadev.domain.DataDevTermnialTest
Tests run: 81, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.023 sec - in com.jd.bdp.datadev.domain.DataDevTermnialTest
Running com.jd.bdp.datadev.domain.DataDevFunUseHistoryTest
Tests run: 42, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.011 sec - in com.jd.bdp.datadev.domain.DataDevFunUseHistoryTest
Running com.jd.bdp.datadev.domain.DataDownloadLogTest
Tests run: 25, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.006 sec - in com.jd.bdp.datadev.domain.DataDownloadLogTest
Running com.jd.bdp.datadev.domain.DataDevScriptDirTest
Tests run: 41, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 sec - in com.jd.bdp.datadev.domain.DataDevScriptDirTest
Running com.jd.bdp.datadev.domain.Buffalo5AnalysisScriptQueryTest
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.Buffalo5AnalysisScriptQueryTest
Running com.jd.bdp.datadev.domain.part.InstancePartIndexTest
Tests run: 11, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.004 sec - in com.jd.bdp.datadev.domain.part.InstancePartIndexTest
Running com.jd.bdp.datadev.domain.Buffalo5ScriptCheckTest
{"message":"111","messageCode":"code","name":"name","operate":"aaaa","scriptId":1,"status":"status"}
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.005 sec - in com.jd.bdp.datadev.domain.Buffalo5ScriptCheckTest
Running com.jd.bdp.datadev.domain.DataDevFunDetailTest
Tests run: 108, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.03 sec - in com.jd.bdp.datadev.domain.DataDevFunDetailTest
Running com.jd.bdp.datadev.domain.DataDevGitProjectSharedGroupTest
Tests run: 24, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 sec - in com.jd.bdp.datadev.domain.DataDevGitProjectSharedGroupTest
Running com.jd.bdp.datadev.domain.DataDevScriptConfigTest
Tests run: 79, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.024 sec - in com.jd.bdp.datadev.domain.DataDevScriptConfigTest
Running com.jd.bdp.datadev.domain.DataDevUIUserInfoTest
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.datadev.domain.DataDevUIUserInfoTest
Running com.jd.bdp.datadev.domain.data.TableSelectLogTest
Tests run: 29, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 sec - in com.jd.bdp.datadev.domain.data.TableSelectLogTest
Running com.jd.bdp.datadev.domain.ZtreeNodeTest
[{"chkDisabled":false,"dir":true,"gitProjectId":900033603,"master":false,"name":"test","parChl":0,"parentPath":"","path":"test","tableLevel":0,"targetDir":false,"type":-1},{"chkDisabled":false,"deleted":0,"dir":false,"gitProjectId":900033603,"id":1000007403,"lastModified":"2024-07-24 18:17:32","lastVersion":"200009","master":false,"modifier":"吕延猛(bjlvyanmeng)","name":"test2.sh","parChl":1,"parentPath":"test","path":"test/test2.sh","tableLevel":1,"targetDir":false,"type":2,"version":"200009"},{"chkDisabled":false,"deleted":0,"dir":false,"gitProjectId":900033603,"id":1000007947,"lastModified":"2024-07-25 10:03:50","lastVersion":"200002","master":false,"modifier":"吕延猛(bjlvyanmeng)","name":"test3333.sh","parChl":1,"parentPath":"test","path":"test/test3333.sh","tableLevel":1,"targetDir":false,"type":2,"version":"200002"},{"chkDisabled":false,"deleted":0,"dir":false,"gitProjectId":900033603,"id":1000007465,"lastModified":"2024-08-21 13:50:05","lastVersion":"200008","master":false,"modifier":"吕延猛(bjlvyanmeng)","name":"test3.sh","parChl":1,"parentPath":"","path":"test3.sh","tableLevel":0,"targetDir":false,"type":2,"version":"200008"},{"chkDisabled":false,"createSql":"add jar test_global_2.jar; CREATE TEMPORARY FUNCTION test_global_2 AS 'com.jd.udf.test.squareInt';","deleted":0,"dir":false,"format":"[\"test_global_2(int a)\"]","funId":1360,"funType":2,"id":1360,"lastModified":"2024-08-21 07:00:56","lastVersion":"1001","master":false,"modifier":"王晓丽(wangxiaoli76)","name":"test_global_2","owners":[{"funId":1360,"funMemberCode":"wangxiaoli76","funMemberName":"王晓丽","id":7460,"type":1},{"funId":1360,"funMemberCode":"bjlvyanmeng","funMemberName":"吕延猛","id":7461,"type":1},{"funId":1360,"funMemberCode":"zhangrui156","funMemberName":"张睿","id":7462,"type":1},{"funId":1360,"funMemberCode":"chenyuhan4","funMemberName":"陈宇涵","id":7463,"type":1}],"parChl":1,"parentPath":"","path":"test_global_2.jar","tableLevel":0,"targetDir":false,"version":"1001"}]
Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.033 sec - in com.jd.bdp.datadev.domain.ZtreeNodeTest
Running com.jd.bdp.datadev.domain.ScriptFileExtTest
Tests run: 32, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 sec - in com.jd.bdp.datadev.domain.ScriptFileExtTest
Running com.jd.bdp.datadev.domain.DataDevGitDtoTest
Tests run: 34, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.009 sec - in com.jd.bdp.datadev.domain.DataDevGitDtoTest
Running com.jd.bdp.datadev.domain.DataDevGitGroupTest
Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.datadev.domain.DataDevGitGroupTest
Running com.jd.bdp.idenew.domain.DataIdeSqlInfoTest
Tests run: 44, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.015 sec - in com.jd.bdp.idenew.domain.DataIdeSqlInfoTest
Running com.jd.bdp.idenew.domain.DataIdeUploadFileParamTest
Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.idenew.domain.DataIdeUploadFileParamTest
Running com.jd.bdp.idenew.domain.DataIdeSqlOperationLogTest
Tests run: 127, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.035 sec - in com.jd.bdp.idenew.domain.DataIdeSqlOperationLogTest
Running com.jd.bdp.idenew.domain.DataIdeShareDataParamTest
Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.002 sec - in com.jd.bdp.idenew.domain.DataIdeShareDataParamTest
Running com.jd.bdp.idenew.domain.DataIdeSqlInfoDirTest
Tests run: 27, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.007 sec - in com.jd.bdp.idenew.domain.DataIdeSqlInfoDirTest
Running com.jd.bdp.idenew.domain.DataIdeSqlOperationLogOnlineParamTest
Tests run: 12, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.idenew.domain.DataIdeSqlOperationLogOnlineParamTest
Running com.jd.bdp.domain.ide_access.SqlInfoTest
Tests run: 37, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.008 sec - in com.jd.bdp.domain.ide_access.SqlInfoTest
Running com.jd.bdp.domain.ide_access.FieldFilterTest
Tests run: 6, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.001 sec - in com.jd.bdp.domain.ide_access.FieldFilterTest
Running com.jd.bdp.dorisIde.domain.ScriptRunTableRltTest
Tests run: 14, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.003 sec - in com.jd.bdp.dorisIde.domain.ScriptRunTableRltTest

Results :

Tests run: 4065, Failures: 0, Errors: 0, Skipped: 0
"""
    print(extract_important_maven_output(test_content))