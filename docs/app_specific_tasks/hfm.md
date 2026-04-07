# Hyperion HFM

This section is needed only if you have an On Premise Oracle HFM application where
EPMWARE agent is installed.

**Copy `“reg.properties”` file to EPM Instance folder.**

We need to copy the `"reg.properties"` file from the location as mentioned below.
(If the Oracle is installed on another drive such as D or E, please use that drive instead).


- Log on to the HFM Application server. In this example we will assume it is a Windows server and Oracle is installed on the D drive.  
- Copy `“reg.properties”` file from `<MIDDLEWARE>\user_projects\config\foundation\11.1.2.0` to the `<MIDDLEWARE>\user_projects\epmsystem1\config\foundation\11.1.2.0` folder.  
- For example, copy  `D:\Oracle\Middleware\user_projects\config\foundation\11.1.2.0\reg.properties`  
  to  `D:\Oracle\Middleware\user_projects\epmsystem1\config\foundation\11.1.2.0` folder.

