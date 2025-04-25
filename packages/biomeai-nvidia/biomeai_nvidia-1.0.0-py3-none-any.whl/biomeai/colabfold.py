"""
ColabFold MSA search integration module.
"""
import asyncio
import json
from typing import List, Dict, Any, Optional
import httpx
import os
from pathlib import Path

class ColabFoldMSA:
    """
    Simplified interface for ColabFold MSA search using NVIDIA Cloud Functions.
    """
    
    PUBLIC_URL = "https://health.api.nvidia.com/v1/biology/colabfold/msa-search/predict"
    STATUS_URL = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/{task_id}"
    
    # Available MSA databases
    AVAILABLE_DATABASES = {
        "all": ["Uniref30_2302", "PDB70_220313", "colabfold_envdb_202108"],
        "Uniref30_2302": ["Uniref30_2302"],
        "PDB70_220313": ["PDB70_220313"],
        "colabfold_envdb_202108": ["colabfold_envdb_202108"]
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize ColabFoldMSA with optional API key.
        If not provided, will look for NVCF_RUN_KEY in environment variables.
        """
        self.api_key = api_key or os.environ.get("NVCF_RUN_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as NVCF_RUN_KEY environment variable")
        
    @classmethod
    def list_databases(cls) -> Dict[str, List[str]]:
        """
        Get available MSA databases.
        
        Returns:
            Dict containing available database options
        """
        return cls.AVAILABLE_DATABASES

    async def _prepare_search_data(
        self,
        sequence: str,
        e_value: float = 0.0001,
        iterations: int = 1,
        databases: List[str] = ["Uniref30_2302"],
        output_formats: List[str] = ["a3m", "fasta"]
    ) -> Dict[str, Any]:
        """
        Prepare the data dictionary for MSA search.
        
        Args:
            sequence: Protein sequence to search
            e_value: E-value threshold
            iterations: Number of search iterations
            databases: List of databases to search
            output_formats: Desired output formats
            
        Returns:
            Dict containing the prepared search parameters
        """
        return {
            "sequence": sequence,
            "e_value": e_value,
            "iterations": iterations,
            "databases": databases,
            "output_alignment_formats": output_formats
        }

    async def search(
        self,
        sequence: str,
        e_value: float = 0.0001,
        iterations: int = 1,
        databases: List[str] = ["Uniref30_2302"],
        output_formats: List[str] = ["a3m", "fasta"]
    ) -> Dict[str, Any]:
        """
        Perform MSA search for the given sequence.
        
        Args:
            sequence: Protein sequence to search
            e_value: E-value threshold (default: 0.0001)
            iterations: Number of search iterations (default: 1)
            databases: List of databases to search (default: ["Uniref30_2302"])
            output_formats: Desired output formats (default: ["a3m", "fasta"])
            
        Returns:
            Dict containing the search results
        """
        data = await self._prepare_search_data(
            sequence=sequence,
            e_value=e_value,
            iterations=iterations,
            databases=databases,
            output_formats=output_formats
        )
        
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "NVCF-POLL-SECONDS": "10",
                "Content-Type": "application/json"
            }
            
            response = await client.post(
                self.PUBLIC_URL,
                json=data,
                headers=headers,
                timeout=20
            )
            
            if response.status_code == 202:
                task_id = response.headers.get("nvcf-reqid")
                while True:
                    status_response = await client.get(
                        self.STATUS_URL.format(task_id=task_id),
                        headers=headers,
                        timeout=20
                    )
                    if status_response.status_code == 200:
                        return status_response.json()
                    elif status_response.status_code in [400, 401, 404, 422, 500]:
                        raise Exception(f"Error: {status_response.text}")
            elif response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error: {response.text}")

    def search_sync(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Synchronous version of the search method.
        """
        return asyncio.run(self.search(*args, **kwargs))

    def save_results(self, results: Dict[str, Any], output_file: str) -> None:
        """
        Save search results to a file.
        
        Args:
            results: Search results dictionary
            output_file: Path to save the results
        """
        Path(output_file).write_text(json.dumps(results, indent=4))
