import json
import tempfile
import os
from pathlib import Path
from typing import List, Dict, Union, Optional, Tuple, Any, Literal
from rdkit import Chem
from deeporigin_molstar.src.viewers.molecule_viewer import LigandConfig
from deeporigin_molstar.src.viewers.protein_viewer import ProteinConfig
from deeporigin_molstar.src.viewers.viewer import Viewer


class DockingViewer(Viewer):
    def __init__(self, html: str = ''):
        """
        Initializes a DockingViewer object.

        Args:
            html (str): The HTML content to be displayed in the viewer.

        """
        super().__init__(
            data='', format='pdb', html=html
        )
        self._temp_files_to_cleanup = []
    
    def _is_path(self, raw):
        """Helper method to check if the input is a file path."""
        try:
            is_path = Path(raw).is_file()
        except (TypeError, OSError):
            is_path = False
        return is_path
    
    def _get_mol_format(self, data: str) -> Literal['mol2', 'mol', 'sdf']:
        """
        Determine the molecule format based on content
        
        Args:
            data (str): Molecular data as string
            
        Returns:
            Literal['mol2', 'mol', 'sdf']: Format identifier
        """
        data_lower = data.lower()
        if '@<TRIPOS>MOLECULE' in data_lower:
            return 'mol2'
        elif 'v2000' in data_lower or 'v3000' in data_lower:
            return 'mol'
        else:
            return 'sdf'
    
    def _read_molecules_with_rdkit(self, data: str, format_type: Literal['mol2', 'mol', 'sdf']):
        """
        Read multiple molecules from data using RDKit
        
        Args:
            data (str): Molecule data or file path
            format_type (Literal['mol2', 'mol', 'sdf']): Format of the molecule
            
        Returns:
            List[Chem.Mol]: List of RDKit.Mol objects
        """
        mols = []
        
        if self._is_path(data):
            if format_type.lower() == 'mol2':
                with open(data, 'r') as f:
                    content = f.read()
                
                mol_blocks = content.split('@<TRIPOS>MOLECULE')
                if len(mol_blocks) > 1:
                    mol_blocks = mol_blocks[1:] if not mol_blocks[0].strip() else mol_blocks
                
                for mol_block in mol_blocks:
                    if mol_block.strip():
                        mol_content = '@<TRIPOS>MOLECULE' + mol_block
                        with tempfile.NamedTemporaryFile(suffix='.mol2', delete=False) as tmp_file:
                            tmp_file.write(mol_content.encode('utf-8'))
                            tmp_path = tmp_file.name
                        try:
                            mol = Chem.MolFromMol2File(tmp_path)
                            if mol:
                                mols.append(mol)
                        finally:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
            
            elif format_type.lower() == 'mol':
                mol = Chem.MolFromMolFile(data)
                if mol:
                    mols.append(mol)
            
            else:
                supplier = Chem.SDMolSupplier(data)
                for mol in supplier:
                    if mol:
                        mols.append(mol)
        
        else:
            if format_type.lower() == 'mol2':
                mol_blocks = data.split('@<TRIPOS>MOLECULE')
                if len(mol_blocks) > 1:
                    mol_blocks = mol_blocks[1:] if not mol_blocks[0].strip() else mol_blocks
                
                for mol_block in mol_blocks:
                    if mol_block.strip():
                        mol_content = '@<TRIPOS>MOLECULE' + mol_block
                        with tempfile.NamedTemporaryFile(suffix='.mol2', delete=False) as tmp_file:
                            tmp_file.write(mol_content.encode('utf-8'))
                            tmp_path = tmp_file.name
                        try:
                            mol = Chem.MolFromMol2File(tmp_path)
                            if mol:
                                mols.append(mol)
                        finally:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
            
            elif format_type.lower() == 'mol':
                mol = Chem.MolFromMolBlock(data)
                if mol:
                    mols.append(mol)
            
            elif format_type.lower() == 'sdf':
                supplier = Chem.SDMolSupplier()
                supplier.SetData(data)
                for mol in supplier:
                    if mol:
                        mols.append(mol)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
        
        return mols
    
    def _prepare_paginated_ligands(self, ligands_data: List[str], ligand_format: Optional[Literal['mol2', 'mol', 'sdf']] = None) -> Tuple[str, Literal['sdf']]:
        """
        Prepare ligands for pagination by combining them into a single SDF file using RDKit.
        
        Args:
            ligands_data (List[str]): List of ligand data strings or file paths
            ligand_format (Optional[Literal['mol2', 'mol', 'sdf']]): Format of the ligand data, auto-detected if None
            
        Returns:
            Tuple[str, Literal['sdf']]: (path to combined file, format)
        """
        with tempfile.NamedTemporaryFile(suffix='.sdf', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        writer = Chem.SDWriter(tmp_path)
        
        for data in ligands_data:
            current_format = ligand_format
            if not current_format:
                if self._is_path(data):
                    file_ext = os.path.splitext(data)[1].lower()
                    if file_ext == '.mol2':
                        current_format = 'mol2'
                    elif file_ext == '.mol':
                        current_format = 'mol'
                    elif file_ext == '.sdf':
                        current_format = 'sdf'
                    else:
                        with open(data, 'r') as f:
                            content_sample = f.read()
                        current_format = self._get_mol_format(content_sample)
                else:
                    current_format = self._get_mol_format(data)
            
            mols = self._read_molecules_with_rdkit(data, current_format)
            if mols:
                for mol in mols:
                    writer.write(mol)
            else:
                print(f"Warning: Failed to read molecule data with format {current_format}")
        
        writer.close()
        return tmp_path, 'sdf'

    def render_with_seperate_crystal(
            self, 
            protein_data: str, 
            protein_format: str, 
            ligands_data: List[str], 
            ligand_format: Literal['mol2', 'mol', 'sdf'], 
            crystal_data: Optional[Dict[str, str]] = None,
            protein_config: Optional[ProteinConfig] = None, 
            ligand_config: Optional[LigandConfig] = None,
            paginate: bool = True,
            finalize: bool = True
        ) -> str:
        """
        Renders merged structures using the provided protein, ligand and native crystal data.

        Args:
            protein_data (str): The protein data to be rendered.
            protein_format (str): The format of the protein data.
            ligands_data (List[str]): The list of ligand data to be rendered.
            ligand_format (str): The format of the ligand data.
            crystal_data (Optional[Dict[str, str]]): The native crystal data, optional
            protein_config (Optional[ProteinConfig]): Configuration for protein rendering
            ligand_config (Optional[LigandConfig]): Configuration for ligand rendering
            paginate (bool): Whether to paginate ligands (combine into single SDF)
            finalize (bool): Whether to finalize HTML output

        Returns:
            str: The HTML representation of the rendered structures.
        """

        if not protein_config:
            protein_config = ProteinConfig()

        if not ligand_config:
            ligand_config = LigandConfig()

        def prepare_data(raw, _format):
            if self._is_path(raw):
                return self.load_from_file(raw, _format)
            return self.load_from_data(raw, _format)

        representations = [
            {'componentType': 'polymer', 'representationConfig': {'type': protein_config.style_type, 'typeParams': {'alpha': protein_config.surface_alpha, 'quality': 'high'}}},
            {'componentType': 'ligand', 'representationConfig': {'type': ligand_config.style_type, 'typeParams': {'alpha': ligand_config.surface_alpha, 'quality': 'high'}}}
        ]

        formatted_representations = ', '.join(
            f"{{componentType: '{representation['componentType']}', representationConfig: {{type: '{representation['representationConfig']['type']}', typeParams: {{alpha: {representation['representationConfig']['typeParams']['alpha']}, quality: '{representation['representationConfig']['typeParams']['quality']}'}}}}}}"
            for representation in representations
        )

        raw_source = [
            {'raw': protein_data, 'format': protein_format}
        ]

        if paginate and len(ligands_data) > 1:
            combined_path, combined_format = self._prepare_paginated_ligands(ligands_data, ligand_format)
            raw_source.append({'raw': combined_path, 'format': combined_format})
            
            self._temp_files_to_cleanup.append(combined_path)
        else:
            for data in ligands_data:
                raw_source.append({'raw': data, 'format': ligand_format})

        sources = [prepare_data(source['raw'], source['format']) for source in raw_source]
        formatted_sources = ', '.join([f"{{raw: `{raw}`, format: '{_format}'}}" for raw, _format in sources])
        
        formatted_crystal = ""
        if crystal_data and isinstance(crystal_data, dict) and 'raw' in crystal_data and 'format' in crystal_data:
            crystal_from_raw = prepare_data(crystal_data['raw'], crystal_data['format'])
            formatted_crystal = f"{{raw: `{crystal_from_raw[0]}`, format: '{crystal_from_raw[1]}'}}"
        
        js_code = f"await Renderer.renderStructureWithSeperateCrystal([{formatted_representations}], [{formatted_sources}], Renderer.renderMergedRawStructuresAndMergeWithRepresentation{', ' + formatted_crystal if formatted_crystal else ''});"
                    
        self.add_component(js_code)
        if finalize:
            self.add_suffix()

        return self.html

    def render_merged_structures(
            self, 
            protein_data: str, 
            protein_format: str, 
            ligands_data: List[str], 
            ligand_format: Literal['mol2', 'mol', 'sdf'], 
            protein_config: Optional[ProteinConfig] = None, 
            ligand_config: Optional[LigandConfig] = None, 
            paginate: bool = True,
            finalize: bool = True
        ) -> str:
        """
        Renders merged structures using the provided protein and ligand data.

        Args:
            protein_data (str): The protein data to be rendered.
            protein_format (str): The format of the protein data.
            ligands_data (List[str]): The list of ligand data to be rendered.
            ligand_format (str): The format of the ligand data.
            protein_config (Optional[ProteinConfig]): Configuration for protein rendering
            ligand_config (Optional[LigandConfig]): Configuration for ligand rendering
            paginate (bool): Whether to paginate ligands (combine into single SDF)
            finalize (bool): Whether to finalize HTML output

        Returns:
            str: The HTML representation of the rendered structures.
        """

        if not protein_config:
            protein_config = ProteinConfig()

        if not ligand_config:
            ligand_config = LigandConfig()

        def prepare_data(raw, _format):
            is_path = self._is_path(raw)
            if is_path:
                return self.load_from_file(raw, _format)
            return self.load_from_data(raw, _format)

        representations = [
            {'componentType': 'polymer', 'representationConfig': {'type': protein_config.style_type, 'typeParams': {'alpha': protein_config.surface_alpha, 'quality': 'high'}}},
            {'componentType': 'ligand', 'representationConfig': {'type': ligand_config.style_type, 'typeParams': {'alpha': ligand_config.surface_alpha, 'quality': 'high'}}}
        ]

        formatted_representations = ', '.join(
            f"{{componentType: '{representation['componentType']}', representationConfig: {{type: '{representation['representationConfig']['type']}', typeParams: {{alpha: {representation['representationConfig']['typeParams']['alpha']}, quality: '{representation['representationConfig']['typeParams']['quality']}'}}}}}}"
            for representation in representations
        )

        raw_source = [
            {'raw': protein_data, 'format': protein_format}
        ]
        
        if paginate and len(ligands_data) > 1:
            combined_path, combined_format = self._prepare_paginated_ligands(ligands_data, ligand_format)
            raw_source.append({'raw': combined_path, 'format': combined_format})
            
            self._temp_files_to_cleanup.append(combined_path)
        else:
            for data in ligands_data:
                raw_source.append({'raw': data, 'format': ligand_format})

        sources = [prepare_data(source['raw'], source['format']) for source in raw_source]
        formatted_sources = ', '.join([f"{{raw: `{raw}`, format: '{_format}'}}" for raw, _format in sources])
        js_code = f"await Renderer.renderWithNativeCrystalControl([{formatted_representations}], [{formatted_sources}], Renderer.renderMergedRawStructuresAndMergeWithRepresentation);"
                    
        self.add_component(js_code)
        if finalize:
            self.add_suffix()
            
        return self.html
    
    def __del__(self):
        """Cleanup temporary files when the object is destroyed"""
        temp_files = getattr(self, '_temp_files_to_cleanup', [])
        for file_path in temp_files:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error cleaning up temp file {file_path}: {e}")
                
    def cleanup_temp_files(self):
        """
        Manually cleanup temporary files
        Useful when you want to explicitly clean up before object destruction
        """
        temp_files = getattr(self, '_temp_files_to_cleanup', [])
        for file_path in temp_files:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error cleaning up temp file {file_path}: {e}")
        
        self._temp_files_to_cleanup = []

    @classmethod
    def render_ligand_with_bounding_box(cls, protein_data: str, protein_format: str, ligand_data: str, ligand_format: str,
                                        box: Dict[str, List[float]], path: Optional[str] = None) -> str:
        """
        Render a ligand with a bounding box around it
        
        Args:
            protein_data (str): Protein data or file path
            protein_format (str): Format of the protein data
            ligand_data (str): Ligand data or file path
            ligand_format (str): Format of the ligand data
            box (Dict[str, List[float]]): Dictionary with 'min' and 'max' coordinates
            path (Optional[str]): Path to save the HTML output
            
        Returns:
            str: HTML output
        """
        viewer = Viewer('', 'pdb')

        def prepare_data(raw, _format):
            try:
                is_path = Path(raw).is_file()
            except (TypeError, OSError):
                is_path = False

            if is_path:
                return viewer.load_from_file(raw, _format)
            return viewer.load_from_data(raw, _format)

        formatted_box = f"{{min: {box['min']}, max: {box['max']}}}"
        raw_source = [
            {'raw': protein_data, 'format': protein_format},
            {'raw': ligand_data, 'format': ligand_format}
        ]
        sources = [prepare_data(source['raw'], source['format']) for source in raw_source]

        formatted_sources = ', '.join([f"{{raw: `{raw}`, format: '{_format}'}}" for raw, _format in sources])
        js_code = f"await Renderer.renderLigandWidthBoundingBox({formatted_box}, [{formatted_sources}]);"

        viewer.add_component(js_code)
        viewer.add_suffix()

        if path is not None:
            viewer.write(path)

        return viewer.html
    
    @classmethod
    def render_bounding_box(cls, protein_data: str, protein_format: str, 
                          box_center: List[float], box_size: List[float], 
                          path: Optional[str] = None) -> str:
        """
        Render a bounding box around the protein
        
        Args:
            protein_data (str): Protein data or file path
            protein_format (str): Format of the protein data
            box_center (List[float]): Center coordinates of the box [x, y, z]
            box_size (List[float]): Size of the box in each dimension [width, height, depth]
            path (Optional[str]): Path to save the HTML output
            
        Returns:
            str: HTML output
        """
        viewer = Viewer('', 'pdb')

        def prepare_data(raw, _format):
            try:
                is_path = Path(raw).is_file()
            except (TypeError, OSError):
                is_path = False

            if is_path:
                return viewer.load_from_file(raw, _format)
            return viewer.load_from_data(raw, _format)

        half_dimensions = [d / 2 for d in box_size]

        min_coords = [box_center[i] - half_dimensions[i] for i in range(len(box_center))]
        max_coords = [box_center[i] + half_dimensions[i] for i in range(len(box_center))]
        formatted_box = f"{{min: {min_coords}, max: {max_coords}}}"

        raw_source = [
            {'raw': protein_data, 'format': protein_format},
        ]
        sources = [prepare_data(source['raw'], source['format']) for source in raw_source]

        formatted_sources = ', '.join([f"{{raw: `{raw}`, format: '{_format}'}}" for raw, _format in sources])
        js_code = f"await Renderer.renderLigandWidthBoundingBox({formatted_box}, [{formatted_sources}]);"

        viewer.add_component(js_code)
        viewer.add_suffix()

        if path is not None:
            viewer.write(path)

        return viewer.html
    
    @classmethod
    def render_highlighted_residues(cls, protein_data: str, protein_format: str, residue_ids: List[str]) -> str:
        """
        Render protein with highlighted residues
        
        Args:
            protein_data (str): Protein data or file path
            protein_format (str): Format of the protein data
            residue_ids (List[str]): List of residue IDs to highlight
            
        Returns:
            str: HTML output
        """
        viewer = Viewer('', 'pdb')

        def prepare_data(raw, _format):
            try:
                is_path = Path(raw).is_file()
            except (TypeError, OSError):
                is_path = False

            if is_path:
                return viewer.load_from_file(raw, _format)
            return viewer.load_from_data(raw, _format)

        protein_data, protein_format = prepare_data(protein_data, protein_format)
        js_code = f"""
            const proteinData = `{protein_data}`;
            const format = `{protein_format}`;
            const residue_ids = {residue_ids};
            await Renderer.renderProteinPocketBasedOnResidues(
                proteinData, 
                format, 
                residue_ids
            );
        """
        viewer.add_component(js_code)
        viewer.add_suffix()
        
        return viewer.html
