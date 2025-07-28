import os
import sys
import shutil

from markdown_blocks import markdown_to_html_node
from inline_markdown import extract_title

def main():
    args = sys.argv
    basepath = ""
    if len(args) > 0:
        basepath = args[1]
    else:
        basepath = "/"
    dir_path_static = "./static"
    dir_path_public = "./docs"
    dir_path_content = "./content"
    template_path = "./template.html"

    copy_directory(dir_path_static, dir_path_public)
    generate_all_pages(dir_path_content, template_path, dir_path_public, basepath)


def copy_directory(source, destination):
    # First clear the destination to an empty directory
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    # Copy all files, subdirectories, etc.
    source_directory_list = os.listdir(source)

    for item in source_directory_list:
        path_to_item = os.path.join(source, item)
        if os.path.isfile(path_to_item):
            path_to_target = os.path.join(destination, item)
            print(f"Copying file {path_to_item} to {path_to_target}")
            shutil.copy(path_to_item, path_to_target)
        else:
            path_to_target = os.path.join(destination, item)
            print(f"Copying directory {path_to_item} to {path_to_target}")
            copy_directory(path_to_item, path_to_target)


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    
    from_file_data = ""
    with open(from_path) as file:
        from_file_data = file.read()
    
    template_file_data = ""
    with open(template_path) as file:
        template_file_data = file.read()
    
    html_data = markdown_to_html_node(from_file_data).to_html()
    
    title = extract_title(from_file_data)
    
    new_page = template_file_data.replace("{{ Content }}", html_data)
    new_page = new_page.replace("{{ Title }}", title)
    if base_path != "/":
        new_page = new_page.replace('href="/', f'href="{base_path}')
        new_page = new_page.replace('src="/', f'src="{base_path}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(new_page)


def generate_all_pages(from_directory, template_path, dest_directory, base_path):
    directory_list = os.listdir(from_directory)
    for item in directory_list:
        path_to_item = os.path.join(from_directory, item)
        if os.path.isfile(path_to_item) and path_to_item.endswith(".md"):
            path_to_target = os.path.join(dest_directory, item).removesuffix(".md") + ".html"
            generate_page(path_to_item, template_path, path_to_target, base_path)
        else:
            path_to_target = os.path.join(dest_directory, item)
            generate_all_pages(path_to_item, template_path, path_to_target, base_path)
    


main()