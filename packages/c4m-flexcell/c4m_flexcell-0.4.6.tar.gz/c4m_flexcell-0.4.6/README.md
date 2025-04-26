# Flexible, scalable, standard cell library

A standard cell library is a collection of cells that perform certain digital functions. It consists of so-called combinatorial cells which perform a binary logic function and sequential cells sync internal signal with a clock signal.

Standard cells are introduced into an [ASIC](https://en.wikipedia.org/wiki/Application-specific_integrated_circuit) [EDA](https://en.wikipedia.org/wiki/Electronic_design_automation) flow during the synthesis step. This is the step where a (RTL) logic design into a netlist consisting only of the cells from your standard cell library. Later on these cells are then placed next to each and the inputs and outputs of each cell connected to each other. The former is called placement and the latter routing.

## Release History

* [v0.4.6](https://gitlab.com/Chips4Makers/c4m-flexcell/-/commits/v0.4.6):
  * DRC fixing for _Tie cell
  * Update for PDKMaster 0.12.0 API changes
  * Code cleansing
* [v0.4.5](https://gitlab.com/Chips4Makers/c4m-flexcell/-/commits/v0.4.5):
  Some internal routing optimizations in the cells.
* [v0.4.4](https://gitlab.com/Chips4Makers/c4m-flexcell/-/commits/v0.4.4):
  Mainly update for signoff fixing and new PDK support.
* [v0.4.3](https://gitlab.com/Chips4Makers/c4m-flexcell/-/commits/v0.4.3):
  * regular code cleansing
  * update layout generation to avoid DRC violation with updated primitives in PDKMaster
* [v0.4.2](https://gitlab.com/Chips4Makers/c4m-flexcell/-/commits/v0.4.2): only internal
  improvements
* v0.4.1:
  major reworking of the code. A new class ActiveColumnsCell has been introduced to generate the layouts of the standard cells. This removes the lambda based dimensions from the cells to compute them all from the design rules.  
  All cells were converter to this new layout method and this should allow to make standard cell libraries with much lower height of the cells. Compatiblity function are provided so that layout spec can be derived as was done previously as based on a lambda value.  
  v0.4.0 had only dev releases and code was rebased and squashed for this release.
* v0.3.3: bug fix; remove public 0.3.2 release
* v0.3.2: code cleansing, bug fixing, update dependencies
* v0.3.1: small update for Coriolis export
* v0.3.0: Update for [release v0.9.0 of PDKMaster](https://gitlab.com/Chips4Makers/PDKMaster/-/blob/v0.9.0/ReleaseNotes/v0.9.0.md); replace Library-> StdCellFactory to follow common usage of a factory to generate cells.
* v0.2.0: Small updates for changing PDKMaster API
* [v0.1.0](https://gitlab.com/Chips4Makers/c4m-flexcell/-/blob/v0.1.0/ReleaseNotes/v0.1.0.md)
* [v0.0.4](https://gitlab.com/Chips4Makers/c4m-flexcell/-/blob/v0.1.0/ReleaseNotes/v0.0.4.md)

## Rationale

Up to now for a lot of standard cell libraries the layout was done manually leading to a lot manual work when changes need to be done like changing the height of the cells or porting it to another technology node. Some of them are based on so-called [lambda rules](http://www.electronics-tutorial.net/Digital-CMOS-Design/CMOS-Layout-Design/CMOS-lambda-Design-Rules/) to make them scalable to different nodes. Usage of [lambda rules](http://www.electronics-tutorial.net/Digital-CMOS-Design/CMOS-Layout-Design/CMOS-lambda-Design-Rules/) will cause their own inefficiencies in the layout especially when scaling to smaller nodes.  
Alternative implementations try to fully automate the layout generation out of the transistor netlist. Finding a good placement of the transistor for non-trivial logic cells is a hard problem leading often to complex code for finding acceptable solutions. Also the layout code itself often becomes complex to take peculiarities of different design rules into account.  
The `flexcell` library tries to take a middle road. It will start from a topological layout of the cell but without the layout already fixed to certain design rules; it thus avoid the step where netlist need to be converted to topologies. It will use the design rules from a PDKMaster Technology object to generate an optimized layout for conforming to the cells topology. By baking in independence of the Technology the standard cell library should be easily ported to different technologies with better area efficiency than current [lambda rules](http://www.electronics-tutorial.net/Digital-CMOS-Design/CMOS-Layout-Design/CMOS-lambda-Design-Rules/) based solutions.  
In future options are planned so libraries can be generated for different targets like ,minimum area, maximum performance or minimum power consumption.

## Status

This repository is currently considered experimental code with no backwards compatibility guarantees whatsoever.  
Current implementation is based on the topology of the Coriolis nsxlib standard cells with some area improvements but not yet with optimal area use. For v0.1 of this library a total replacement of the layout generation is planned fully based on minimized area for the technology design rules.  
If interested head over to [gitter](https://gitter.im/Chips4Makers/community) for further discussion.

## Project Arrakeen subproject

This project is part of Chips4Makers' [project Arrakeen](https://gitlab.com/Chips4Makers/c4m-arrakeen). It shares some common guide lines and regulations:

* [Contributing.md](https://gitlab.com/Chips4Makers/c4m-arrakeen/-/blob/redtape_v1/Contributing.md)
* [LICENSE.md](https://gitlab.com/Chips4Makers/c4m-arrakeen/-/blob/redtape_v1/LICENSE.md): license of release code
* [LICENSE_rationale.md](https://gitlab.com/Chips4Makers/c4m-arrakeen/-/blob/redtape_v1/LICENSE_rationale.md)
