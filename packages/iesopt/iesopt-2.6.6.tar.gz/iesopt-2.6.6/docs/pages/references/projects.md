# Projects

## Overview

This maintains a list of projects where IESopt was applied as part of the modeling
approach. Entries are in alphabetical order. If you want to contribute a new project, please follow the
instructions in the [section on contributing](#contributing) below.

## List of references

(references-projects-deriskdh)=
### DeRiskDH

:**title**: DeRiskDH
:**homepage**: [ait.ac.at](https://www.ait.ac.at/themen/integratedenergysystems/projekte/deriskdh)
:**funding**: [ffg.at](https://www.ffg.at/vorzeigeregionenergie)
:**description**: Risk minimization for decarbonizing heating networks via network temperature reductions and flexibility utilization
:**AIT contact**: R. Schmidt

---

(references-projects-ENABLE-DHC)=
### ENABLE-DHC

:**title**: ENABLE-DHC
:**homepage**: [ait.ac.at](https://www.ait.ac.at/themen/flexibilitaet-geschaeftsmodelle/projekte/dekarbonisierungsstrategien-fuer-die-fernwaerme)
:**funding**: [ec.euopa.eu](https://webgate.ec.europa.eu/life/publicWebsite/project/LIFE23-CET-ENABLE-DHC-101167576/enabling-strategies-and-investment-plans-for-efficient-multi-energy-and-digitalized-dhc)
:**description**: ENABLE DHC aims to foster the switch of district heating and cooling (DHC) networks towards efficient DHC as defined in the Energy Efficiency Directive, by developing 9 case studies of investment plans in 7 European countries.
:**AIT contact**: R. Schmidt

---

(references-projects-heathighway)=
### Heat Highway

:**title**: Heat Highway
:**homepage**: [ait.ac.at](https://www.ait.ac.at/themen/integratedenergysystems/projekte/heat-highway)
:**funding**: [ffg.at](https://projekte.ffg.at/projekt/3851881)
:**description**: The HeatHighway project investigates supra-regional heat transmission networks, focusing on the use of multiple waste heat sources.
:**AIT contact**: R. Schmidt

---

(references-projects-heatminedh)=
### HeatMineDH

:**title**: Low-Grade Renewable and Waste Heat Mapping and Investment Planning for Efficient District Heating
:**homepage**: [ait.ac.at](https://www.ait.ac.at/themen/integratedenergysystems/projekte/heatminedh)
:**funding**: [cinea.ec.europa.eu](https://cinea.ec.europa.eu/programmes/life_en?prefLang=de)
:**description**: HeatMineDH aims to develop business cases and investment plans for the incorporation of low-grade heat sources into high temperature district heating networks.
:**AIT contact**: R. Schmidt

---

(references-projects-hytechonomy)=
### HyTechonomy

:**title**: Hydrogen Technologies for Sustainable Economies
:**homepage**: [hytechonomy.com](https://www.hytechonomy.com/)
:**funding**: [ffg.at](https://projekte.ffg.at/projekt/3915332)
:**description**: The overall scientific vision of the COMET-Project HyTechonomy is to provide the technological and strategic know-how basis for the substitution of the fossil energy carriers by renewable hydrogen.
:**AIT contact**: S. Reuter

---

(references-projects-knowing)=
### KNOWING

:**title**: KNOWING
:**homepage**: [knowing-climate.eu](https://knowing-climate.eu)
:**funding**: [commission.europa.eu](https://commission.europa.eu/funding-tenders/find-funding/eu-funding-programmes/horizon-europe_en)
:**description**: Modelling of electricity and district heating systems for a full decarbonisation path in 2050 for four demonstration regions: Tallinn, Granollers, Naples and South Westphalia.
:**AIT contact**: K. Tovaas

---

## Contributing

To contribute a new reference, either

- fork the [iesopt](https://github.com/ait-energy/iesopt) repository, and directly add to the above list, or
- open an issue with the reference details.

See the template below for the structure of a reference.

### Template

```markdown
(references-projects-project-slug-title)=
### Project Slug Title

:**title**: Full Project Title
:**homepage**: [something.com](https://www.something.com/)
:**funding**: [ffg.at](https://projekte.ffg.at/projekt/XXXXXXXXX)
:**description**: some copy-pasted, or other sort of short description / abstract goes here
:**AIT contact**: F. Lastname

---
```

Consider the following:

- If possible link to an `ait.ac.at` subpage for `homepage`.
- Project slug might be `HyTechonomy`, with the full title being `Hydrogen Technologies for Sustainable Economies`, then the link target (the thing above the slug title `(references-projects-project-slug-title)=`) would then be `(references-projects-hytechonomy)=`.
- Replace the `funding` information accordingly.
