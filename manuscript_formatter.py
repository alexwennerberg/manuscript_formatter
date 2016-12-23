import subprocess, os 

def main():
	print('hello world')

def compile_story_word(name):
	print("Creating manuscript for", name)
	try:
		os.remove('test.docx')
	except OSError:
		pass
	with open('temp_file.mdown', 'w') as outfile:
		with open('title_page.mdown') as infile:
			outfile.write(infile.read())
		with open(name) as infile:
			outfile.write(infile.read())
	subprocess.check_call(['pandoc', '-f', 'markdown', '-S', '-t', 'docx', 'temp_file.mdown', '-o', 'test.docx', '--reference-docx=reference.docx'])
	os.remove('temp_file.mdown')

def compile_story_latex(name):
	print("Creating manuscript for " +  name)
	word_count = find_word_count(name)
	output_path = os.path.splitext(name)[0] + '.pdf' 
	try:
		os.remove(output_path)
	except OSError:
		pass
	subprocess.check_call(['pandoc', '--from=markdown_github+yaml_metadata_block',
		'-t', 'latex', name,
		'--latex-engine=xelatex', '--template=story.latex', 
		'-o', output_path, '--variable=wordcount:' + str(word_count)])
	
def create_story(story_name):
	if os.path.exists(story_name):
		print("ERROR - FOLDER ALREADY EXISTS")
		return
	else:
		os.makedirs(story_name)
		notes_file = story_name + "/" + "notes" + ".txt"
		story_file = story_name + "/" + story_name + ".txt"
		f = open(story_file, 'w')
		open(notes_file, 'w')
		f.write('---' + '\n' + 
				'title: ' + story_name + '\n' +
				'shorttitle: ' + story_name + '\n' +
				'---')

def compile_all_stories():
	root_directory = './stories'
	for directory_name, subdirectory_list, file_list in os.walk(root_directory):
		for file_name in file_list:
			if root_directory + "/" + file_name == directory_name + ".md":
				compile_story_latex(directory_name + "/" + file_name)

def find_word_count(story):
	f = open(story)
	words = f.read().split()
	word_count = len(words)
	return int(50 *  round(float(word_count)/50))

compile_all_stories()
