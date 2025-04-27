"""
Report generation functionality for ThinkML.

This module provides functions for generating comprehensive reports
of machine learning experiments, including data summaries,
preprocessing steps, and model evaluation results.
"""

import os
import base64
from typing import Dict, List, Union, Optional
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Environment, FileSystemLoader
import pdfkit
from io import BytesIO

def _create_visualizations(data_summary: Dict) -> Dict[str, str]:
    """
    Create visualizations for the report.
    
    Parameters
    ----------
    data_summary : Dict
        Dictionary containing dataset summary information
        
    Returns
    -------
    Dict[str, str]
        Dictionary of base64 encoded images
    """
    visualizations = {}
    
    # Create feature distribution plots
    if 'feature_types' in data_summary:
        plt.figure(figsize=(10, 6))
        feature_types = data_summary['feature_types']
        plt.bar(feature_types.keys(), feature_types.values())
        plt.title('Feature Types Distribution')
        plt.xlabel('Feature Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        
        # Save plot to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        visualizations['feature_types'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
    
    # Create missing values heatmap
    if 'missing_values' in data_summary:
        plt.figure(figsize=(10, 6))
        missing_data = data_summary['missing_values']
        sns.heatmap(missing_data.reshape(1, -1), 
                   annot=True, 
                   fmt='.2f',
                   cmap='YlOrRd')
        plt.title('Missing Values Heatmap')
        
        # Save plot to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        visualizations['missing_values'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
    
    # Create class imbalance plot
    if 'class_distribution' in data_summary:
        plt.figure(figsize=(10, 6))
        class_dist = data_summary['class_distribution']
        plt.bar(class_dist.keys(), class_dist.values())
        plt.title('Class Distribution')
        plt.xlabel('Class')
        plt.ylabel('Count')
        
        # Save plot to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        visualizations['class_distribution'] = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
    
    return visualizations

def _create_html_report(
    data_summary: Dict,
    preprocessing_steps: List[str],
    models_results: Dict,
    visualizations: Dict[str, str]
) -> str:
    """
    Create HTML report using Jinja2 template.
    
    Parameters
    ----------
    data_summary : Dict
        Dictionary containing dataset summary information
    preprocessing_steps : List[str]
        List of preprocessing steps applied
    models_results : Dict
        Dictionary containing model evaluation results
    visualizations : Dict[str, str]
        Dictionary of base64 encoded images
        
    Returns
    -------
    str
        HTML report content
    """
    # Create Jinja2 environment
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template('report_template.html')
    
    # Render template
    html_content = template.render(
        data_summary=data_summary,
        preprocessing_steps=preprocessing_steps,
        models_results=models_results,
        visualizations=visualizations
    )
    
    return html_content

def generate_report(
    data_summary: Dict,
    preprocessing_steps: List[str],
    models_results: Dict,
    output_format: str = 'html',
    filename: str = 'report'
) -> None:
    """
    Generate a comprehensive report of the machine learning experiment.
    
    Parameters
    ----------
    data_summary : Dict
        Dictionary containing dataset summary information:
        - shape: tuple of (n_samples, n_features)
        - missing_values: numpy array of missing value counts
        - feature_types: dict of feature type counts
        - class_distribution: dict of class counts (for classification)
    preprocessing_steps : List[str]
        List of preprocessing steps applied to the data
    models_results : Dict
        Dictionary containing model evaluation results:
        - metrics: dict of metric names and values
        - selected_model: str, name of the best performing model
    output_format : str, optional
        Output format, either 'html' or 'pdf', by default 'html'
    filename : str, optional
        Output filename without extension, by default 'report'
        
    Returns
    -------
    None
        
    Raises
    ------
    ValueError
        If output_format is not 'html' or 'pdf'
    """
    # Validate output format
    if output_format not in ['html', 'pdf']:
        raise ValueError("output_format must be either 'html' or 'pdf'")
    
    # Create visualizations
    visualizations = _create_visualizations(data_summary)
    
    # Generate HTML content
    html_content = _create_html_report(
        data_summary,
        preprocessing_steps,
        models_results,
        visualizations
    )
    
    # Save report
    if output_format == 'html':
        output_file = f"{filename}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    else:  # PDF
        output_file = f"{filename}.pdf"
        pdfkit.from_string(html_content, output_file) 