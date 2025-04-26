import typer
import shutil
from pathlib import Path
from importlib.resources import files

app = typer.Typer()

def copy_template(project_name: str):
    try:
        # Get template path from package
        template_path = files("fastsecforge").joinpath("templates/project_template")
        
        # Create project directory
        project_path = Path(project_name)
        project_path.mkdir(exist_ok=False)
        
        # Copy template files
        shutil.copytree(
            template_path,
            project_path,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns('__pycache__')
        )
        
        # Rename placeholder directory
        src_dir = project_path / "src" / "PROJECT_NAME"
        new_src_dir = project_path / "src" / project_name
        src_dir.rename(new_src_dir)
        
        # Update requirements.txt path
        (project_path / "requirements.txt").rename(new_src_dir / "requirements.txt")
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

@app.command()
def new(project_name: str):
    """Create new FastAPI project with security boilerplate"""
    if copy_template(project_name):
        print(f"\n✅ Successfully created project: {project_name}")
        print(f"\nNext steps:\ncd {project_name}\nuvicorn src.{project_name}.main:app --reload\n")
    else:
        print("❌ Project creation failed")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()