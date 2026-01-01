MySims Blender Add-on
======================

Importer/exporter and toolset for inspecting and editing PC MySims assets directly inside Blender. The add-on provides operators for WindowsModel meshes, Havok-based physics, and level files, plus utilities for materials and shader setup tailored to the game formats.

Features
- Import WindowsModel files (.windowsmodel, .wmdl, .0xb359c791) with optional embedded physics.
- Import Havok physics blobs (.Physics).
- Import MySims level files (.levelxml, .levelbin) to scene objects and collections.
- Export the active object back to WindowsModel binary format.
- Sidebar panel to set the game data folder and choose export modes.
- Basic shader nodes and material helpers registered on startup.

Requirements
- Blender 4.2 or newer (tested with bl_info 4.3.2).
- Access to the MySims game data directory for resolving asset references. Default path: `C:/Program Files (x86)/Steam/steamapps/common/MySims/data/`.

Installation
1) Download or clone this repository.
2) In Blender, open Edit → Preferences → Add-ons → Install… and select the downloaded zip (or the folder if using Blender 4.2+ extension management).
3) Enable "MySims Blender" in the add-on list.
4) In the 3D Viewport sidebar (N-panel) under the MySims tab, set **Game Folder** to your MySims data directory so assets can be located.

Usage
- Import models: File → Import → "MySims WindowsModel (.windowsmodel)" and choose one or more files.
- Import physics: File → Import → "MySims Physics (.Physics)".
- Import levels: File → Import → "MySims Level (.levelxml / .levelbin)".
- Export model: Select the object to export, and click the "Export" button in the sidebar.
- Game path scanning: the first time you set the game folder, the add-on indexes assets; this may take a moment.

Project Layout (high level)
- __init__.py registers Blender operators, panels, properties, and shader nodes.
- Import/: Operators for WindowsModel, Physics, and Level ingestion.
- Export/: WindowsModel exporter.
- Serializers/: Binary readers/writers for MySims formats and Havok physics.
- Shaders/, Props/, UI/, Panels/: UI components, custom properties, and shader setup used by the add-on.

Limitations and Notes
- Physics and shader support are minimal and may need manual cleanup after import.
- Paths must point to an extracted/local MySims data directory; packaged DBPF (.package) archives are not yet supported.