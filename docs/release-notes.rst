.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


VF-C Release Notes
==================

VF-C includes two main components, NFV-O and GVNFM, to implement life cycle
management and FCAPS of VNF and NS. VF-C takes part in end to end service
orchestration and close loop automation by working with SO, DCAE and Policy.
VF-C also provides standard southbound interface to VNFMs and can integrate
with multi vendor VNFMs via drivers.

Version: 1.2.0
--------------

:Release Date: 2018-11-30

**New Features**

- NS Orchestration supports PNF:1.NSLCM supports NSD, composed of VNF, PNF, and VL;2.Catalog supports PNFD and updates NSD DM
- Hardware Platform Awareness (HPA) Support:1.integrate with OOF;2.VF-C can parse R2+ TOSCA MODEL which includes HPA feature
- Standard Alignment:SOL003 Alignment in GVNFM and Catalog
- Standalone DB Microservice

Released components:

NFVO
 - vfc-nfvo-lcm 1.2.2
 - vfc-nfvo-catalog 1.2.2
 - vfc-nfvo-resmgr 1.2.1
 - vfc-nfvo-driver-emsdriver 1.2.1
 - vfc-nfvo-driver-gvnfm-gvnfmadapter 1.2.2
 - vfc-nfvo-driver-gvnfm-jujudriver 1.2.1
 - vfc-nfvo-driver-svnfm-ztedriver 1.2.1
 - vfc-nfvo-driver-svnfm-huaweidriver 1.2.1
 - vfc-nfvo-driver-svnfm-nokiav2driver 1.2.1
 - vfc-nfvo-driver-sfc-ztesfcdriver 1.2.0
 - vfc-nfvo-multivimproxy 1.2.1
 - vfc-nfvo-db 1.2.2
GVNFM
 - vfc-gvnfm-vnflcm 1.2.2
 - vfc-gvnfm-vnfmgr 1.2.1
 - vfc-gvnfm-vnfres 1.2.1
Workflow
 - workflow-engine-mgr-service
 - activiti-extension

**Bug Fixes**

**Known Issues**

 - `VFC-896 <https://jira.onap.org/browse/VFC-896>`_  vim-id in AAI is handled as a mandatory parameter
 - `VFC-890 <https://jira.onap.org/browse/VFC-890>`_  The hard coded SDC user and password in catalog & LCM is not present in SDC
 - `VFC-891 <https://jira.onap.org/browse/VFC-891>`_  The AAI credentials is hard coded in LCM
 - SDC-1897 - Parser exported CSAR with error OPEN (Will be fixed at Dublin),VFC could ignore that error. To ignore that error, we need either apply the patch at https://jira.opnfv.org/browse/PARSER-187 locally in nfv-toscaparser which VFC uses or wait for nfv-toscaparser got that fixed.

**Security Notes**

VFC code has been formally scanned during build time using NexusIQ and all Critical
vulnerabilities have been addressed, items that remain open have been assessed
for risk and determined to be false positive. The VFC open Critical security
vulnerabilities and their risk assessment have been documented as part
of the `project <https://wiki.onap.org/pages/viewpage.action?pageId=45298878>`_.

Quick Links:

- `VFC project page <https://wiki.onap.org/display/DW/Virtual+Function+Controller+Project>`_
- `Passing Badge information for VFC <https://bestpractices.coreinfrastructure.org/en/projects/1608>`_
- `Project Vulnerability Review Table for VFC <https://wiki.onap.org/pages/viewpage.action?pageId=45298878>`_

**Upgrade Notes**
	NA

**Deprecation Notes**
	NA

**Other**
	NA

Version: 1.1.0
--------------

:Release Date: 2018-06-07

**New Features**

- NS/VNF manual scaling supporting for VoLTE use case
- VNF Integration, integration with VNF via GVNFM
- S3P improvement

Released components:

NFVO
 - vfc-nfvo-lcm
 - vfc-nfvo-catalog
 - vfc-nfvo-resmgr
 - vfc-nfvo-driver-emsdriver
 - vfc-nfvo-driver-gvnfm-gvnfmadapter
 - vfc-nfvo-driver-gvnfm-jujudriver
 - vfc-nfvo-driver-svnfm-ztedriver
 - vfc-nfvo-driver-svnfm-huaweidriver
 - vfc-nfvo-driver-svnfm-nokiadriver
 - vfc-nfvo-driver-svnfm-nokiav2driver
 - vfc-nfvo-driver-sfc-ztesfcdriver
 - vfc-nfvo-multivimproxy
GVNFM
 - vfc-gvnfm-vnflcm
 - vfc-gvnfm-vnfmgr
 - vfc-gvnfm-vnfres
Workflow
 - workflow-engine-mgr-service
 - activiti-extension

**Bug Fixes**

This is the initial release

**Known Issues**

 - `VFC-896 <https://jira.onap.org/browse/VFC-896>`_  vim-id in AAI is handled as a mandatory parameter
 - `VFC-890 <https://jira.onap.org/browse/VFC-890>`_  The hard coded SDC user and password in catalog & LCM is not present in SDC
 - `VFC-891 <https://jira.onap.org/browse/VFC-891>`_  The AAI credentials is hard coded in LCM

**Security Notes**

VFC code has been formally scanned during build time using NexusIQ and all Critical
vulnerabilities have been addressed, items that remain open have been assessed
for risk and determined to be false positive. The VFC open Critical security
vulnerabilities and their risk assessment have been documented as part
of the `project <https://wiki.onap.org/pages/viewpage.action?pageId=25437810>`_.

Quick Links:

- `VFC project page <https://wiki.onap.org/display/DW/Virtual+Function+Controller+Project>`_
- `Passing Badge information for VFC <https://bestpractices.coreinfrastructure.org/en/projects/1608>`_
- `Project Vulnerability Review Table for VFC <https://wiki.onap.org/pages/viewpage.action?pageId=25437810>`_

**Upgrade Notes**
	NA

**Deprecation Notes**
	NA

**Other**
	NA

Version: 1.0.0
--------------

:Release Date: 2017-11-16

**New Features**

- NS lifecycle management, including NS instance creation, termination and healing
- VNF lifecycle management, including VNF instance creation, termination and healing
- VNF FCAPS, collecting FCAPS data from vendor EMS
- VNFM Integration, integration with specific VNFMs of vendors to deploy commercial VNFs
- VNF Integration, integration with VNF via GVNFM

Released components:

NFVO
 - vfc-nfvo-lcm
 - vfc-nfvo-catalog
 - vfc-nfvo-resmgr
 - vfc-nfvo-driver-emsdriver
 - vfc-nfvo-driver-gvnfm-gvnfmadapter
 - vfc-nfvo-driver-gvnfm-jujudriver
 - vfc-nfvo-driver-svnfm-ztedriver
 - vfc-nfvo-driver-svnfm-huaweidriver
 - vfc-nfvo-driver-svnfm-nokiadriver
 - vfc-nfvo-driver-sfc-ztesfcdriver
GVNFM
 - vfc-gvnfm-vnflcm
 - vfc-gvnfm-vnfmgr
 - vfc-gvnfm-vnfres
Workflow
 - workflow-engine-mgr-service
 - activiti-extension

**Bug Fixes**

This is the initial release

**Known Issues**

None

**Security Issues**

None

**Upgrade Notes**

This is the initial release

**Deprecation Notes**

This is the initial release

**Other**
	NA

===========

End of Release Notes