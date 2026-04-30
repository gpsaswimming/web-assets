import os
import sys
import argparse
import html

# --- Configuration ---
OUTPUT_FILE = "index.html"
PAGE_TITLE = "GPSA Files"
EXCLUDE_DIRS = ['.git', 'scripts']
EXCLUDE_FILES = ['CLAUDE.md', 'README.md', 'CNAME', '.gitignore', '.nojekyll']

CSS_URL = "https://css.gpsaswimming.org/gpsa-tools-common.css"


def find_repository_root(start_path):
    current = os.path.abspath(start_path)
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.abspath(start_path)

def generate_index_for_single_directory(current_path, subdirs, files, repo_root):
    try:
        css_path = CSS_URL

        current_abs = os.path.abspath(current_path)
        repo_abs = os.path.abspath(repo_root)

        if current_abs == repo_abs:
            dir_name = os.path.basename(repo_abs)
            breadcrumb_html = f'<h1 class="text-2xl sm:text-3xl md:text-4xl font-bold">{html.escape(dir_name)}</h1>'
        else:
            rel_path = os.path.relpath(current_abs, repo_abs).replace('\\', '/')
            path_parts = rel_path.split('/')

            breadcrumbs = []

            levels_up = len(path_parts)
            home_link = '../' * levels_up + 'index.html'
            breadcrumbs.append(f'<a href="{home_link}" class="hover:underline">Home</a>')

            for i, part in enumerate(path_parts[:-1]):
                levels_up = len(path_parts) - i - 1
                segment_link = '../' * levels_up + 'index.html'
                breadcrumbs.append(f'<a href="{segment_link}" class="hover:underline">{html.escape(part)}</a>')

            breadcrumbs.append(f'<span class="font-semibold">{html.escape(path_parts[-1])}</span>')

            breadcrumb_html = f'<h1 class="text-xl sm:text-2xl md:text-3xl font-bold">{" / ".join(breadcrumbs)}</h1>'

            dir_name = rel_path

        print(f"  → Display: {dir_name}")

        all_items = sorted(subdirs + files, key=str.lower)
        all_items = [item for item in all_items if item != OUTPUT_FILE and item not in EXCLUDE_FILES]

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(PAGE_TITLE)} - {html.escape(dir_name)}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{css_path}">
  <style>
    .gpsa-header h1 a {{
      color: white;
      text-decoration: none;
      opacity: 0.9;
      transition: opacity 0.2s;
    }}
    .gpsa-header h1 a:hover {{
      opacity: 1;
      text-decoration: underline;
    }}
    .directory-item {{
      transition: all 0.2s;
    }}
    .directory-item:hover {{
      transform: translateX(4px);
      background-color: #f9fafb;
    }}
    .directory-icon {{
      font-size: 1.5rem;
      margin-right: 0.75rem;
    }}
  </style>
</head>
<body>
  <main class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">
      <header class="gpsa-header p-4 shadow-md flex items-center justify-center no-print mb-6 rounded-lg">
        <img src="https://publicity.gpsaswimming.org/assets/gpsa_logo.png"
             alt="GPSA Logo"
             class="h-16 w-16 md:h-20 md:w-20 mr-4 rounded-full"
             onerror="this.onerror=null; this.src='https://placehold.co/100x100/002366/FFFFFF?text=GPSA';">
        <div>
          {breadcrumb_html}
          <p class="gpsa-header-subtitle">Directory Listing</p>
        </div>
      </header>

      <div class="bg-white rounded-xl shadow-lg p-6">
"""

        if not all_items:
            html_content += """        <p class="text-gray-500 text-center py-8">No files or directories found.</p>\n"""
        else:
            html_content += """        <ul class="space-y-2">\n"""
            for item_name in all_items:
                escaped_item = html.escape(item_name)

                if item_name in subdirs:
                    icon = "📁"
                    link_target = f"{escaped_item}/"
                else:
                    icon = "📄"
                    link_target = escaped_item

                html_content += f"""          <li class="directory-item">
            <a href='{link_target}' class="flex items-center p-3 rounded-lg border border-gray-200" style="text-decoration: none; color: #002366;">
              <span class="directory-icon">{icon}</span>
              <span class="font-medium">{escaped_item}</span>
            </a>
          </li>\n"""
            html_content += """        </ul>\n"""

        html_content += """      </div>

      <div class="text-center mt-6 text-gray-500 text-sm">
        <p>Greater Peninsula Swimming Association</p>
      </div>
    </div>
  </main>
</body>
</html>"""

        output_file_path = os.path.join(current_path, OUTPUT_FILE)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Index generated for: '{output_file_path}'")

    except Exception as e:
        print(f"❌ An error occurred while processing {current_path}: {e}")

def crawl_and_index(root_path):
    if not os.path.isdir(root_path):
        print(f"❌ Error: The specified root path '{root_path}' is not a valid directory.")
        sys.exit(1)

    crawl_start_path = os.path.abspath(root_path)
    repo_root = find_repository_root(crawl_start_path)

    print(f"🚀 Starting crawl from '{crawl_start_path}'...")
    print(f"📁 Repository root detected at '{repo_root}'")

    for current_path, dir_names, file_names in os.walk(root_path, topdown=True):
        dir_names[:] = [d for d in dir_names if d not in EXCLUDE_DIRS and not d.startswith('.')]
        visible_files = [f for f in file_names if not f.startswith('.')]
        generate_index_for_single_directory(current_path, dir_names, visible_files, repo_root)

    print("\n✨ Crawl complete!")

def main():
    parser = argparse.ArgumentParser(
        description="Recursively generate index.html files for a directory tree.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("folder_path", help="The root path of the folder to crawl and index.")
    args = parser.parse_args()
    crawl_and_index(args.folder_path)

if __name__ == "__main__":
    main()
