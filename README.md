# README

**Repository:** `[repository-name]`  
**Description:** `node-lib provides useful helper libraries for building Adaptors, Mappers and Projectors for the Integration Architecture Node Platform.`  
**Repository Status:** `Private – NDTP InnerSource`  

---

## Overview

This repository is part of the **National Digital Twin Programme (NDTP)**. It supports the development of secure, modular, and standards-based components for internal use across NDTP projects.

> **This repository is private and governed by the NDTP InnerSource Licence – Version 1.0.**  
> It is intended solely for collaboration among NDTP teams and authorised suppliers.  
> It is **not open source** and must not be disclosed, redistributed, or published externally.

--- 

## Dependencies

- Python \>=3.10
- Kafka*

node-lib uses `confluent-kafka` to manage connections to Kafka. 
Please see [confluent-kafka's compatability documentation](https://docs.confluent.io/platform/current/installation/versions-interoperability.html) to ensure you have a compatible Kafka instance.


## Installation

```shell
pip install node-lib
```

## Usage

For documentation on how to use node-lib, please see the [documentation index](https://github.com/National-Digital-Twin/node-lib/blob/main/docs/index.md).

## Public Funding Acknowledgment  
This repository has been developed with public funding as part of the National Digital Twin Programme (NDTP), a UK Government initiative. NDTP, alongside its partners, has invested in this work to advance open, secure, and reusable digital twin technologies for any organisation, whether from the public or private sector, irrespective of size.  

## Licensing

This repository, including all source code, documentation, configuration files, and related materials, is licensed under the:

**NDTP InnerSource Licence – Version 1.0**  
See [LICENSE.md](LICENSE.md) for the full licence text.

> ⚠️ This repository is **not open source**.  
> Redistribution, disclosure, or publication of any part of this repository is prohibited without the **explicit, written approval** of the NDTP Management Team.

All intellectual property rights are held by the **Department for Business and Trade (UK)** as the governing entity for the National Digital Twin Programme (NDTP).

## Security and Responsible Disclosure  
We take security seriously. If you believe you have found a security vulnerability in this repository, please follow our responsible disclosure process outlined in `SECURITY.md`.  

## Software Bill of Materials (SBOM)

This project provides a Software Bill of Materials (SBOM) to help users and integrators understand its dependencies.

### Current SBOM
Download the [latest SBOM for this codebase](../../dependency-graph/sbom) to view the current list of components used in this repository.

## Contributing  
We welcome contributions that align with the Programme’s objectives. Please read our `CONTRIBUTING.md` guidelines before submitting pull requests.  

## Acknowledgements  
This repository has benefited from collaboration with various organisations. For a list of acknowledgments, see `ACKNOWLEDGEMENTS.md`.  

## Support and Contact  
For questions or support, check our Issues or contact the NDTP team on ndtp@businessandtrade.gov.uk.

**Maintained by the National Digital Twin Programme (NDTP).**  

© Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.