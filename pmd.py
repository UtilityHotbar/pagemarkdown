import argparse
import markdown
import os
import glob

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	%TITLE%
<body>
%CONTENT%
</body>
</html>
'''

class FileObj:
	def __init__(self, preferred_title, markdown=False):
		self.content = []
		self.title = preferred_title
		self.markdown_mode = markdown

	def compile(self):
		if not self.markdown_mode:
			page_content = HTML_TEMPLATE.replace('%TITLE%', self.title).replace('%CONTENT%', markdown.markdown('\n'.join(self.content)))
			return page_content
		else:
			return '\n'.join(self.content)


def process(target_filename, markdown=False, rootdir=os.getcwd()):
	with open(target_filename, 'r') as f:
		data = [line for line in f.readlines()]
	ignore = False
	shortened_filename = target_filename.removesuffix('.pmd')
	
	curr_line = 0
	chunk_no = 0
	curr_addr = shortened_filename
	if MARKDOWN_MODE:
		curr_addr += '.md'
	else:
		curr_addr += '.html'
	
	files = {curr_addr: FileObj(curr_addr, markdown)}
	while True:
		line = data[curr_line]
		if line.startswith('```'):
			if ignore:
				ignore = False
			else:
				ignore = True
		if not ignore:
			if line.startswith('Â§') or line.startswith('§'):
				chunk_no += 1
				pref_title = None
				curr_addr = None
				if len(line) > 1:
					curr_addr = line.strip('Â§\n')
				else:
					while True:
						curr_line += 1
						nextline = data[curr_line]
						if nextline.startswith('TITLE:'):
							pref_title = '<title>'+nextline.removeprefix('TITLE:').strip()+'</title>'
						elif nextline.startswith('ADDRESS:'):
							curr_addr = nextline.removeprefix('ADDRESS:').strip()
						elif nextline.startswith('Â§') or nextline.startswith('§'):
							break
					if not curr_addr:
						raise RuntimeError(f'Missing local address at chunk number {chunk_no}, line {curr_line+1}.')
				if not pref_title:
					pref_title = ''
				if MARKDOWN_MODE:
					curr_addr += '.md'
				else:
					curr_addr += '.html'
				if not curr_addr in files:
					files[curr_addr] = FileObj(pref_title, markdown)
				curr_line += 1
				continue
		files[curr_addr].content.append(line)
		curr_line += 1
		if curr_line == len(data):
			break
	for file in files:
		if files[file].content:
			dest = file
			if not dest.startswith('/'):
				dest = '/'+dest
			dest = rootdir + dest
			print('Writing to', dest)
			os.makedirs(os.path.dirname(dest), exist_ok=True)
			with open(dest, 'w') as f:
				f.write(files[file].compile())


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Pagemarkdown to HTML converter.')
	parser.add_argument('target', help='Target file or directory to convert from.')
	parser.add_argument('--markdown', '-m', help='Compile to markdown files instead of html files.', action='store_true', default=False)
	parser.add_argument('--directory', '-d', help='Target is a directory.', action='store_true')
	parser.add_argument('--output', '-o', help='Output directory.')
	args = parser.parse_args()

	if args.markdown:
		MARKDOWN_MODE = True
	else:
		MARKDOWN_MODE = False

	if args.directory:
		DIRECTORY_MODE = True
	else:
		DIRECTORY_MODE = False

	if args.output:
		OUTPUT = os.path.abspath(args.output)
	else:
		OUTPUT = os.getcwd()
	if not OUTPUT.endswith('/'):
		OUTPUT += '/'

	if not DIRECTORY_MODE:
		process(args.target, markdown=MARKDOWN_MODE, rootdir=OUTPUT)
	else:
		path = args.target
		if not path.endswith('/'):
			path += '/'
		file_list = [os.path.normpath(filename) for filename in glob.iglob(path + '../**/*.pmd', recursive=True)]
		print(file_list)
		for filename in file_list:
			print(os.path.dirname(filename))
			process(filename, markdown=MARKDOWN_MODE, rootdir=OUTPUT+os.path.dirname(filename))
