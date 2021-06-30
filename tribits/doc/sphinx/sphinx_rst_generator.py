import os
import subprocess
import sys

try:
    doc_path = f"{os.sep}".join(os.path.abspath(__file__).split(os.sep)[:-2])
    sys.path.append(doc_path)
    project_path = f"{os.sep}".join(os.path.abspath(__file__).split(os.sep)[:-4])
    sys.path.append(project_path)
except Exception as e:
    print(f"Can not add project path to system path! Exiting!\nERROR: {e}")
    exit(1)


class SphinxRstGenerator:
    """ Changes include paths to relative to Sphinx build dir. Saves three main .rst docs files inside Sphinx dir.
    """
    def __init__(self):
        self.paths = {
            'mainteiners_guide': {
                'src': os.path.join(doc_path, 'guides', 'maintainers_guide', 'TribitsMaintainersGuide.rst'),
                'src_path': os.path.join(doc_path, 'guides', 'maintainers_guide'),
                'final_path': os.path.join(doc_path, 'sphinx', 'maintainers_guide_rst.rst')},
            'users_guide': {
                'src': os.path.join(doc_path, 'guides', 'users_guide', 'TribitsUsersGuide.rst'),
                'src_path': os.path.join(doc_path, 'guides', 'users_guide'),
                'final_path': os.path.join(doc_path, 'sphinx', 'users_guide_rst.rst')},
            'build_ref': {
                'src': os.path.join(doc_path, 'build_ref', 'TribitsBuildReference.rst'),
                'src_path': os.path.join(doc_path, 'build_ref'),
                'final_path': os.path.join(doc_path, 'sphinx', 'build_ref_rst.rst')}}
        self.sphinx_path = os.path.abspath(os.path.join(doc_path, 'sphinx'))
        self.already_modified_files = set()
        self.build_docs()

    @staticmethod
    def build_docs() -> None:
        """ Builds TriBITS documentation based on shell scripts
        """
        build_script_path = os.path.join(doc_path, 'build_docs.sh')
        current_working_dir = os.path.split(build_script_path)[0]
        subprocess.call(build_script_path, cwd=current_working_dir)

    @staticmethod
    def is_rst_file(file_path: str) -> bool:
        """ Checks if file_path has .rst extension and if file_path is a file
        """
        if os.path.splitext(file_path)[-1] == '.rst' and os.path.isfile(file_path):
            return True
        return False

    @staticmethod
    def save_rst(file_path: str, file_content: str) -> None:
        """ Saves .rst file with given pathh and content
        """
        with open(file_path, 'w') as dest_file:
            dest_file.write(file_content)

    def generate_rst(self, source_file: str, final_path: str = None, src_path: str = None,
                     start_path: str = None) -> set:
        """ Generate corect links in .rst files, so Sphinx can find them
        """
        if final_path is None:
            overwrite_source = True
        else:
            overwrite_source = False

        file_content, includes = self.change_paths_and_get_includes(source_file=source_file, src_file_path=src_path,
                                                                    start_path=start_path)

        if overwrite_source:
            self.save_rst(file_path=source_file, file_content=file_content)
        else:
            self.save_rst(file_path=final_path, file_content=file_content)

        return includes

    def change_paths_and_get_includes(self, source_file: str, src_file_path: str, start_path: str) -> tuple:
        """ Changes paths in source file, to be relative to sphinx_path or parent .rst document.
            Returns a tuple with .rst file content and includes(absolute_path, relative_to)
        """
        with open(source_file, 'r') as src_file:
            source_file_str = src_file.read()
            source_file_list = list()
            include_file_list = set()
            for line in source_file_str.split('\n'):
                splitted_line = line.split()
                if 'include::' in splitted_line:
                    incl_index = splitted_line.index('include::')
                    path_index = incl_index + 1
                    if len(splitted_line) > path_index:
                        new_line = splitted_line[:path_index]
                        abs_path = os.path.abspath(os.path.join(src_file_path, splitted_line[path_index]))
                        if self.is_rst_file(file_path=abs_path):
                            include_file_list.add((abs_path, src_file_path))
                        rel_path_from_sphinx_dir = os.path.relpath(path=abs_path, start=start_path)
                        new_line.append(rel_path_from_sphinx_dir)
                        new_line = ' '.join(new_line)
                        source_file_list.append(new_line)
                    else:
                        source_file_list.append(line)
                else:
                    source_file_list.append(line)
            abs_path_str = '\n'.join(source_file_list)

        return abs_path_str, include_file_list

    def main(self):
        """ Main routine goes for nested .rst docs
        """
        child_rst = set()
        for doc_name, sources in self.paths.items():
            includes = self.generate_rst(source_file=sources.get('src'), src_path=sources.get('src_path'),
                                         final_path=sources.get('final_path'), start_path=self.sphinx_path)
            child_rst.update(includes)
        self.already_modified_files.update(child_rst)
        child_rst_lst = list(child_rst)

        grand_child_rst = set()
        for child in child_rst_lst:
            includes_grand = self.generate_rst(source_file=child[0], src_path=os.path.split(child[0])[0],
                                               start_path=self.sphinx_path)
            grand_child_rst.update(includes_grand)
        grand_child_rst_lst = [gc_rst for gc_rst in grand_child_rst if gc_rst not in self.already_modified_files]

        grand_grand_child_rst = set()
        for grand_child in grand_child_rst_lst:
            includes_grand_grand = self.generate_rst(source_file=grand_child[0],
                                                     src_path=os.path.split(grand_child[0])[0],
                                                     start_path=self.sphinx_path)
            grand_grand_child_rst.update(includes_grand_grand)

        if not grand_grand_child_rst:
            print('DONE! ALL GOOD!')
        else:
            print('NOT DONE!')


if __name__ == '__main__':
    SphinxRstGenerator().main()
