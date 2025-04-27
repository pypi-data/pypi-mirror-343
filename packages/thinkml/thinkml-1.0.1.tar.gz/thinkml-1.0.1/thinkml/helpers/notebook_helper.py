"""
Notebook Helper Module for ThinkML

This module provides Jupyter notebook integration for ThinkML, making it easier
to use the library's features in interactive environments.
"""

import inspect
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

import IPython
from IPython.core.magic import Magics, cell_magic, line_magic, magics_class
from IPython.display import display, HTML


@magics_class
class ThinkMLMagics(Magics):
    """Magic commands for ThinkML in Jupyter notebooks."""

    @line_magic
    def thinkml(self, line: str) -> None:
        """
        ThinkML magic command for Jupyter notebooks.
        
        Usage:
            %thinkml modules     # Show available modules
            %thinkml classes     # Show available classes
            %thinkml methods     # Show available methods
            %thinkml example     # Show usage examples
            %thinkml pipeline    # Show complete pipeline example
            %thinkml help        # Show help information
        """
        command = line.strip().lower()
        
        if command == "modules":
            self._show_modules()
        elif command == "classes":
            self._show_classes()
        elif command == "methods":
            self._show_methods()
        elif command == "example":
            self._show_example()
        elif command == "pipeline":
            self._show_pipeline()
        elif command == "help":
            self._show_help()
        else:
            print("Unknown command. Use %thinkml help for available commands.")

    def _show_modules(self) -> None:
        """Display available ThinkML modules."""
        import thinkml
        modules = [name for name, _ in inspect.getmembers(thinkml) 
                  if inspect.ismodule(_) and name != 'helpers']
        
        html = "<h3>Available ThinkML Modules:</h3><ul>"
        for module in sorted(modules):
            html += f"<li>{module}</li>"
        html += "</ul>"
        display(HTML(html))

    def _show_classes(self) -> None:
        """Display available ThinkML classes."""
        import thinkml
        classes = []
        for name, obj in inspect.getmembers(thinkml):
            if inspect.isclass(obj) and obj.__module__.startswith('thinkml'):
                classes.append((name, obj.__module__))
        
        html = "<h3>Available ThinkML Classes:</h3><ul>"
        for name, module in sorted(classes):
            html += f"<li>{name} ({module})</li>"
        html += "</ul>"
        display(HTML(html))

    def _show_methods(self) -> None:
        """Display available ThinkML methods."""
        import thinkml
        methods = []
        for name, obj in inspect.getmembers(thinkml):
            if inspect.isfunction(obj) and obj.__module__.startswith('thinkml'):
                methods.append((name, obj.__module__))
        
        html = "<h3>Available ThinkML Methods:</h3><ul>"
        for name, module in sorted(methods):
            html += f"<li>{name} ({module})</li>"
        html += "</ul>"
        display(HTML(html))

    def _show_example(self) -> None:
        """Display usage examples."""
        examples = {
            'validation': '''
from thinkml.validation import NestedCrossValidator
validator = NestedCrossValidator(
    estimator=RandomForestClassifier(),
    param_grid={'n_estimators': [100, 200]},
    cv=5
)
scores = validator.fit_predict(X, y)
''',
            'optimization': '''
from thinkml.optimization import EarlyStopping
early_stopping = EarlyStopping(
    patience=5,
    min_delta=0.001
)
''',
            'selection': '''
from thinkml.selection import BayesianOptimizer
optimizer = BayesianOptimizer(
    estimator=RandomForestClassifier(),
    param_space={
        'n_estimators': (100, 1000),
        'max_depth': (3, 10)
    }
)
best_params = optimizer.optimize(X, y)
'''
        }
        
        html = "<h3>Usage Examples:</h3>"
        for module, example in examples.items():
            html += f"<h4>{module.title()}</h4><pre>{example}</pre>"
        display(HTML(html))

    def _show_pipeline(self) -> None:
        """Display complete pipeline example."""
        pipeline_example = '''
# Import required modules
from thinkml.validation import NestedCrossValidator
from thinkml.optimization import EarlyStopping
from thinkml.selection import BayesianOptimizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Create preprocessing pipeline
preprocessor = Pipeline([
    ('scaler', StandardScaler())
])

# Create model with hyperparameter optimization
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

# Setup validation
validator = NestedCrossValidator(
    estimator=model,
    param_grid={
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [3, 5, 7]
    },
    cv=5
)

# Fit and evaluate
scores = validator.fit_predict(X, y)
print(f"Cross-validation scores: {scores}")
'''
        
        html = "<h3>Complete Pipeline Example:</h3><pre>" + pipeline_example + "</pre>"
        display(HTML(html))

    def _show_help(self) -> None:
        """Display help information."""
        help_text = """
ThinkML Magic Commands:

%thinkml modules     - Show available ThinkML modules
%thinkml classes     - Show available ThinkML classes
%thinkml methods     - Show available ThinkML methods
%thinkml example     - Show usage examples
%thinkml pipeline    - Show complete pipeline example
%thinkml help        - Show this help message

For more information, visit the ThinkML documentation.
"""
        display(HTML(f"<pre>{help_text}</pre>"))


def load_ipython_extension(ipython: IPython.core.interactiveshell.InteractiveShell) -> None:
    """Load the ThinkML magic commands in IPython."""
    ipython.register_magics(ThinkMLMagics)


class ThinkMLHelper:
    """Helper class for using ThinkML in Jupyter notebooks."""
    
    def __init__(self) -> None:
        """Initialize the ThinkML helper."""
        self.magics = ThinkMLMagics(shell=IPython.get_ipython())
    
    def show_modules(self) -> None:
        """Show available ThinkML modules."""
        self.magics._show_modules()
    
    def show_classes(self, module: Optional[str] = None) -> None:
        """Show available ThinkML classes."""
        self.magics._show_classes()
    
    def show_methods(self, class_name: Optional[str] = None) -> None:
        """Show available ThinkML methods."""
        self.magics._show_methods()
    
    def show_example(self, module: Optional[str] = None) -> None:
        """Show usage examples."""
        self.magics._show_example()
    
    def show_complete_pipeline(self) -> None:
        """Show complete pipeline example."""
        self.magics._show_pipeline()
    
    def help(self, topic: Optional[str] = None) -> None:
        """Show help information."""
        self.magics._show_help() 