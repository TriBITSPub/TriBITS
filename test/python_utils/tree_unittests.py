import os
import sys
import unittest
import subprocess
from pathlib import Path

# Determine repository root (this test file lives in test/python_utils/)
THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
TREE_SCRIPT = REPO_ROOT / 'tribits' / 'python_utils' / 'tree.py'

# Make test data directory path relative to this test file's directory
TESTDATA_DIR = THIS_FILE.parent / 'tree_testdata'
if not TESTDATA_DIR.is_dir():
  raise RuntimeError(f'Expected test data directory not found: {TESTDATA_DIR}')

class TestTreeScript(unittest.TestCase):
  """Golden-output tests for tree.py.

  If the directory structure in test/python_utils/tree_testdata/ changes
  intentionally, update the expected multi-line strings in each test by
  re-running the corresponding command manually and copying stdout verbatim.
  Keep the trailing newline and all spacing intact.
  """
  maxDiff = None

  def run_tree(self, *args):
    cmd = [sys.executable, str(TREE_SCRIPT)] + list(args)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr

  def assertTreeSuccess(self, rc, stderr):
    self.assertEqual(rc, 0, msg=f"Non-zero return code. Stderr=\n{stderr}")
    self.assertEqual(stderr.strip(), '', msg=f"Expected no stderr output. Got: {stderr}")

  def test_directories_only_default(self):
    rc, out, err = self.run_tree(str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
  |
  +-.cache/
  |
  +-.git_mock/
  |
  +-.hiddenDir/
  |
  +-__pycache__/
  |
  +-dirA/
  | |
  | +-subDir1/
  | |
  | +-subDir2/
  |
  +-dirB/
''', out)

  def test_show_files(self):
    rc, out, err = self.run_tree('--show-files', str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
  |
  +-.cache/
  | |
  | +-thing
  |
  +-.git_mock/
  | |
  | +-config
  |
  +-.gitignore
  |
  +-.hiddenDir/
  | |
  | +-hiddenFile.txt
  |
  +-__pycache__/
  | |
  | +-module.cpython-311.pyc
  |
  +-dirA/
  | |
  | +-fileA1.txt
  | |
  | +-subDir1/
  | | |
  | | +-fileS1.txt
  | |
  | +-subDir2/
  | | |
  | | +-fileS2.txt
  |
  +-dirB/
  | |
  | +-fileB1.txt
  |
  +-file_root.txt
  |
  +-script.sh
''', out)

  def test_no_hidden_files(self):
    rc, out, err = self.run_tree('--show-files', '--no-hidden-files', str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
  |
  +-__pycache__/
  | |
  | +-module.cpython-311.pyc
  |
  +-dirA/
  | |
  | +-fileA1.txt
  | |
  | +-subDir1/
  | | |
  | | +-fileS1.txt
  | |
  | +-subDir2/
  | | |
  | | +-fileS2.txt
  |
  +-dirB/
  | |
  | +-fileB1.txt
  |
  +-file_root.txt
  |
  +-script.sh
''', out)

  def test_exclude_multiple_and_comma_list(self):
    # Exclude dirA using one -x and dirB via comma list plus .git_mock
    rc, out, err = self.run_tree('--show-files', '-x', 'dirA', '-x', 'dirB,.git_mock', str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
  |
  +-.cache/
  | |
  | +-thing
  |
  +-.gitignore
  |
  +-.hiddenDir/
  | |
  | +-hiddenFile.txt
  |
  +-__pycache__/
  | |
  | +-module.cpython-311.pyc
  |
  +-file_root.txt
  |
  +-script.sh
''', out)

  def test_depth_limit(self):
    rc, out, err = self.run_tree('--show-files', '--depth', '2', str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
  |
  +-.cache/
  | |
  | +-thing
  |
  +-.git_mock/
  | |
  | +-config
  |
  +-.gitignore
  |
  +-.hiddenDir/
  | |
  | +-hiddenFile.txt
  |
  +-__pycache__/
  | |
  | +-module.cpython-311.pyc
  |
  +-dirA/
  | |
  | +-fileA1.txt
  | |
  | +-subDir1/
  | |
  | +-subDir2/
  |
  +-dirB/
  | |
  | +-fileB1.txt
  |
  +-file_root.txt
  |
  +-script.sh
''', out)

  def test_remove_dir_sep_option(self):
    rc, out, err = self.run_tree('--show-files', '--remove-dir-sep', str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
   
    .cache/
     
      thing
   
    .git_mock/
     
      config
   
    .gitignore
   
    .hiddenDir/
     
      hiddenFile.txt
   
    __pycache__/
     
      module.cpython-311.pyc
   
    dirA/
     
      fileA1.txt
     
      subDir1/
       
        fileS1.txt
     
      subDir2/
       
        fileS2.txt
   
    dirB/
     
      fileB1.txt
   
    file_root.txt
   
    script.sh
''', out)

  def test_compact_output(self):
    rc, out, err = self.run_tree('--show-files', '--compact', str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
  +-.cache/
  | +-thing
  +-.git_mock/
  | +-config
  +-.gitignore
  +-.hiddenDir/
  | +-hiddenFile.txt
  +-__pycache__/
  | +-module.cpython-311.pyc
  +-dirA/
  | +-fileA1.txt
  | +-subDir1/
  | | +-fileS1.txt
  | +-subDir2/
  | | +-fileS2.txt
  +-dirB/
  | +-fileB1.txt
  +-file_root.txt
  +-script.sh
''', out)

  def test_compact_showfiles_nohiddenfiles_exclude_output(self):
    rc, out, err = self.run_tree('-cfn', '-x', "__pycache__", str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
  +-dirA/
  | +-fileA1.txt
  | +-subDir1/
  | | +-fileS1.txt
  | +-subDir2/
  | | +-fileS2.txt
  +-dirB/
  | +-fileB1.txt
  +-file_root.txt
  +-script.sh
''', out)

  def test_compact_showfiles_exclude_list_output(self):
    rc, out, err = self.run_tree('-cf', '-x', ".git_mock", "-x", "__pycache__", "-x", ".hiddenDir", str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
  +-.cache/
  | +-thing
  +-.gitignore
  +-dirA/
  | +-fileA1.txt
  | +-subDir1/
  | | +-fileS1.txt
  | +-subDir2/
  | | +-fileS2.txt
  +-dirB/
  | +-fileB1.txt
  +-file_root.txt
  +-script.sh
''', out)

  def test_compact_exclude_list_output(self):
    rc, out, err = self.run_tree('-c', '-x', ".git_mock", "-x", ".hiddenDir", str(TESTDATA_DIR))
    self.assertTreeSuccess(rc, err)
    self.assertEqual('''  tree_testdata/
  +-.cache/
  +-__pycache__/
  +-dirA/
  | +-subDir1/
  | +-subDir2/
  +-dirB/
''', out)

  def test_error_on_non_directory(self):
    file_path = TESTDATA_DIR / 'file_root.txt'
    rc, out, err = self.run_tree(str(file_path))
    self.assertNotEqual(rc, 0)
    self.assertIn("is not a directory", out)
    self.assertIn("See --help!", out)

if __name__ == '__main__':
  unittest.main()
